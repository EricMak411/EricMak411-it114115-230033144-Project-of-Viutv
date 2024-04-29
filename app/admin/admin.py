from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, redirect, url_for
from flask_login import current_user

from app.models import Video
from app import db

# Create an admin blueprint with the '/admin' URL prefix
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def init_admin():
    # Customized admin index view
    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            # Only accessible for admin users
            return current_user.is_authenticated and current_user.is_admin()

        def inaccessible_callback(self, name, **kwargs):
            # Redirect non-admin users to the home page
            return redirect(url_for('routes.index'))

    # Create admin instance
    admin = Admin(name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

    # Add model views to admin
    class VideoModelView(ModelView):
        column_list = ('title', 'description', 'user_id')  # Adjust columns as needed
        column_searchable_list = ('title', 'description')  # Enable search
        column_filters = ('user_id',)  # Enable filtering

    admin.add_view(VideoModelView(Video, db.session))

    # Return the admin blueprint and admin instance
    return admin_bp, admin
