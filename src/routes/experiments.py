from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from src.models.build import Build
from src.models.game_data import Target
from src.models.experiment import Experiment
from src.utils.damage_calculator import run_damage_simulation
from src.models.base import db
from flask import json

bp = Blueprint('exp', __name__)


@bp.route('/run', methods=['POST'])
@login_required
def run_experiment():
    build_id = request.form.get('build_id', type=int)
    target_id = request.form.get('target_id', type=int)
    level = request.form.get('level', type=int, default=1)
    is_eximus = request.form.get('is_eximus') == '1'

    if not build_id or not target_id:
        return jsonify({'error': 'Билд и цель обязательны'}), 400

    build = Build.query.get_or_404(build_id)
    target = Target.query.get_or_404(target_id)

    try:
        results = run_damage_simulation(build, target, level=level, is_eximus=is_eximus)
        result_data = json.loads(results)

        if 'error' in result_data:
            return jsonify({'error': result_data['error']}), 500

        # Сохраняем эксперимент
        exp = Experiment(build_id=build_id, target_id=target_id, results=results)
        db.session.add(exp)
        db.session.commit()

        return jsonify({
            'success': True,
            'experiment_id': exp.id,
            'results': result_data
        })

    except Exception as e:
        print(f"Ошибка при запуске эксперимента: {e}")
        return jsonify({'error': str(e)}), 500