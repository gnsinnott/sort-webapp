# Data models.
from . import db
from flask_marshmallow import Marshmallow
from . import ma



class ScrapReasons(db.Model):
    # Data model for scrap reasons

    __tablename__ = "scrap-reasons"
    id = db.Column(db.Integer, primary_key=True)
    scrap_reason = db.Column(db.String(64), index=False, unique=True, nullable=False)

    def populate_table():
        # populates table with scrap reasons from text file
        scrap_codes = open('app/scrapreasons.txt', 'r')

        for line in scrap_codes:
            exists = ScrapReasons.query.filter_by(scrap_reason=line.strip()).first()
            # Only add if reason does not all ready exist
            if not exists:
                print(line.strip())
                new_reasons = ScrapReasons(scrap_reason = line.strip())
                db.session.add(new_reasons)
                db.session.commit()

class Record(db.Model):
    # Data model for labor records.

    __tablename__ = "sort-data"
    id = db.Column(db.Integer, primary_key=True)
    Employee = db.Column(db.String(64), index=False, unique=False, nullable=False)
    StartTime = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    TableNumber = db.Column(db.Integer, nullable=False)
    Job = db.Column(db.Integer, nullable=False)
    Part = db.Column(db.Integer, nullable=False)
    Operation = db.Column(db.Integer, nullable=False)
    CastDate = db.Column(db.DateTime, nullable=False)
    CastShift = db.Column(db.Integer, nullable=False)
    GoodQuantity = db.Column(db.Integer, index=False, unique=False, nullable=False)
    Assembly = db.Column(db.Integer, nullable=True)
    AutoSort = db.Column(db.Integer, nullable=True)
    BadThreads = db.Column(db.Integer, nullable=True)
    Bent = db.Column(db.Integer, nullable=True)
    Blisters = db.Column(db.Integer, nullable=True)
    BrokenCore = db.Column(db.Integer, nullable=True)
    Buffing = db.Column(db.Integer, nullable=True)
    Contamination = db.Column(db.Integer, nullable=True)
    DamagedDie = db.Column(db.Integer, nullable=True)
    Debris = db.Column(db.Integer, nullable=True)
    Dimensional = db.Column(db.Integer, nullable=True)
    Flash = db.Column(db.Integer, nullable=True)
    GateVestige = db.Column(db.Integer, nullable=True)
    HeatSinks = db.Column(db.Integer, nullable=True)
    EjectorPinLength = db.Column(db.Integer, nullable=True)
    Lamination = db.Column(db.Integer, nullable=True)
    LeakTest = db.Column(db.Integer, nullable=True)
    MixedParts = db.Column(db.Integer, nullable=True)
    Other = db.Column(db.Integer, nullable=True)
    PartDamage = db.Column(db.Integer, nullable=True)
    PartsNotTapped = db.Column(db.Integer, nullable=True)
    PartsOnGates = db.Column(db.Integer, nullable=True)
    Plating = db.Column(db.Integer, nullable=True)
    PoorFill = db.Column(db.Integer, nullable=True)
    Porosity = db.Column(db.Integer, nullable=True)
    Skiving = db.Column(db.Integer, nullable=True)
    Soldering = db.Column(db.Integer, nullable=True)
    StartUp = db.Column(db.Integer, nullable=True)
    SurfaceFinish = db.Column(db.Integer, nullable=True)
    TrimDamage = db.Column(db.Integer, nullable=True)
    Weight = db.Column(db.Integer, nullable=True)
    WrongPart = db.Column(db.Integer, nullable=True)
    EndTime = db.Column(db.DateTime, nullable=True)
    Rework = db.Column(db.Integer, nullable=True)
    NIT = db.Column(db.Integer, nullable=True)
    Hours = db.Column(db.Integer, nullable=True)
    Obsolete = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return "<User {}>".format(self.Employee)

class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Record
        include_fk = True