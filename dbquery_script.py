from app import app, db
from app.models import User, Post

# Run your database operation within an application context
with app.app_context():
    #one = User.query.first()
    #print(one)
    #print(one.password)

    '''username = 'David'
    user = User.query.filter_by(username=username).first()
    print(user.email)
    print(user.password)
    print(user)'''

    confirm_email = User.query.filter_by(email='okellodavid002@gmail.com').first()

    print(confirm_email)
    print(confirm_email.password)
    print(confirm_email.username)