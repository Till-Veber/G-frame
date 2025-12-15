from flask import json
from collections import defaultdict
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def apply_mods_to_weapon(weapon, build_mods):
    """
    Применяет моды к оружию в соответствии с ТЗ:
    - critical_chance и status_chance: база × (1 + сумма бонусов / 100)
    - damage: мультипликативный бонус ко всем физ. типам
    - impact/puncture/slash: бонус применяется ТОЛЬКО если база > 0
    - heat/cold/toxin/electricity: добавляются как %(суммы физ.урона), затем комбинируются
    - элементы комбинируются в порядке слотов → образуют взрыв, вирус и др.
    """
    base_shooting = weapon.shooting_types[0]

    # 1. Базовый урон
    base_damage = defaultdict(float)
    for dmg_type, value in base_shooting.damage.items():
        base_damage[dmg_type] = value
    total_physical = base_damage['impact'] + base_damage['puncture'] + base_damage['slash']

    # 2. Суммируем бонусы от всех модов
    total_damage_bonus = 0.0  # damage (%)
    total_multiplicative_bonus = 0.0  # multiplicative_damage (%)
    total_critical_chance_bonus = 0.0  # critical_chance (%)
    total_critical_damage_bonus = 0.0  # critical_damage (%)
    total_status_chance_bonus = 0.0  # status_chance (%)
    total_multishot_bonus = 0.0  # multishot (%)
    total_fire_rate_bonus = 0.0  # fire_rate (%)
    total_reload_speed_bonus = 0.0  # reload_speed (%)
    total_ammo_maximum_bonus = 0.0  # ammo_maximum (%)
    total_magazine_capacity_bonus = 0.0  # magazine_capacity (%)

    # Бонусы к физ. урону
    physical_bonus = {'impact': 0.0, 'puncture': 0.0, 'slash': 0.0}

    # Сбор элементов для комбинирования (в порядке слотов)
    elemental_sources = []
    slot_order = [f'slot{i}' for i in range(1, 9)]
    for slot in slot_order:
        for bm in build_mods:
            if bm.slot == slot:
                mod = bm.mod
                # Суммируем бонусы
                total_damage_bonus += getattr(mod, 'damage', 0)
                total_multiplicative_bonus += getattr(mod, 'multiplicative_damage', 0)
                total_critical_chance_bonus += getattr(mod, 'critical_chance', 0)
                total_critical_damage_bonus += getattr(mod, 'critical_damage', 0)
                total_status_chance_bonus += getattr(mod, 'status_chance', 0)
                total_multishot_bonus += getattr(mod, 'multishot', 0)
                total_fire_rate_bonus += getattr(mod, 'fire_rate', 0)
                total_reload_speed_bonus += getattr(mod, 'reload_speed', 0)
                total_ammo_maximum_bonus += getattr(mod, 'ammo_maximum', 0)
                total_magazine_capacity_bonus += getattr(mod, 'magazine_capacity', 0)

                # Физ. урон (только если база > 0)
                for pt in ['impact', 'puncture', 'slash']:
                    val = getattr(mod, pt, 0)
                    if base_damage[pt] > 0:
                        physical_bonus[pt] += val

                # Чистые элементы
                for et in ['heat', 'cold', 'toxin', 'electricity']:
                    if getattr(mod, et, 0) > 0:
                        elemental_sources.append(et)
                break

    # Базовые элементы оружия
    for et in ['heat', 'cold', 'toxin', 'electricity']:
        if base_damage[et] > 0:
            elemental_sources.append(et)

    # 3. Комбинирование элементов
    combined_damage = defaultdict(float)
    used = set()
    combinations = {
        frozenset(['heat', 'cold']): 'blast',
        frozenset(['heat', 'toxin']): 'gas',
        frozenset(['heat', 'electricity']): 'radiation',
        frozenset(['cold', 'toxin']): 'viral',
        frozenset(['cold', 'electricity']): 'magnetic',
        frozenset(['toxin', 'electricity']): 'corrosive'
    }

    i = 0
    while i < len(elemental_sources):
        if i in used:
            i += 1
            continue
        j = i + 1
        while j < len(elemental_sources):
            if j in used:
                j += 1
                continue
            pair = frozenset([elemental_sources[i], elemental_sources[j]])
            if pair in combinations:
                combined_type = combinations[pair]
                combined_damage[combined_type] += total_physical
                used.add(i)
                used.add(j)
                break
            j += 1
        i += 1

    # Неиспользованные элементы остаются как есть
    for idx, et in enumerate(elemental_sources):
        if idx not in used:
            combined_damage[et] += total_physical

    # 4. Применяем бонусы к физ. урону
    final_damage = defaultdict(float)
    for pt in ['impact', 'puncture', 'slash']:
        base_val = base_damage[pt]
        if base_val > 0:
            final_damage[pt] = base_val * (1 + physical_bonus[pt] / 100.0)
        else:
            final_damage[pt] = 0.0

    # 5. Общий бонус урона (damage)
    damage_mult = 1 + total_damage_bonus / 100.0
    for pt in ['impact', 'puncture', 'slash']:
        final_damage[pt] *= damage_mult

    # 6. Добавляем комбинированный/элементальный урон
    for dmg_type, value in combined_damage.items():
        final_damage[dmg_type] += value

    # 7. Мультипликативный урон
    mult_damage_factor = 1 + total_multiplicative_bonus / 100.0
    for dmg_type in final_damage:
        final_damage[dmg_type] *= mult_damage_factor

    # 8. Шансы и скорострельность
    critical_chance = (base_shooting.critical_chance / 100.0) * (1 + total_critical_chance_bonus / 100.0)
    critical_damage = base_shooting.critical_damage * (1 + total_critical_damage_bonus / 100.0)
    status_chance = (base_shooting.status_chance / 100.0) * (1 + total_status_chance_bonus / 100.0)
    multishot = base_shooting.multishot * (1 + total_multishot_bonus / 100.0)
    fire_rate = base_shooting.fire_rate * (1 + total_fire_rate_bonus / 100.0)
    reload_speed = 1.0 * (1 + total_reload_speed_bonus / 100.0)
    ammo_maximum = 1.0 * (1 + total_ammo_maximum_bonus / 100.0)
    magazine_capacity = 1.0 * (1 + total_magazine_capacity_bonus / 100.0)

    return {
        'damage': dict(final_damage),
        'critical_chance': critical_chance,  # в долях (например, 1.02 = 102%)
        'critical_damage': critical_damage,
        'status_chance': status_chance,  # в долях
        'multishot': multishot,
        'fire_rate': fire_rate,
        'reload_speed': reload_speed,
        'ammo_maximum': ammo_maximum,
        'magazine_capacity': magazine_capacity,
    }


def get_damage_multiplier(target, dmg_type):
    """Возвращает множитель урона для типа урона против цели"""
    for dm in target.damage_multipliers:
        if dm.type == dmg_type:
            return dm.value
    return 1.0


def calculate_damage_to_component(raw_damage, target, component='health'):
    """
    Рассчитывает урон по компоненту (shield, armor, health)
    """
    total_damage = 0
    for dmg_type, value in raw_damage.items():
        multiplier = get_damage_multiplier(target, dmg_type)
        total_damage += value * multiplier
    return total_damage


def calculate_armor_reduction(armor):
    """Рассчитывает снижение урона от брони"""
    if armor <= 0:
        return 0
    return armor / (armor + 300)


def run_damage_simulation(build, target, level=1, is_eximus=False):
    """Основная функция симуляции с обработкой ошибок"""
    try:
        if not build.weapon:
            raise ValueError("Билд не имеет связанного оружия")

        scaled_stats = target.get_scaled_stats(level=level, is_eximus=is_eximus)

        # Создаём временный объект для расчётов
        class ScaledTarget:
            def __init__(self, base_target, stats):
                self.damage_multipliers = base_target.damage_multipliers
                self.health = stats['health']
                self.shields = stats['shields']
                self.armor = stats['armor']
                self.fraction = base_target.fraction

        scaled_target = ScaledTarget(target, scaled_stats)

        # Применяем моды
        weapon_params = apply_mods_to_weapon(build.weapon, build.build_mods)

        # Базовые расчёты
        raw_damage = weapon_params['damage']
        shield_damage = calculate_damage_to_component(raw_damage, target)
        health_damage = calculate_damage_to_component(raw_damage, target)
        armor_reduction = calculate_armor_reduction(target.armor)
        effective_health_damage = health_damage * (1 - armor_reduction)

        shield_dps = shield_damage * weapon_params['multishot'] * weapon_params['fire_rate']
        health_dps = effective_health_damage * weapon_params['multishot'] * weapon_params['fire_rate']

        total_health = target.shields + target.health
        if target.shields > 0:
            shield_time = target.shields / shield_dps if shield_dps > 0 else float('inf')
            health_time = target.health / health_dps if health_dps > 0 else float('inf')
            total_time = shield_time + health_time
            avg_dps = total_health / total_time if total_time > 0 else 0
        else:
            avg_dps = health_dps

        kill_time = total_health / avg_dps if avg_dps > 0 else float('inf')

        chart_title = f"Уровень {level}" + (" (Eximus)" if is_eximus else "")

        # Генерация графика
        times, health_remaining = simulate_damage_over_time(weapon_params, target, simulation_time=kill_time + 2)
        chart_path = generate_damage_chart(times, health_remaining, build.id, target.id)
        # Извлекаем имя файла из полного пути
        filename = os.path.basename(chart_path)
        chart_url = f"/charts/{filename}"

        return json.dumps({
            'shield_dps': round(shield_dps, 2),
            'health_dps': round(health_dps, 2),
            'avg_dps': round(avg_dps, 2),
            'kill_time': round(kill_time, 2),
            'shield_time': round(target.shields / shield_dps, 2) if shield_dps > 0 else float('inf'),
            'health_time': round(target.health / health_dps, 2) if health_dps > 0 else float('inf'),
            'total_health': total_health,
            'chart_url': chart_url,
            'damage_breakdown': {k: round(v, 2) for k, v in dict(raw_damage).items()},
            'level': level,
            'is_eximus': is_eximus,
            'scaled_stats': scaled_stats
        })

    except Exception as e:
        print(f"❌ Ошибка в run_damage_simulation: {e}")
        return json.dumps({
            'error': str(e),
            'success': False
        })

def simulate_damage_over_time(weapon_params, target, simulation_time=10.0):
    """
    Симулирует урон по времени с шагом 0.1 сек
    Возвращает списки времени и оставшегося здоровья
    """
    times = []
    health_remaining = []

    current_shields = float(target.shields)
    current_health = float(target.health)
    armor = float(target.armor)

    time = 0.0
    time_step = 0.1  # шаг симуляции

    # Рассчитываем урон за выстрел
    raw_damage = weapon_params['damage']
    shield_damage_per_shot = calculate_damage_to_component(raw_damage, target)
    health_damage_per_shot = calculate_damage_to_component(raw_damage, target)
    armor_reduction = calculate_armor_reduction(armor)
    effective_health_damage_per_shot = health_damage_per_shot * (1 - armor_reduction)

    # Скорострельность и мультшот
    shots_per_second = weapon_params['fire_rate'] * weapon_params['multishot']
    shots_per_step = shots_per_second * time_step

    while time <= simulation_time and (current_shields > 0 or current_health > 0):
        times.append(time)
        health_remaining.append(current_shields + current_health)

        # Урон за шаг
        shield_damage = shield_damage_per_shot * shots_per_step
        health_damage = effective_health_damage_per_shot * shots_per_step

        # Сначала щиты
        if current_shields > 0:
            if shield_damage >= current_shields:
                health_damage += (shield_damage - current_shields)  # Перекол
                current_shields = 0
            else:
                current_shields -= shield_damage
                health_damage = 0  # Нет урона по здоровью, пока есть щиты

        # Затем здоровье
        if current_health > 0:
            current_health -= health_damage
            if current_health < 0:
                current_health = 0

        time += time_step

    # Добавляем финальную точку
    times.append(time)
    health_remaining.append(0)

    return times, health_remaining


def generate_damage_chart(times, health_remaining, build_id, target_id):
    """Генерирует график и возвращает путь к файлу"""
    plt.figure(figsize=(10, 5))
    plt.plot(times, health_remaining, 'r-', linewidth=2)
    plt.title(f'Урон по цели (Билд #{build_id} vs Цель #{target_id})')
    plt.xlabel('Время (сек)')
    plt.ylabel('Оставшееся здоровье')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().invert_yaxis()  # Здоровье уменьшается

    # Создаём папку для графиков
    chart_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'img', 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    # Уникальное имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'damage_chart_{build_id}_{target_id}_{timestamp}.png'
    filepath = os.path.join(chart_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✅ График сохранён: {filepath}")
    return filepath


def get_weapon_stats_with_mods(build):
    """Подготавливает данные для отображения в шаблоне (возвращает словарь)"""
    if not build.weapon:
        return {}

    weapon_params = apply_mods_to_weapon(build.weapon, build.build_mods)

    return {
        'damage': weapon_params['damage'],
        'critical_chance': weapon_params['critical_chance'],
        'critical_damage': weapon_params['critical_damage'],
        'status_chance': weapon_params['status_chance'],
        'multishot': weapon_params['multishot'],
        'fire_rate': weapon_params['fire_rate'],
        'reload_speed': weapon_params['reload_speed'],
        'ammo_maximum': weapon_params['ammo_maximum'],
        'magazine_capacity': weapon_params['magazine_capacity'],
    }