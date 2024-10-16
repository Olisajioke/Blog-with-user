from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages,request, session
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from forms import CreatePostForm, RegisterForm, LoginForm
from flask_migrate import Migrate
from datetime import datetime
from flask_principal import Identity, AnonymousIdentity, identity_changed
from functools import wraps


#create a new flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#gravatar
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)



#Define roles
ROLES = {
    1: 'admin',  # Admin user
    3: 'editor',  # Editor user
    # Add more roles as needed, i will need this later
}

##CONFIGURE TABLES

class BlogPost(db.Model):
    """Create a BlogPost table"""
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = relationship("User", back_populates="posts")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #relationship to the User table
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="post")  # Relationship to comments


class User(UserMixin, db.Model):
    """Create A user Table"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")  # Relationship to comments



class Comment(db.Model):
    """Create a comment table"""
    __tablename__ = "comments"  # Table name
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="comments")  # Relationship to users
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)  # ForeignKey to BlogPost
    post = relationship("BlogPost", back_populates="comments")  # Relationship to BlogPost
    date = db.Column(db.String(250), nullable=False, default=datetime.now().strftime("%B %d, %Y"))

# Decorator to restrict file deletion to admin users (ID 1)
def confirm_admin(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        year = datetime.now().year
        #print(f"Current User ID: {current_user.id}") # Print current user ID
        if current_user.id not in (1, 3):  # Block users who are not admin (ID 1)
            return render_template('403.html', year=year)  # Return forbidden page
        return func(*args, **kwargs)  # Admin can proceed
    return wrapper_func



# Decorator to prevent diting by non-adminusers
def confirm_edit(func):
    @wraps(func)
    def wrapper_edit_func(*args, **kwargs):
        year = datetime.now().year
        #print(f"Current User ID: {current_user.id}") # Debugging
        if current_user.id not in (1, 3):  # Block users who are not admin (ID 1)
            return render_template('403.html', year=year)  # Return forbidden page
        return func(*args, **kwargs)  # Admin can proceed
    return wrapper_edit_func


#Decorator to prevent adding posts by non-admin users
def confirm_add(func):
    @wraps(func)
    def wrapper_add_func(*args, **kwargs):
        year = datetime.now().year
        #print(f"Current User ID: {current_user.id}") 
        if not current_user.is_authenticated:
            return redirect(url_for('login')) 
        if current_user.id not in (1, 3):  # Block users who are not admin (ID 1)
            return render_template('403.html', year=year)  # Return forbidden page
        return func(*args, **kwargs)  # Admin can proceed
    return wrapper_add_func


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    year = datetime.now().year
    users = User.query.all()
    return render_template("index.html", all_posts=posts, year=year, users=users)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['POST', 'GET'])
def register():
    year = datetime.now().year
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        if form.password.data != form.confirm_password.data:
            flash("Passwords don't match, please try again.")
            return redirect(url_for('register'))
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8),
            name=(form.name.data).title()
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('login'))
    return render_template("register.html", form=form, year=year)


@app.route('/login', methods=['POST', 'GET'])
def login():
    year = datetime.now().year
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        print(email, password)
        user = User.query.filter_by(email=email).first()
        if not user:
            flash(f'{email} does not exist in our database, please try again or register.')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        print(current_user.email)
        
        login_user(user)
        #print(f"Current User ID: {current_user.id}")
        #print(f"Is Authenticated: {current_user.is_authenticated}")

        return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, year=year)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    print(app.url_map)
    return redirect(url_for('get_all_posts'))

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    # Check if post_id is provided as a query parameter (from another route)
    retrieved_post = request.args.get('post_id')
    if retrieved_post:
        post_id = retrieved_post  # If query parameter exists, use it

    # Get the post using post_id (whether from URL or query parameter)
    requested_post = db.session.get(BlogPost, post_id)

    # Handle comment submission
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))

        if form.validate_on_submit():
            new_comment = Comment(
                text=form.comment.data,
                author=current_user,
                post_id=post_id,
                date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment added successfully!")
            return redirect(url_for('show_post', post_id=post_id))

    year = datetime.now().year
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    
    return render_template("post.html", post=requested_post, year=year, form=form, comments=comments)


@app.route("/about")
def about():
    year = datetime.now().year
    return render_template("about.html", year=year)


@app.route("/contact")
def contact():
    year = datetime.now().year
    return render_template("contact.html", year=year)


@app.route("/new-post", methods=["GET", "POST"])
@login_required
@confirm_add
def add_new_post():
    year = datetime.now().year
    form = CreatePostForm()
    if request.method == 'POST':
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, year=year)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@confirm_edit
def edit_post(post_id):
    year = datetime.now().year
    #post = BlogPost.query.get(post_id)
    post = db.session.get(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = post.author
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, year=year)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
@confirm_admin
def delete_post(post_id):
    #post_to_delete = BlogPost.query.get(post_id)
    post_to_delete = db.session.get(BlogPost, post_id)
    flash(f"Post {post_to_delete.title} has been deleted.")
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


#delete comment
@app.route("/delete-comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    comment_to_delete = db.session.get(Comment, comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    comment_id = comment_to_delete.post_id
    return redirect(url_for('show_post', post_id=comment_id))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
