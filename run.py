from app.app_factory import create_app, db
from app.libs.ip_utils import insert_data
import os

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/config.ini")
app = create_app(config_path)


@app.cli.command("create_db")
def create_database():
    db.app = app
    db.create_all()
    insert_data()
