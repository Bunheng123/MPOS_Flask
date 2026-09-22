import os
from PIL import Image
from werkzeug.utils import secure_filename
from config import Config

UPLOAD_DIR = Config.UPLOAD_DIR
ALLOWED_EXT = Config.ALLOWED_EXTENSIONS

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename, allowed_extensions=ALLOWED_EXT):
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in allowed_extensions

def generate_image_names(user_id, username, ext):
    clean_uname = secure_filename(username)
    if not clean_uname:
        clean_uname = f"user_{user_id}"
    ext = ext.lower()
    org_name = f"{user_id}_org_{clean_uname}.{ext}"
    thumb_name = f"{user_id}_thumb_{clean_uname}.{ext}"
    return org_name, thumb_name

def save_user_image(file, user_id, username, upload_folder=UPLOAD_DIR, allowed_extensions=ALLOWED_EXT, thumb_size=(200, 200)):
    if not file or file.filename == '':
        return None
    if not allowed_file(file.filename, allowed_extensions):
        return None

    ext = file.filename.rsplit('.', 1)[1].lower()
    org_name, thumb_name = generate_image_names(user_id, username, ext)
    org_path = os.path.join(upload_folder, org_name)
    thumb_path = os.path.join(upload_folder, thumb_name)

    file.save(org_path)

    image = Image.open(org_path)
    if ext in ("jpg", "jpeg") and image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    thumb = image.copy()
    thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)

    save_kwargs = {"optimize": True}
    if ext in ("jpg", "jpeg"):
        save_kwargs["quality"] = 80

    thumb.save(thumb_path, **save_kwargs)

    return org_name

def get_thumb_name(profile_filename):
    if not profile_filename:
        return None
    return profile_filename.replace("_org_", "_thumb_")

def delete_profile_image(filename, upload_folder=UPLOAD_DIR):
    if filename and filename != "no-image.jpg":
        org_path = os.path.join(upload_folder, filename)
        thumb_name = get_thumb_name(filename)
        thumb_path = os.path.join(upload_folder, thumb_name) if thumb_name else None
        for p in (org_path, thumb_path):
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
