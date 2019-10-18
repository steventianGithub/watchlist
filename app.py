from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'user: %s' % name

@app.route('/test')
def test_url_for():
    #调用示例
    print(url_for('hello')) #输出：/
    #注意下面两个调用是如何生成包含URL变量的URL的
    print(url_for('user_page', name='tian'))    #输出/user/tian
    print(url_for('user_page', name='Shuo'))    #输出/user/shuo
    print(url_for('test_url_for'))  #输出/test
    #下面这个调用传入了多余的关键字参数，他们会被作为查询字符串附加到URl后面
    print(url_for('test_url_for', num=2))   #输出/test？num=2
    return 'Test Page'