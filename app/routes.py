from flask import render_template, flash, redirect, url_for, request, abort
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def hello_world():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            flash('Passwords match!', 'success')
            
            hashed_pass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user = User(username=request.form['username'], email=request.form['email'],password=hashed_pass)
            
            confirm_user = User.query.filter_by(username=request.form['username']).first()
            confirm_email = User.query.filter_by(email=request.form['email']).first()
            if confirm_user:
                flash("Username Already exists. Try a different username!",'danger')
            if confirm_email:
                flash("Email Already exists. Try a different email!",'danger')
                return render_template('register.html')
            else:
                db.session.add(user)
                db.session.commit()

            
            flash('Account created successfully. Please Login.', 'success')
            return redirect(url_for('login'))
        
        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        confirm_email = User.query.filter_by(email=email).first()
        #hash_entered_password = bcrypt.generate_password_hash(password).decode('utf-8')

        verify_password = bcrypt.check_password_hash(confirm_email.password, password)

        if confirm_email and verify_password:
            login_user(confirm_email)
            flash(f'Username: {confirm_email.username} has been successfully logged in!', 'success')
            return redirect(url_for('hello_world'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello_world'))

@app.route('/profile')
@login_required
def profile():
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template('profile.html', profile_image=profile_image)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/updateprofile')
@login_required
def updateprofile():
    return render_template('updateprofile.html')

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'], author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('hello_world'))
    return render_template('newpost.html',h2text='New Post')

@app.route('/post/<int:post_id>')
def post_modify(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('postmodify.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('hello_world'))