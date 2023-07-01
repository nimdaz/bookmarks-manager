from config import db, app
import route

with app.app_context():
    db.create_all()
