from app import app, db
from app.models import User, Post

# Run your database operation within an application context
with app.app_context():
    # Your database operation here (e.g., adding data)
    new_user = User(username='TestUser', email='test@demo.com', password='password1')
    db.session.add(new_user)
    db.session.commit()
