# encoding:utf-8
from flask import render_template,request,flash,redirect,url_for
from . import main
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import Permission,current_app
#from PIL import Image
import os,hashlib
from werkzeug.utils import secure_filename





@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/mod')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

@main.route('/res/<filename>')
def static_res(filename):
    print "[Resource file]:",filename
    app = current_app._get_current_object()
    return redirect(url_for('static',filename="avatar/male.jpg"))




@main.route('/about')
def about():
    return render_template('about.html')

#@main.route('/')

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
