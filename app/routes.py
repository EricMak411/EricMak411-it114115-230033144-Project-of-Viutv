from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from .models import Video
from .forms import VideoUploadForm
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template("index.html", title="Home Page")

@bp.route("/dashboard")
def dashboard():
    # Query videos uploaded by the current user (if logged in)
    if current_user.is_authenticated:
        videos = Video.query.filter_by(user_id=current_user.id).order_by(Video.modified_time.desc()).all()
        return render_template("dashboard.html", title="Dashboard", videos=videos)
    else:
        return redirect(url_for('routes.index'))

@bp.route("/logout")
def logout():
    # Implement logout logic here if needed
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.index'))

@bp.route("/upload", methods=['GET', 'POST'])
def upload():
    form = VideoUploadForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # Save the uploaded video to the database
            video = Video(title=form.title.data,
                          description=form.description.data,
                          user_id=current_user.id)  
            db.session.add(video)
            db.session.commit()
            flash('Video uploaded successfully!', 'success')
            return redirect(url_for('routes.dashboard'))  
        else:
            flash('Please log in to upload videos.', 'info')
            return redirect(url_for('routes.login'))  
    return render_template("upload.html", title="Upload Video", form=form)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    # Instantiate the VideoUploadForm
    form = VideoUploadForm()
    # Registration logic
    return render_template("register.html", title="Register", form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    # Instantiate the VideoUploadForm
    form = VideoUploadForm()
    # Login logic
    return render_template("login.html", title="Login", form=form)
