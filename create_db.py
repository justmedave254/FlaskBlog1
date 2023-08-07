# create_db.py

from app import app, db

# Run the application context
with app.app_context():
    # Create the database tables
    db.create_all()
