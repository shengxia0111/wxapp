#!C:\Users\GP63 006\AppData\Local\Programs\Python\Python36
# -*- coding: utf-8 -*-

__author__ = 'Sheng Xia'

'''
Test WSGI connection
'''

from flask import Flask, render_template, jsonify

app = Flask(__name__)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True
    )


@app.route('/')
def hello_world():
    return "<h1 style='color:red' algin='center'>Hello World!<h1>"


@app.route('/main/')
def westos():
    # 如何在flask程序中返回一个html页面；flask默认查找页面内容的位置为templates目录；
    return render_template('main.html')


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }]


@app.route('/restful/getTask', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/restful/postTask', methods=['POST'])
def post_tasks():
    return jsonify({'tasks': tasks})
