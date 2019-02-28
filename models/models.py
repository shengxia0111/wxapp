#!C:\Users\GP63 006\AppData\Local\Programs\Python\Python36
# -*- coding: utf-8 -*-

'''
Models for tables(departmentinfo, regesterinfo, sessioninfo, userinfo, userrole)
'''

__author__ = 'Sheng Xia'

from app import db


class UserInfo(db.Model):
    __table__ = 'userinfo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(40))
    user_name = db.Column(db.String(32))
    cellphone = db.Column(db.String(32))
    email = db.Column(db.String(40))
    status = db.Column(db.Integer, db.ForeignKey('registerstatus.status_id'),nullable=False, default=1)
    role_id = db.Column(db.Integer, db.ForeignKey('userrole.role_id'), nullable=False, default=1)
    department_id = db.Column(db.Integer, db.ForeignKey('departmentinfo.department_id'), nullable=False, default=1)
    gender = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<User %s>' % self.user_name

class DepartmentInfo(db.Model):
    __table__ = 'departmentinfo'

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(20), nullable=False)

    users = db.relationship('UserInfo', backref='department', lazy=True)

    def __repr__(self):
        return '<Department %s>' % self.department_name


class RegisterStatus(db.Model):
    __table__ = 'registerstatus'

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(10), nullable=False)

    users = db.relationship('UserInfo', backref='registerstatus', lazy=True)

    def __repr__(self):
        return '<RegisterStatus %s>' % self.status_name

class UserRole(db.Model):
    __table__ = 'userrole'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), nullable=False)
    privillege = db.Column(db.String(64), nullable=False, Default='无')

    users= db.relationship('UserInfo', backref='role', lazy=True)

    def __repr__(self):
        return '<UserRole %s with Privillege %s>' % (self.role_name, self.privillege)




