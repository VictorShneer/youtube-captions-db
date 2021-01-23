"""
authentication routes
"""

from flask import render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from app.auth import bp
from app.auth.forms import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('login.html', title='LogIn', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/ligon', methods=['POST'])
def ligon():
    creds = request.get_json()  
    #TODO
    #validate creds
    try:
        email = creds['email']
        p = creds['p']
    except:
        abort(403)
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(p):
        return {'message':'hey dog!'}
    token = user.get_token()
    return {'token':token}