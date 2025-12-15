from .base import Base, db


class Experiment(Base):
    __tablename__ = 'experiments'

    build_id = db.Column(db.Integer, db.ForeignKey('builds.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'), nullable=False)

    # Параметры эксперимента
    simulation_time = db.Column(db.Float, default=10.0)
    accuracy = db.Column(db.Float, default=1.0)

    # Результаты (можно хранить как JSON)
    results = db.Column(db.Text, nullable=True)

    build = db.relationship('Build', backref=db.backref('experiments', lazy=True))
    target = db.relationship('Target', backref=db.backref('experiments', lazy=True))