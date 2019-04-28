from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import Required, Email

class BlogForm(FlaskForm):
    title = StringField('Title', validators = [Required()])
    content = TextAreaField('Blog',validators = [Required()])
    photo = FileField('Select an image', validators= [Required()])
    category = SelectField('Category', choices = [('cuisine', 'Cuisine'),('voyage','Voyage'), ('health','Health'),('empower','Empowerment')], validators = [Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    firstname = StringField('First Name', validators = [Required()])
    lastname = StringField('Last Name', validators = [Required()])
    email = StringField('Email', validators = [Required(), Email()])
    comment = TextAreaField('Comment', validators = [Required()])
    submit = SubmitField('Post your Comment')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class SubscriberForm(FlaskForm):
    name  = StringField('Your name', validators = [Required()])
    email = StringField('Your email address', validators = [Required(), Email()])
    submit = SubmitField('Subscribe')
