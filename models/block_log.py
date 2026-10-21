from datetime import datetime
from extensions import db

class BlockLog(db.Model):
    #table name, column
    __tablename__ = 'block_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    methods = db.Column(db.String(20), nullable=False)
    attempts = db.Column(db.String(100), nullable=True)
    device = db.Column(db.String(500), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #What it does: The constructor method called whenever you create a new log object in Python.
    # call it to use when we want to catch data for saving into database
    def __init__(self, ip, endpoint, methods, attempts=None, device=None, create_at=None):
        self.ip = ip
        self.endpoint = endpoint
        self.methods = methods
        self.attempts = attempts
        self.device = device
        self.create_at = create_at or datetime.utcnow()

    # convert data into dictionary, easy to transfer data into JSON
    def to_dict(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'endpoint': self.endpoint,
            'methods': self.methods,
            'attempts': self.attempts,
            'device': self.device,
            'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S') if self.create_at else ''
        }
    