from app import app, db
from app.models import User, Post

# Run your database operation within an application context
with app.app_context():
    one = User.query.first()
    post_1 = Post(title='First db post', content='First post added to db', user_id=one.id)
    db.session.add(post_1)
    db.session.commit()

    p = one.posts
    print(p)
