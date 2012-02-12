"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views

# REST API helper from flask.pocco.org docs

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

app.add_url_rule('/upload', 'upload', view_func=views.upload)

# Add new example via web form
app.add_url_rule('/example/new', 'new_example', view_func=views.new_example, methods=['GET', 'POST'])

# Contrived admin-only view example
app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# design.book API routes

register_api(views.ProjectAPI, 'project_api', '/projects/', pk='project_id')




## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

