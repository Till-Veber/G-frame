# src/routes/builds.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.base import db
from src.models.game_data import Weapon, Mod, Arcane
from src.models.build import Build, BuildMod
from flask import abort
from src.models.game_data import Target
from src.utils.damage_calculator import get_weapon_stats_with_mods

bp = Blueprint('builds', __name__)


@bp.route('/')
def list_builds():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    if query:
        builds = Build.query.filter(Build.title.ilike(f'%{query}%')) \
            .order_by(Build.id.desc()) \
            .paginate(page=page, per_page=12)
    else:
        builds = Build.query.order_by(Build.id.desc()).paginate(page=page, per_page=12)

    return render_template('builds/list.html', builds=builds, search_query=query)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_build():
    if request.method == 'POST':

        weapon_id = request.form.get('weapon_id', type=int)
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not weapon_id or not title:
            flash('Название билда и оружие обязательны.', 'danger')
            return redirect(request.url)

        # Создаём билд
        build = Build(
            title=title,
            description=description,
            weapon_id=weapon_id,
            author_id=current_user.id,
            arcane_id=None
        )
        db.session.add(build)
        db.session.flush()

        # Обрабатываем слоты: exilus + slot1 ... slot8
        slot_names = ['exilus'] + [f'slot{i}' for i in range(1, 9)]
        for slot in slot_names:
            mod_id_str = request.form.get(f'slot_{slot}')
            if mod_id_str and mod_id_str.isdigit():
                mod_id = int(mod_id_str)
                mod = Mod.query.get(mod_id)
                if mod:
                    build_mod = BuildMod(build_id=build.id, mod_id=mod_id, slot=slot)
                    db.session.add(build_mod)

        # Arcane
        arcane_id_str = request.form.get('slot_arcane')
        if arcane_id_str and arcane_id_str.isdigit():
            arcane = Arcane.query.get(int(arcane_id_str))
            if arcane:
                build.arcane_id = arcane.id

        try:
            db.session.commit()
            flash('Билд успешно сохранён!', 'success')
            return redirect(url_for('builds.view_build', build_id=build.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при сохранении: {str(e)}', 'danger')
            return redirect(request.url)

    # === GET-запрос ===
    weapon_id = request.args.get('weapon_id', type=int)
    if not weapon_id:
        flash('⚠️ Выберите оружие для создания билда.', 'warning')
        return redirect(url_for('main.index'))

    weapon = Weapon.query.get_or_404(weapon_id)

    # Передаём данные для проверки эквивалентов в JS
    all_mods = Mod.query.all()
    mod_name_map = {mod.id: mod.name_eng for mod in all_mods}
    equivalent_map = {}
    for mod in all_mods:
        if mod.equivalents:
            equivalent_map[mod.id] = [mod.name_eng] + mod.equivalents
        else:
            equivalent_map[mod.id] = [mod.name_eng]

    return render_template('builds/create.html',
                           weapon=weapon,
                           mod_name_map=mod_name_map,
                           equivalent_map=equivalent_map)


@bp.route('/<int:build_id>')
def view_build(build_id):
    build = Build.query.get_or_404(build_id)
    targets = Target.query.order_by(Target.name_ru).all()
    weapon_stats = get_weapon_stats_with_mods(build)
    return render_template('builds/view.html',
                           build=build,
                           targets=targets,
                           weapon_stats=weapon_stats)

@bp.route('/<int:build_id>/delete', methods=['POST'])
@login_required
def delete_build(build_id):
    build = Build.query.get_or_404(build_id)
    if build.author_id != current_user.id:
        abort(403)
    db.session.delete(build)
    db.session.commit()
    flash('Билд удалён.', 'info')
    return redirect(url_for('user.my_builds'))