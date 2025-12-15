# src/utils/load_game_data.py
import os
import json
from src.app import create_app, db
from src.models.game_data import Weapon, ShootingType, Mod, Arcane, Target, DamageMultiplier

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'json', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clear_tables():
    """Очищает игровые таблицы перед загрузкой (чтобы избежать дублей)"""
    db.session.query(ShootingType).delete()
    db.session.query(Weapon).delete()
    db.session.query(Mod).delete()
    db.session.query(Arcane).delete()
    db.session.query(DamageMultiplier).delete()
    db.session.query(Target).delete()
    db.session.commit()

def load_weapons():
    weapons_data = load_json('weapons.json')
    for w in weapons_data:
        weapon = Weapon(
            name_eng=w['name_eng'],
            name_ru=w['name_ru'],
            types=w['types'],
            magazine_capacity=w['magazine_capacity'],
            ammo_maximum=w['ammo_maximum'],
            reload_time=w['reload_time']
        )
        db.session.add(weapon)
        db.session.flush()  # Получаем weapon.id для связей

        for st in w['types_of_shooting']:
            shooting = ShootingType(
                weapon_id=weapon.id,
                name_eng=st['name_eng'],
                name_ru=st['name_ru'],
                damage=st['damage'],
                critical_chance=st['critical_chance'],
                critical_damage=st['critical_damage'],
                status_chance=st['status_chance'],
                forced_procs=st['forced_procs'],
                fire_rate=st['fire_rate'],
                ammo_cost=st['ammo_cost'],
                multishot=st['multishot']
            )
            db.session.add(shooting)
    db.session.commit()
    print(f"✅ Загружено {len(weapons_data)} оружий")

def load_mods():
    mods_data = load_json('mods.json')
    for m in mods_data:
        mod = Mod(
            name_eng=m['name_eng'],
            name_ru=m['name_ru'],
            description_eng=m.get('description_eng'),
            description_ru=m.get('description_ru'),
            mod_type=m['mod_type'],
            polarity=m['polarity'],
            rank=m['rank'],
            capacity=m['capacity'],
            exilus=bool(m['exilus']),
            weapon_types=m['weapon_types'],
            equivalents=m.get('equivalents'),
            locks=m.get('locks'),
            set_name=m.get('set', {}).get('name'),
            set_bonus=m.get('set', {}).get('bonus'),
            set_value=m.get('set', {}).get('value'),
            set_step=m.get('set', {}).get('step'),
            set_mods_count=m.get('set', {}).get('mods'),
            conditional=m.get('conditional')
        )
        # Заполняем числовые бонусы (если есть)
        numeric_fields = [
            'damage', 'impact', 'puncture', 'slash', 'heat', 'cold', 'electricity',
            'toxin', 'blast', 'corrosive', 'gas', 'magnetic', 'radiation', 'viral',
            'critical_chance', 'critical_damage', 'status_chance', 'multishot',
            'fire_rate', 'bows_fire_rate', 'reload_speed', 'ammo_maximum',
            'magazine_capacity', 'damage_to_corpus', 'damage_to_grineer',
            'damage_to_infested', 'damage_to_orokin', 'damage_to_murmur',
            'status_duration', 'multiplicative_damage', 'weak_point_damage',
            'weak_point_critical_chance', 'extra_critical_chance', 'conditional_damage',
            'ammo_efficiency'
        ]
        for field in numeric_fields:
            if field in m:
                setattr(mod, field, float(m[field]))

        db.session.add(mod)
    db.session.commit()
    print(f"✅ Загружено {len(mods_data)} модов")

def load_arcanes():
    arcanes_data = load_json('arcanes.json')
    for a in arcanes_data:
        arcane = Arcane(
            name_eng=a['name_eng'],
            name_ru=a['name_ru'],
            description_eng=a.get('description_eng'),
            description_ru=a.get('description_ru'),
            weapon_types=a['weapon_types'],
            conditional=a.get('conditional')
        )
        numeric_fields = [
            'damage', 'critical_chance', 'critical_damage', 'status_chance', 'multishot',
            'fire_rate', 'bows_fire_rate', 'reload_speed', 'ammo_maximum',
            'magazine_capacity', 'damage_to_corpus', 'damage_to_grineer',
            'damage_to_infested', 'damage_to_orokin', 'damage_to_murmur',
            'status_duration', 'multiplicative_damage', 'weak_point_damage',
            'weak_point_critical_chance', 'extra_critical_chance', 'conditional_damage',
            'ammo_efficiency'
        ]
        for field in numeric_fields:
            if field in a:
                setattr(arcane, field, float(a[field]))

        db.session.add(arcane)
    db.session.commit()
    print(f"✅ Загружено {len(arcanes_data)} мистификаторов")

def load_targets():
    targets_data = load_json('targets.json')
    for t in targets_data:
        # Преобразование head_shot_multiplier: если 'none' — то None
        hsm = t.get('head_shot_multiplier')
        if isinstance(hsm, str) and hsm.lower() == 'none':
            hsm = None
        elif isinstance(hsm, str):
            hsm = float(hsm)  # если это строка с числом, например "1.5"
        # Если уже число — оставляем как есть

        target = Target(
            name_eng=t['name_eng'],
            name_ru=t['name_ru'],
            fraction=t['fraction'],
            health=t['health'],
            armor=t['armor'],
            shields=t['shields'],
            head_shot_multiplier=hsm,
            base_level=t['base_level'],
            proc_immunity=t['proc_immunity']
        )
        db.session.add(target)
        db.session.flush()

        for dm in t['damage_types_multipliers']:
            multiplier = DamageMultiplier(
                target_id=target.id,
                type=dm['type'],
                value=dm['value']
            )
            db.session.add(multiplier)
    db.session.commit()
    print(f"✅ Загружено {len(targets_data)} противников")

def main():
    app = create_app()
    with app.app_context():
        clear_tables()
        load_weapons()
        load_mods()
        load_arcanes()
        load_targets()
        print("🎉 Все игровые данные успешно загружены в БД!")

if __name__ == '__main__':
    main()