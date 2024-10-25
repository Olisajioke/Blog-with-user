from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


#form classes

class CreatePostForm(FlaskForm):
    """Form for users to create a new blog post"""
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    img_url = StringField('Image URL[search google for it, right click and copy😉]', validators=[DataRequired()])
    
    # Genre select field with a variety of genres for both blog posts and movie reviews
    genre = SelectField('Genre [Select One]', 
                        choices=[
                            ('None', 'Select Genre'),
                            ('Blogpost', 'Blogpost'),
                            ('Romance', 'Romance'),
                            ('Horror', 'Horror'),
                            ('Science Fiction', 'Science Fiction'),
                            ('Action', 'Action'),
                            ('Comedy', 'Comedy'),
                            ('Drama', 'Drama'),
                            ('Fantasy', 'Fantasy'),
                            ('Mystery', 'Mystery'),
                            ('Thriller', 'Thriller'),
                            ('Adventure', 'Adventure'),
                            ('Documentary', 'Documentary'),
                            ('Biography', 'Biography'),
                            ('History', 'History'),
                            ('Animation', 'Animation'),
                            ('Crime', 'Crime'),
                            ('Family', 'Family'),
                            ('Music', 'Music'),
                            ('War', 'War'),
                            ('Western', 'Western'),
                            ('Novel', 'Novel'),
                            ('Non-fiction', 'Non-fiction'),
                            ('Poetry', 'Poetry'),  # Added comma here
                            ('Short Story/fiction', 'Short Story/fiction')  # Added comma here
                        ], 
                        validators=[DataRequired()],
                        default='Blogpost')  # Default set to 'None' so users must select a genre
    
    rating = SelectField('Rating', 
                         choices=[(str(i), f'{i} stars') for i in range(11)], 
                         validators=[DataRequired()],
                         default='0')
    
    duration = StringField('Duration', validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField('Submit')




class RegisterForm(FlaskForm):
    """Form for users to create an account"""
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    """Form for users to log in"""
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    """Form for users to add comments"""
    comment = CKEditorField("Leave a Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

class EditProfileForm(FlaskForm):
    """Form for users to edit their profile"""
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class SearchForm(FlaskForm):
    """Form for users to search for posts"""
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")

class SearchGenre(FlaskForm):
    """Form for users to search for posts by genre"""
    genre = SelectField('Genre [Select One]', 
                        choices=[
                            ('None', 'Select Genre'),
                            ('Blogpost', 'Blogpost'),
                            ('Romance', 'Romance'),
                            ('Horror', 'Horror'),
                            ('Science Fiction', 'Science Fiction'),
                            ('Action', 'Action'),
                            ('Comedy', 'Comedy'),
                            ('Drama', 'Drama'),
                            ('Fantasy', 'Fantasy'),
                            ('Mystery', 'Mystery'),
                            ('Thriller', 'Thriller'),
                            ('Adventure', 'Adventure'),
                            ('Documentary', 'Documentary'),
                            ('Biography', 'Biography'),
                            ('History', 'History'),
                            ('Animation', 'Animation'),
                            ('Crime', 'Crime'),
                            ('Family', 'Family'),
                            ('Music', 'Music'),
                            ('War', 'War'),
                            ('Western', 'Western'),
                            ('Novel', 'Novel'),
                            ('Non-fiction', 'Non-fiction'),
                            ('Poetry', 'Poetry'),  # Added comma here
                            ('Short Story/fiction', 'Short Story/fiction')  # Added comma here
                        ], 
                        validators=[DataRequired()],
                        default='Blogpost')  # Default set to 'None' so users must select a genre
    submit = SubmitField("Search")



class DeleteProfileForm(FlaskForm):
    """Form for users to delete their account"""
    submit = SubmitField('Delete', validators=[DataRequired()])