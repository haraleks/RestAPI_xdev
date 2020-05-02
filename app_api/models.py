from datetime import datetime

from app_api import db


class Role(db.Model):
    __tablename__ = 'roles_table'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)
    users = db.relationship('Users', backref='role', lazy=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.role_name)


class Users(db.Model):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles_table.id'), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.full_name, self.phone, self.created_on, self.updated_on)
