from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectnummer = db.Column(db.String(50), unique=True, nullable=False)
    klant = db.Column(db.String(100), nullable=False)
    locatie = db.Column(db.String(200), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    opmerkingen = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'projectnummer': self.projectnummer,
            'klant': self.klant,
            'locatie': self.locatie,
            'datum': self.datum.isoformat(),
            'opmerkingen': self.opmerkingen,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Raam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    ruimte = db.Column(db.String(100), nullable=False)
    raamtype = db.Column(db.String(50))
    breedte = db.Column(db.Float, nullable=False)
    hoogte = db.Column(db.Float, nullable=False)
    plafondhoogte = db.Column(db.Float, nullable=False)
    ophangsysteem = db.Column(db.String(50))
    montagewijze = db.Column(db.String(50))
    rail_lengte = db.Column(db.Float, nullable=False)
    stof = db.Column(db.String(100))
    voering = db.Column(db.String(50))
    plooi = db.Column(db.String(50))
    motorisatie = db.Column(db.Boolean, default=False)
    opmerkingen = db.Column(db.Text)
    foto = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = db.relationship('Project', backref=db.backref('ramen', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'ruimte': self.ruimte,
            'raamtype': self.raamtype,
            'breedte': self.breedte,
            'hoogte': self.hoogte,
            'plafondhoogte': self.plafondhoogte,
            'ophangsysteem': self.ophangsysteem,
            'montagewijze': self.montagewijze,
            'rail_lengte': self.rail_lengte,
            'stof': self.stof,
            'voering': self.voering,
            'plooi': self.plooi,
            'motorisatie': self.motorisatie,
            'opmerkingen': self.opmerkingen,
            'foto': self.foto,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 