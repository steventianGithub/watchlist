from watchlist import app, db
from watchlist.models import User, Movie
from flask import url_for, render_template
from flask import request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))
        
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('index'))
        
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    #判断是否是POST请求
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        #获取表单数据
        title = request.form.get('title')   #传入表单对应输入字段的name值
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.') #显示错误提示
            return redirect(url_for('index'))   #重定向回主页
        #保存表单数据到数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    user = User.query.first()   #读取用户记录
    movies = Movie.query.all()  #读取所有电影记录
    return render_template('index.html', movies=movies)

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


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':    #处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)    

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  #限定只接受POST请求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))