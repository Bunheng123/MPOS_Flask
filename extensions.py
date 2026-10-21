from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

db = SQLAlchemy() #
migrate = Migrate() # working on migrating

limiter = Limiter(
    key_func=get_remote_address, # get user's public ip
    default_limits=["10000 per day", "100 per minute"]
)

csrf = CSRFProtect()

cors = CORS()
