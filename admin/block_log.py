from flask import render_template, request, redirect, url_for, flash
from admin import admin_bp
from extensions import db
from models.block_log import BlockLog
from sqlalchemy import func

@admin_bp.get('/block-logs', endpoint='block_logs')
def block_logs():
    module = 'block_logs'
    search = request.args.get('search', '').strip()

    query = BlockLog.query
    if search:
        query = query.filter(
            (BlockLog.ip.ilike(f"%{search}%")) |
            (BlockLog.endpoint.ilike(f"%{search}%")) |
            (BlockLog.methods.ilike(f"%{search}%")) |
            (BlockLog.device.ilike(f"%{search}%"))
        )

    logs = query.order_by(BlockLog.id.desc()).all()

    # Calculate summary metrics
    total_blocks = BlockLog.query.count()
    unique_ips = db.session.query(func.count(func.distinct(BlockLog.ip))).scalar() or 0
    
    # Most targeted endpoint
    top_endpoint_row = db.session.query(
        BlockLog.endpoint, func.count(BlockLog.id).label('count')
    ).group_by(BlockLog.endpoint).order_by(func.count(BlockLog.id).desc()).first()
    top_endpoint = top_endpoint_row[0] if top_endpoint_row else 'None'

    return render_template(
        'admin/block_log/block_log.html',
        logs=logs,
        module=module,
        total_blocks=total_blocks,
        unique_ips=unique_ips,
        top_endpoint=top_endpoint,
        search=search
    )

@admin_bp.post('/block-logs/clear', endpoint='clear_block_logs')
def clear_block_logs():
    try:
        BlockLog.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[BlockLog Clear Error]: {e}")
    return redirect(url_for('admin_bp.block_logs'))

@admin_bp.post('/block-logs/delete/<int:log_id>', endpoint='delete_block_log')
def delete_block_log(log_id):
    log_item = BlockLog.query.get(log_id)
    if log_item:
        try:
            db.session.delete(log_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[BlockLog Delete Error]: {e}")
    return redirect(url_for('admin_bp.block_logs'))
