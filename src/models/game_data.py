from sqlalchemy.dialects.sqlite import JSON
from .base import Base, db

# ===============
# WEAPON MODELS
# ===============

class Weapon(Base):
    __tablename__ = 'weapons'

    name_eng = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)
    types = db.Column(JSON, nullable=False)
    magazine_capacity = db.Column(db.Integer, nullable=False)
    ammo_maximum = db.Column(db.Integer, nullable=False)
    reload_time = db.Column(db.Float, nullable=False)

    shooting_types = db.relationship('ShootingType', back_populates='weapon', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Weapon {self.name_eng}>"

class ShootingType(Base):
    __tablename__ = 'shooting_types'

    weapon_id = db.Column(db.Integer, db.ForeignKey('weapons.id'), nullable=False)
    name_eng = db.Column(db.String(128), nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)
    damage = db.Column(JSON, nullable=False)
    critical_chance = db.Column(db.Integer, nullable=False)
    critical_damage = db.Column(db.Float, nullable=False)
    status_chance = db.Column(db.Integer, nullable=False)
    forced_procs = db.Column(JSON, nullable=False)
    fire_rate = db.Column(db.Float, nullable=False)
    ammo_cost = db.Column(db.Integer, nullable=False)
    multishot = db.Column(db.Float, nullable=False)

    weapon = db.relationship('Weapon', back_populates='shooting_types')

    def __repr__(self):
        return f"<ShootingType {self.name_eng} for {self.weapon.name_eng}>"

# ===========
# MOD MODEL
# ===========

class Mod(Base):
    __tablename__ = 'mods'

    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)
    description_eng = db.Column(db.Text, nullable=True)
    description_ru = db.Column(db.Text, nullable=True)
    mod_type = db.Column(db.String(32), nullable=False)
    polarity = db.Column(db.String(32), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    exilus = db.Column(db.Boolean, nullable=False)
    weapon_types = db.Column(JSON, nullable=False)
    equivalents = db.Column(JSON, nullable=True)
    locks = db.Column(JSON, nullable=True)
    set_name = db.Column(db.String(128), nullable=True)
    set_bonus = db.Column(db.String(64), nullable=True)
    set_value = db.Column(db.Float, nullable=True)
    set_step = db.Column(db.Float, nullable=True)
    set_mods_count = db.Column(db.Integer, nullable=True)
    conditional = db.Column(JSON, nullable=True)

    # Numeric bonuses
    damage = db.Column(db.Float, default=0)
    impact = db.Column(db.Float, default=0)
    puncture = db.Column(db.Float, default=0)
    slash = db.Column(db.Float, default=0)
    heat = db.Column(db.Float, default=0)
    cold = db.Column(db.Float, default=0)
    electricity = db.Column(db.Float, default=0)
    toxin = db.Column(db.Float, default=0)
    blast = db.Column(db.Float, default=0)
    corrosive = db.Column(db.Float, default=0)
    gas = db.Column(db.Float, default=0)
    magnetic = db.Column(db.Float, default=0)
    radiation = db.Column(db.Float, default=0)
    viral = db.Column(db.Float, default=0)
    critical_chance = db.Column(db.Float, default=0)
    critical_damage = db.Column(db.Float, default=0)
    status_chance = db.Column(db.Float, default=0)
    multishot = db.Column(db.Float, default=0)
    fire_rate = db.Column(db.Float, default=0)
    bows_fire_rate = db.Column(db.Float, default=0)
    reload_speed = db.Column(db.Float, default=0)
    ammo_maximum = db.Column(db.Float, default=0)
    magazine_capacity = db.Column(db.Float, default=0)
    damage_to_corpus = db.Column(db.Float, default=0)
    damage_to_grineer = db.Column(db.Float, default=0)
    damage_to_infested = db.Column(db.Float, default=0)
    damage_to_orokin = db.Column(db.Float, default=0)
    damage_to_murmur = db.Column(db.Float, default=0)
    status_duration = db.Column(db.Float, default=0)
    multiplicative_damage = db.Column(db.Float, default=0)
    weak_point_damage = db.Column(db.Float, default=0)
    weak_point_critical_chance = db.Column(db.Float, default=0)
    extra_critical_chance = db.Column(db.Float, default=0)
    conditional_damage = db.Column(db.Float, default=0)
    ammo_efficiency = db.Column(db.Float, default=0)

    @property
    def all_equivalents(self):
        """Возвращает список name_eng всех эквивалентных модов (включая себя)"""
        if self.equivalents:
            return [self.name_eng] + self.equivalents
        return [self.name_eng]

    def __repr__(self):
        return f"<Mod {self.name_eng}>"

# ==============
# ARCANE MODEL
# ==============

class Arcane(Base):
    __tablename__ = 'arcanes'

    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)
    description_eng = db.Column(db.Text, nullable=True)
    description_ru = db.Column(db.Text, nullable=True)
    weapon_types = db.Column(JSON, nullable=False)
    conditional = db.Column(JSON, nullable=True)

    # Numeric bonuses (same as Mod)
    damage = db.Column(db.Float, default=0)
    critical_chance = db.Column(db.Float, default=0)
    critical_damage = db.Column(db.Float, default=0)
    status_chance = db.Column(db.Float, default=0)
    multishot = db.Column(db.Float, default=0)
    fire_rate = db.Column(db.Float, default=0)
    bows_fire_rate = db.Column(db.Float, default=0)
    reload_speed = db.Column(db.Float, default=0)
    ammo_maximum = db.Column(db.Float, default=0)
    magazine_capacity = db.Column(db.Float, default=0)
    damage_to_corpus = db.Column(db.Float, default=0)
    damage_to_grineer = db.Column(db.Float, default=0)
    damage_to_infested = db.Column(db.Float, default=0)
    damage_to_orokin = db.Column(db.Float, default=0)
    damage_to_murmur = db.Column(db.Float, default=0)
    status_duration = db.Column(db.Float, default=0)
    multiplicative_damage = db.Column(db.Float, default=0)
    weak_point_damage = db.Column(db.Float, default=0)
    weak_point_critical_chance = db.Column(db.Float, default=0)
    extra_critical_chance = db.Column(db.Float, default=0)
    conditional_damage = db.Column(db.Float, default=0)
    ammo_efficiency = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<Arcane {self.name_eng}>"

# ===============
# TARGET MODELS
# ===============

class Target(Base):
    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)
    fraction = db.Column(db.String(32), nullable=False)
    health = db.Column(db.Integer, nullable=False)
    armor = db.Column(db.Integer, nullable=False)
    shields = db.Column(db.Integer, nullable=False)
    head_shot_multiplier = db.Column(db.Float, nullable=True)
    proc_immunity = db.Column(JSON, nullable=False)

    damage_multipliers = db.relationship('DamageMultiplier', back_populates='target', cascade='all, delete-orphan')

    base_level = db.Column(db.Integer, nullable=False, default=1)
    base_health = db.Column(db.Float, default=0.0)
    base_shields = db.Column(db.Float, default=0.0)
    base_armor = db.Column(db.Float, default=0.0)

    # Множители роста (используются в формулах)
    health_level_factor = db.Column(db.Float, default=1.0)
    shield_level_factor = db.Column(db.Float, default=1.0)
    armor_level_factor = db.Column(db.Float, default=1.0)

    # Eximus-множители
    eximus_health_mult = db.Column(db.Float, default=1.0)
    eximus_shield_mult = db.Column(db.Float, default=1.0)
    eximus_armor_mult = db.Column(db.Float, default=1.0)

    def get_scaled_stats(self, level=1, is_eximus=False):
        """Возвращает здоровье, щиты, броню с учётом уровня и Eximus"""
        if level <= 1:
            health = self.base_health
            shields = self.base_shields
            armor = self.base_armor
        else:
            # Формула роста (упрощённая)
            health = self.base_health * (1 + (level - 1) * self.health_level_factor)
            shields = self.base_shields * (1 + (level - 1) * self.shield_level_factor)
            armor = self.base_armor * (1 + (level - 1) * self.armor_level_factor)

        # Eximus-множители
        if is_eximus:
            health *= self.eximus_health_mult
            shields *= self.eximus_shield_mult
            armor *= self.eximus_armor_mult

        return {
            'health': max(health, 0),
            'shields': max(shields, 0),
            'armor': max(armor, 0)
        }

    def __repr__(self):
        return f"<Target {self.name_eng}>"

class DamageMultiplier(Base):
    __tablename__ = 'damage_multipliers'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'), nullable=False)
    type = db.Column(db.String(32), nullable=False)
    value = db.Column(db.Float, nullable=False)

    target = db.relationship('Target', back_populates='damage_multipliers')

    def __repr__(self):
        return f"<DamageMultiplier {self.type}={self.value} for {self.target.name_eng}>"