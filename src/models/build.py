from .base import Base, db

class Build(Base):
    __tablename__ = 'builds'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapons.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    arcane_id = db.Column(db.Integer, db.ForeignKey('arcanes.id'), nullable=True)

    # Связи
    weapon = db.relationship('Weapon', backref=db.backref('builds', lazy=True))
    author = db.relationship('User', backref=db.backref('builds', lazy=True))
    arcane = db.relationship('Arcane', backref=db.backref('builds', lazy=True))
    build_mods = db.relationship('BuildMod', back_populates='build', cascade='all, delete-orphan')

    @property
    def mods_by_slot(self):
        """Возвращает словарь: {'slot1': Mod, 'exilus': Mod, ...}"""
        slots = {bm.slot: bm.mod for bm in self.build_mods}
        for i in range(1, 9):
            slots.setdefault(f'slot{i}', None)
        slots.setdefault('exilus', None)
        slots.setdefault('arcane', None)
        return slots

class BuildMod(Base):
    __tablename__ = 'build_mods'

    build_id = db.Column(db.Integer, db.ForeignKey('builds.id'), nullable=False)
    mod_id = db.Column(db.Integer, db.ForeignKey('mods.id'), nullable=False)
    slot = db.Column(db.String(16), nullable=False)

    build = db.relationship('Build', back_populates='build_mods')
    mod = db.relationship('Mod', backref=db.backref('build_mods', lazy=True))