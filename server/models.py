from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    superpowers = db.relationship('Power', secondary='hero_powers', backref='superheroe')

    # add serialization rules
    serialize_rules = ('id', 'name', 'super_name', 'superpowers')
    
    
    def __repr__(self):
        return f"Hero(id={self.id}, name='{self.name}', super_name='{self.super_name}', created_at='{self.created_at}', updated_at='{self.updated_at}')"
    

    

    


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    superheroes = db.relationship('Hero', secondary='hero_powers', backref='powers')
    

    # add serialization rules
    serialize_rules = ('id', 'name', 'description')

    # add validation
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    def __repr__(self):
        return f"Power(id={self.id}, name='{self.name}', description='{self.description}', created_at='{self.created_at}', updated_at='{self.updated_at}')"


from sqlalchemy_serializer import SerializerMixin

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationships
    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('power_heroes', cascade='all, delete-orphan'))

    # Define serialization rules
    serialize_rules = ('id', 'strength', 'hero_id', 'power_id', 'created_at', 'updated_at')

    # Define validation
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError("Invalid strength value")
        return value

    def __repr__(self):
        return f"HeroPower(id={self.id}, strength='{self.strength}', hero_id={self.hero_id}, power_id={self.power_id}, created_at='{self.created_at}', updated_at='{self.updated_at}')"
    

