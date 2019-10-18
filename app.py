from flask import Flask, url_for, render_template

app = Flask(__name__)

name = 'Steven Tian'
movies = [    
    {'title': 'My Neighbor Totoro', 'year': '1988'},    
    {'title': 'Dead Poets Society', 'year': '1989'},    
    {'title': 'A Perfect World', 'year': '1993'},   
    {'title': 'Leon', 'year': '1994'},    
    {'title': 'Mahjong', 'year': '1996'},    
    {'title': 'Swallowtail Butterfly', 'year': '1996'},    
    {'title': 'King of Comedy', 'year': '1999'},    
    {'title': 'Devils on the Doorstep', 'year': '1999'},   
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'}, 
]

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', name=name, movies=movies)

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