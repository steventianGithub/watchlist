from watchlist import app, db
from watchlist.models import User, Movie
from flask import render_template

@app.errorhandler(404)  #传入要处理的错误代码
def page_not_found(e):  #接受异常对象作为参数
    user = User.query.first()
    return render_template('errors/404.html'), 404  #返回模板和代码