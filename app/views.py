from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProgileForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(author=current_user)
        post.body=form.post.data
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template(
        "index.html",
        title='Home Page',
        form=form,
        posts=posts
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template(
        "login.html",
        title='Sign In',
        form=form
    )

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        title='Register',
        form=form
    )

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    return render_template(
        'user.html',
        user=user,
        posts=posts
    )

@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditProgileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    #elif request.method == 'GET':
     #   form.username.data = current_user.username
     #   form.about_me = current_user.about_me
    return render_template(
        "edit.html",
        title='Edit Profile',
        form=form
    )

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()