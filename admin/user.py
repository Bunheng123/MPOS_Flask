from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from admin import admin_bp
from extensions import db
from models.user import User
from api.user import get_all_users, get_user_by_id
from helpers.upload import (
    save_user_image,
    delete_profile_image,
    allowed_file,
    get_thumb_name,
    UPLOAD_DIR,
    ALLOWED_EXT,
)

# User CRUD Routes
@admin_bp.get('/user', endpoint='user')
def user():
    module = 'user'
    rows = get_all_users()
    return render_template('admin/user/user.html', users=rows, module=module)

@admin_bp.route('/user/add', methods=['GET', 'POST'], endpoint='add_user')
def add_user():
    if request.method == 'POST':
        return do_add_user()
    module = 'user_add'
    return render_template('admin/user/add.html', module=module)

@admin_bp.post('/user/add', endpoint='do_add_user')
def do_add_user():
    module = 'user_add'
    form = request.form
    username = (form.get('username') or '').strip()
    role = (form.get('role') or 'user').strip()
    password = generate_password_hash(form.get('password'))

    # Save the User row first (to get id)
    new_user = User(
        username=username,
        email=form.get('email'),
        password=password,
        role=role,
        profile=None
    )
    db.session.add(new_user)
    db.session.commit()

    # Call save_user_image with the new user id
    file = request.files.get("profile_image") or request.files.get("image")
    if file and file.filename:
        org_name = save_user_image(file, new_user.id, new_user.username, UPLOAD_DIR, ALLOWED_EXT)
        if org_name:
            new_user.profile = org_name
            db.session.commit()

    return redirect(url_for('admin_bp.user'))

@admin_bp.get('/user/edit/<int:user_id>', endpoint='edit_user')
def edit_user(user_id):
    module = 'user_edit'
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for('admin_bp.user'))

    return render_template('admin/user/edit.html', user=user, module=module)

@admin_bp.post('/user/edit', endpoint='do_edit_user')
def do_edit_user():
    module = 'user_edit'
    form = request.form
    user_id = form.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.username = (form.get('username') or user.username).strip()
        user.email = (form.get('email') or user.email).strip()
        user.role = (form.get('role') or user.role).strip()
        
        # Only update password if user typed something new
        password = form.get('password')
        if password and password.strip() != "":
            user.password = generate_password_hash(password)

        # Handle profile image update if provided
        file = request.files.get("profile_image") or request.files.get("image")
        if file and file.filename and allowed_file(file.filename, ALLOWED_EXT):
            delete_profile_image(user.profile)
            org_name = save_user_image(file, user.id, user.username, UPLOAD_DIR, ALLOWED_EXT)
            if org_name:
                user.profile = org_name

        db.session.commit()

        # Update session if current user edited their own profile
        if str(user.id) == str(session.get('user_id')):
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role
            session['user_role'] = user.role
            if user.profile:
                session['profile_image'] = f"images/user/{get_thumb_name(user.profile)}"
                session['profile'] = user.profile
            else:
                session['profile_image'] = "images/no-image.jpg"
                session['profile'] = None

    return redirect(url_for('admin_bp.user'))

@admin_bp.get('/user/confirm-delete/<int:user_id>', endpoint='confirm_delete_user')
def confirm_delete_user(user_id):
    module = 'user_delete'
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for('admin_bp.user'))

    return render_template('admin/user/confirm_delete.html', user=user, module=module)

@admin_bp.post('/user/delete', endpoint='delete_user')
def delete_user():
    form = request.form
    user_id = form.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('admin_bp.user'))

    delete_profile_image(user.profile)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_bp.user'))
