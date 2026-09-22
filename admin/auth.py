from flask import render_template, request, redirect, url_for, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from admin import admin_bp
from extensions import db
from models.user import User
from helpers.upload import get_thumb_name

@admin_bp.get('/login', endpoint='login')
def login():
    module = 'login'
    return render_template('login.html', module=module)

@admin_bp.post('/login', endpoint='do_login')
def do_login():
    module = 'login'
    form = request.form

    username = form.get('username', '').strip()
    password = form.get('password', '')

    sql = text("SELECT * FROM user WHERE username = :username")
    result = db.session.execute(sql, {"username": username}).fetchone()

    if result:
        user = dict(result._mapping)
        if check_password_hash(user['password'], password):
            session.clear()
            session['is_login'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user.get('role', 'admin')
            session['user_role'] = user.get('role', 'admin')

            profile_file = user.get('profile')
            if profile_file:
                thumb = get_thumb_name(profile_file)
                session['profile_image'] = f"images/user/{thumb}"
                session['profile'] = profile_file
            else:
                session['profile_image'] = "images/no-image.jpg"
                session['profile'] = None

            return redirect(url_for('admin_bp.dashboard'))

    return render_template('login.html', module=module, error="Invalid username or password")

@admin_bp.get('/register', endpoint='register')
def register():
    module = 'register'
    return render_template('register.html', module=module)

@admin_bp.post('/register', endpoint='do_register')
def do_register():
    module = 'register'
    form = request.form
    username = form.get('username', '').strip()
    email = form.get('email', '').strip()
    password = form.get('password', '')
    confirm_password = form.get('confirm_password', '')

    if not username or not email or not password:
        return render_template('register.html', module=module, error="All fields are required")

    if confirm_password and password != confirm_password:
        return render_template('register.html', module=module, error="Passwords do not match")

    sql = text("SELECT id FROM user WHERE username = :username OR email = :email")
    existing = db.session.execute(sql, {"username": username, "email": email}).fetchone()
    if existing:
        return render_template('register.html', module=module, error="Username or email already exists")

    hashed_pw = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_pw,
        role='user',
        profile=None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('admin_bp.login'))

@admin_bp.get('/logout', endpoint='logout')
def logout():
    session.clear()
    return redirect(url_for('admin_bp.login'))
