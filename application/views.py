"""
views.py

URL route handlers

"""

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect, request
from flask.views import MethodView

#from models import ExampleModel
from decorators import login_required, admin_required
from forms import ExampleForm

class ProjectAPI(MethodView):

    def get(self, project_id):
        if project_id is None:
            return "All Projects"

        return "Project {id}".format(id=project_id)

    def post(self):

       project_json = request.json

       project_json['id'] = 1
       return project_json


    def put(self, project_id):
        pass

    def delete(self, project_id):
        pass


def upload():
    """ Upload file using flask api - requests.files"""
    pass


@login_required
def new_example():
    """Add a new example, detecting whether or not App Engine is in read-only mode."""
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
                    example_id = form.example_id.data,
                    example_title = form.example_title.data,
                    added_by = users.get_current_user()
                    )
        try:
            example.put()
            flash(u'Example successfully saved.', 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'failure')
            return redirect(url_for('list_examples'))
    return render_template('new_example.html', form=form)


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

