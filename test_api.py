#coding=utf-8
import requests

s = requests

data={"code":"061nDIEX1KvkR01o8bEX1PDpEX1nDIE2"}
r = s.post('http://127.0.0.1:5000/auth', data)
