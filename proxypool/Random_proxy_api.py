from flask import Flask,g
from 代理池.Redis_db import RedisClient

__all__=['app']
app=Flask(__name__)

def get_connection():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():#首页
    return '<h2>Welcome to Proxy Pool System<h2>\n<h2>输入random_100获取分数排名前100代理<h2>\n<h2>输入count查看代理总数<h2>\n<h2>输入all_100获取所有可用代理<h2>\n<h2>输入random获取随机可用代理<h2>'

@app.route('/random_100')
def get_one_100_proxy():#随机代理页
    connection = get_connection()
    return connection.random_100()

@app.route('/count')
def get_counts():#获取数量页
    connection = get_connection()
    return str(connection.count())

@app.route('/random')
def get_proxy():
    connection = get_connection()
    return connection.random()

@app.route("/all_100")
def get_all_100_proxy():
    connection = get_connection()
    return connection.all_100()

if __name__ == '__main__':
    app.run()