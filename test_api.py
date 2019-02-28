#coding=utf-8
import requests

s = requests

data={"code":"00132DSg2zd3MA0yooSg2mdUSg232DSZ-"}
r = s.post('http://127.0.0.1:5000/auth', data)
