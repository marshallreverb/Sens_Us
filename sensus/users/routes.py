from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from sensus import db, bcrypt
from sensus.models import User
from sensus.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from sensus.users.utils import save_picture, send_reset_email

users =Blueprint('users',__name__)


@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('/register.html',form=form)


@users.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page =  request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(f'Login Unsucessfull. Please check username or password ','danger')
    return render_template('/login.html',form=form)




@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data :
            picture_data = save_picture(form.picture.data)
            current_user.image_file = picture_data
        current_user.usename = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','success')
        return redirect(url_for('main.index'))
    return render_template('reset_request.html', title='Reset Password', form= form)


@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password = hashed_pw)
        user.password = hashed_pw
        db.session.commit()
        flash(f'Your Password has been updated ! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)