from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . import main
from .forms import CommentForm, UpdateProfile, BlogForm, SubscriberForm
from ..models import Blog, Comment, User, Subscriber
from .. import db, photos
from ..email import mail_message


@main.route('/')
def index():
    all_blogs = Blog.query.order_by(Blog.posted.desc()).all()
    title = 'Welcome to my blog'

    return render_template('index.html', title = title, all_blogs = all_blogs)

@main.route('/post/<post_id>', methods=['GET','POST'])
def post(post_id):
    form  = CommentForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        comment = form.comment.data
        new_user = User(firstname = firstname, lastname = lastname, email = email)
        new_comment = Comment(comment = comment, user = new_user, blog_id = post_id)

        db.session.add(new_user)
        db.session.commit()
        new_comment.save_comment()

        return redirect(url_for('main.post', post_id = post_id))


    post = Blog.get_blog(post_id)
    comments = Comment.get_comments(post_id)
    title = 'a post'

    return render_template('post.html', title = title, post = post, comments = comments, comment_form = form)

@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'

        new_blog = Blog(post_title = title, post_content = content, photo_path = path, category = category, user = current_user)
        new_blog.save_blog()

        subscriber = Subscriber.query.all()
        for email in subscriber:
            mail_message("New Blog Post from Kasyoki Blog! ","email/postnotification",email.email,subscriber=subscriber)
            
        return redirect(url_for('main.index'))

       
    title = 'New Blog'
    return render_template('new_blog.html', title = title, blog_form = form)


@main.route('/blogger/<user_id>')
def profile(user_id):
    user = User.query.filter_by(id = user_id).first()

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user = user)

@main.route('/blogger/<user_id>/update', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',user_id =user.id))

    return render_template('profile/update.html',form =form)

@main.route('/blogger/<user_id>/update/pic',methods= ['POST'])
@login_required
def update_pic(user_id):
    user = User.query.filter_by(id = user_id).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',user_id=user_id))

@main.route('/subscribe', methods=['GET','POST'])
def subscriber():
    subscriber_form = SubscriberForm()
    blogs = Blog.query.order_by(Blog.posted.desc()).all()

    if subscriber_form.validate_on_submit():
        subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)

        db.session.add(subscriber)
        db.session.commit()

        mail_message("Welcome to Kasyoki Blog","email/welcome_subscriber",subscriber.email,subscriber=subscriber)

        title= "BumbleBee"
        return render_template('index.html',title=title, blogs=blogs)

    subscriber = Blog.query.all()

    blogs = Blog.query.all()


    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blogs)