"""
views.py

URL route handlers

"""
import logging

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext import db, blobstore

from flask import render_template, flash, url_for, redirect, request, jsonify, make_response
from flask.views import MethodView
from werkzeug import secure_filename

#from models import ExampleModel
from decorators import login_required, admin_required, project_required
from forms import ExampleForm

from application import models

def media(project_id, event_id, media):
        e = models.Event.get_by_id(event_id)
        if e is None:
            return "not found", 404

        if media is not None:
            # return the media
            response = make_response(e.media.blob)
            response.headers['Content-Type'] = e.media.mimetype
            return response

class EventAPI(MethodView):

    decorators=[project_required]

    def get(self, project_id, event_id, project, media=None):
        if event_id is None:
            q = models.Event.all()
            q.filter("deleted = ", False)
            q.order(("-eventTime"))
            events = q.fetch(10)

            events_dict = { "events": [m.to_dict() for m in events]}
            return jsonify(events_dict)

        e = models.Event.get_by_id(event_id)
        if e is None:
            return "not found", 404

        # return the event json
        return jsonify({ "event": e.to_dict() })

    def post(self, project_id, project):

        # insert media
        m_list = []
        logging.info("adding media")

        for file in request.files.values():
            media = models.Media(mediaType="image",
                                 filename=secure_filename(file.filename),
                                 mimetype=file.content_type)
            file.seek(0)
            media.blob = db.Blob(file.read())
            #media.timestamp TODO: add file timestamp
            media.put()

            m_list.append(media.key().id_or_name())


        # add event and attach media

        e_form = request.form
        if len(m_list) == 0:
            return "no media", 400
        if 'stage' not in request.form:
            return "no stage", 400

        q = models.Stage.all()
        q.filter("name = ", request.form['stage'])
        stage = q.get()

        # TEMP TODO: make this it's own API
        # with some regard for process
        if stage is None:
            stage = models.Stage(name=request.form['stage'],
                                 activities = [])
            stage.put()

        media = models.Media.get_by_id(m_list[0])

        new_e = models.Event(project=project, 
                             stage=stage,
                             media=media)
        if 'notes' in request.form:
            new_e.notes = request.form['notes']
        new_e.put()

        return jsonify({ "event": new_e.key().id_or_name()})

class ProjectAPI(MethodView):

    def get(self, project_id):
        if project_id is None:
            q = models.Project.all()
            q.filter("deleted = ", False)
            q.order("-created")
            projects = q.fetch(10)

            p_list_dict = { "projects": [p.to_dict() for p in projects]}

            return jsonify(p_list_dict)

        p = models.Project.get_by_id(project_id)
        if p is None:
            return "not found", 404
        return jsonify(p.to_dict())

    def post(self):

        p_json = request.json
        if 'title' not in p_json.keys():
            return "error: malformed request", 400

        new_p = models.Project(title=p_json['title'])
        new_p.from_dict(p_json)
        new_p.put()

        return jsonify(new_p.to_dict())

    def put(self, project_id):

        p = models.Project.get_by_id(project_id)
        if p is None:
            return 404

        p_json = request.json
        if 'title' not in p_json.keys():
            return "error: malformed request", 400

        p.from_dict(p_json)
        p.put()

        return jsonify(p.to_dict())

    def delete(self, project_id):

        p = models.Project.get_by_id(project_id)

        if p is None:
            return 404
        p.deleted = True
        p.put()

        return 200

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

