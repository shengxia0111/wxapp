#!C:\Users\GP63 006\AppData\Local\Programs\Python\Python36
# -*- coding: utf-8 -*-

'''
Models for tables(departmentinfo, regesterinfo, sessioninfo, userinfo, userrole)
'''

__author__ = 'Sheng Xia'

# Web框架
from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy

# 程序内模块
from config.config import configs
from app import app
from models.models import UserRole,UserInfo,RegisterStatus,DepartmentInfo

# 微信API
from weixin import WXAPPAPI



