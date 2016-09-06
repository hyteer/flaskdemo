# encoding:utf-8
from flask import render_template,request,flash,redirect,url_for,make_response
from . import main
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import Permission, current_app, User, Post, db, Comment
from .forms import PostForm, CommentForm
#from PIL import Image
import os,hashlib
from werkzeug.utils import secure_filename



@main.route('/', methods=['GET','POST'])
def index():
    form = PostForm()
    #import pdb; pdb.set_trace()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        print "Comes here..."
        #import pdb; pdb.set_trace()
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page =  request.args.get('page',1,type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,show_followed=show_followed,pagination=pagination)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() -1) / current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        about(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)

@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))



@main.route('/res/<filename>')
def static_res(filename):
    print "[Resource file]:",filename
    app = current_app._get_current_object()
    return redirect(url_for('static',filename="avatar/male.jpg"))

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect('main.index')
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('user.user_home', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('user.user_home', username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.index'))
    if not current_user.is_following(username):
        flash('You are not following this user.')
        return redirect(url_for('user.user_home', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('user.user_home', username=username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)




@main.route('/about')
def about():
    return render_template('about.html')


################################ Test #####################################

allowed_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
folder_upload = '/Users/myusername/Documents/Project_Upload/'

#### Methods ####
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions


#### Routes ####
@main.route('/edit-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    app = current_app._get_current_object()
    if request.method == 'POST':
        file = request.files['file']
        file_ext = file.filename.rsplit('.', 1)[1]
        print "file extension:",file_ext
        #size = (40, 40)
        #im = Image.open(file)
        #im.thumbnail(size)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename__hash = hashlib.md5(current_user.email.encode('utf-8')).hexdigest()

            file.save(os.path.join(app.config['AVATAR_FOLDER'], filename__hash+'.'+ file_ext))

            #current_user.new_avatar_file = url_for('main.static', filename='%s/%s' % ('avatar', filename))
            #current_user.is_avatar_default = False
            flash(u'头像保存成功')
            #return redirect(url_for('.user', username=current_user.username))
    return render_template('test/change_avatar.html')



from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from flask_wtf import Form as FlaskForm
from wtforms import SubmitField



class PhotoForm(FlaskForm):
    photo = FileField('Your photo')
    submit = SubmitField('Submit')
@main.route('/upload/', methods=('GET', 'POST'))
def upload():
    app = current_app._get_current_object()
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(app.config['UPLOAD_PATH'] + filename)
        flash("File:{filename} uploaded.".format(filename=filename))
    else:
        filename = None

    return render_template('test/upload.html', form=form, filename=filename)
