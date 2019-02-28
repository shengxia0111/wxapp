#!C:\Users\GP63 006\AppData\Local\Programs\Python\Python36
# -*- coding: utf-8 -*-

'''
Models for tables(departmentinfo, regesterinfo, sessioninfo, userinfo, userrole)
'''

__author__ = 'Sheng Xia'

import os

from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from config.config import configs

# 微信API
from weixin.lib.wxcrypt import WXBizDataCrypt
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError


# Flask与Mysql配置
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(configs.db['user'], \
                                                                                                      configs.db['password'], \
                                                                                                      configs.db['host'], \
                                                                                                      configs.db['port'], \
                                                                                                      configs.db['db'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Flask路由
@app.route('/auth',methods = ['Post'])
def get_user_openid():
    # POST请求数据
    encrypted_data = request.form['encrypted_data']
    iv = request.form['iv']
    code = request.form['code']

    # app配置秘钥
    appid = configs.wxapp['appid']
    app_secret = configs.wxapp['appsecret']

    if not code:
        resp = make_response('Weixin Code Error', 502)
        return resp
    if not appid or not app_secret:
        resp = make_response('Server Internal Error', 500)
        return resp
    api = WXAPPAPI(appid= appid, app_secret= app_secret)
    session_info= api.exchange_code_for_session_key(code=code)
    if not session_info:
        resp = make_response('Weixin API Error', 502)
        return resp
    if not isinstance(session_info,dict):
        resp = make_response('Session Key Error', 500)
        return resp
    open_id = session_info.get('open_id')
    session_key = session_info.get('session_key')
    crypt = WXBizDataCrypt(appid, session_key)
    user_info = crypt.decrypt(encrypted_data, iv)

    resp = make_response(jsonify(session_info))
    return resp

    # is_open_id_in_dase = True if UserInfo.query.filter_by(open_id=open_id).first() else False
    # if not is_open_id_in_dase:
    #     resp = make_response('User Not Registered', 401)
    #     return resp
    # else:
    #     return make_response(jsonify(user_info))

@app.route('/')
def hello_world():
    return "<h1 style='color:red' algin='center'>Hello World!<h1>"


# 数据表
class UserInfo(db.Model):

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

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(20), nullable=False)

    users = db.relationship('UserInfo', backref='department', lazy=True)

    def __repr__(self):
        return '<Department %s>' % self.department_name

class RegisterStatus(db.Model):

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(10), nullable=False)

    users = db.relationship('UserInfo', backref='registerstatus', lazy=True)

    def __repr__(self):
        return '<RegisterStatus %s>' % self.status_name

class UserRole(db.Model):

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), nullable=False)
    privillege = db.Column(db.String(64), nullable=False, default='无')

    users= db.relationship('UserInfo', backref='role', lazy=True)

    def __repr__(self):
        return '<UserRole %s with Privillege %s>' % (self.role_name, self.privillege)


if __name__=='__main__':
    import logging;
    logging.basicConfig('web_info.log', filemode='a', level=logging.INFO)
    app.logger.info('Running Server On 127.0.0.1:5000...')
    app.logger.info('Using Database %s@%s/%s' % (configs.db['user'], configs.db['host'], configs.db['db']))
    app.logger.info('new log!')
    app.run(host='0.0.0.0',port='8085',debug=True)

