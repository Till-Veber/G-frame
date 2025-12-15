from flask import Blueprint, render_template, request, jsonify
from src.models.game_data import Weapon, Mod, Arcane, Target
import re

bp = Blueprint('main', __name__)


def normalize_text(s):
    if not s:
        return ""
    s = s.lower()
    s = s.replace('ё', 'е')
    s = re.sub(r'[^а-яa-z0-9]', '', s)
    return s


@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/api/search-weapons')
def search_weapons():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    normalized_query = normalize_text(query)

    # Получаем все оружия (для небольшой БД — допустимо)
    weapons = Weapon.query.all()
    matches = []

    for w in weapons:
        # Проверяем совпадение по русскому и английскому названию
        if (normalized_query in normalize_text(w.name_ru)) or \
           (normalized_query in normalize_text(w.name_eng)):
            matches.append({
                'name_eng': w.name_eng,
                'name_ru': w.name_ru,
                'id': w.id
            })
            if len(matches) >= 5:
                break

    return jsonify(matches)

@bp.route('/api/search-mods')
def search_mods():
    try:
        query = request.args.get('q', '').strip().lower()
        weapon_types = request.args.getlist('weapon_type')
        slot_type = request.args.get('slot_type', '')  # 'exilus' или обычный слот

        if not weapon_types:
            return jsonify([])

        mods = Mod.query.all()
        matches = []

        for mod in mods:
            # 1. Проверка совместимости с оружием
            if not any(wt in mod.weapon_types for wt in weapon_types):
                continue

            # 2. Для Exilus-слота — только exilus: true
            if slot_type == 'exilus' and not mod.exilus:
                continue

            # 3. Для обычных слотов — только НЕ exilus
            if slot_type != 'exilus' and mod.exilus:
                continue

            # 4. Фильтрация по запросу
            if query:
                if query in mod.name_ru.lower() or query in mod.name_eng.lower():
                    matches.append({
                        'id': mod.id,
                        'name_eng': mod.name_eng,
                        'name_ru': mod.name_ru,
                        'icon': f"/static/img/mods/{mod.name_eng}.png"
                    })
            else:
                # Если запрос пустой — показываем все совместимые (но ограничим 15)
                matches.append({
                    'id': mod.id,
                    'name_eng': mod.name_eng,
                    'name_ru': mod.name_ru,
                    'icon': f"/static/img/mods/{mod.name_eng}.png"
                })

        # Ограничиваем 15 результатами
        return jsonify(matches[:15])
    except Exception as e:
        print(f"Ошибка в /api/search-mods: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route('/api/search-arcanes')
def search_arcanes():
    try:
        query = request.args.get('q', '').strip().lower()
        weapon_types = request.args.getlist('weapon_type')

        if not weapon_types:
            return jsonify([])

        arcanes = Arcane.query.all()
        matches = []

        for arcane in arcanes:
            # Проверка совместимости с оружием
            if any(wt in arcane.weapon_types for wt in weapon_types):
                if query:
                    if query in arcane.name_ru.lower() or query in arcane.name_eng.lower():
                        matches.append({
                            'id': arcane.id,
                            'name_eng': arcane.name_eng,
                            'name_ru': arcane.name_ru,
                            'icon': f"/static/img/arcanes/{arcane.name_eng}.png"
                        })
                else:
                    matches.append({
                        'id': arcane.id,
                        'name_eng': arcane.name_eng,
                        'name_ru': arcane.name_ru,
                        'icon': f"/static/img/arcanes/{arcane.name_eng}.png"
                    })

        return jsonify(matches[:15])
    except Exception as e:
        print(f"Ошибка в /api/search-arcanes: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/api/search-targets')
def search_targets():
    query = request.args.get('q', '').strip()
    targets = Target.query.order_by(Target.name_ru).all()
    matches = []

    for t in targets:
        if query:
            normalized_query = normalize_text(query)
            if (normalized_query in normalize_text(t.name_ru)) or \
               (normalized_query in normalize_text(t.name_eng)):
                matches.append({
                    'id': t.id,
                    'name_ru': t.name_ru,
                    'name_eng': t.name_eng,
                    'fraction': t.fraction
                })
        else:
            matches.append({
                'id': t.id,
                'name_ru': t.name_ru,
                'name_eng': t.name_eng,
                'fraction': t.fraction
            })
        if len(matches) >= 10:  # Ограничиваем 10 результатами
            break

    return jsonify(matches)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/team')
def team():
    return render_template('main/team.html')