from flask import render_template, session, redirect, url_for
from admin import admin_bp

@admin_bp.get('/dashboard', endpoint='dashboard')
@admin_bp.get('/', endpoint='dashboard_root')
def dashboard():
    module = 'dashboard'

    if not session.get('is_login'):
        return redirect(url_for('admin_bp.login'))

    return render_template('admin/dashboard/dashboard.html', module=module)