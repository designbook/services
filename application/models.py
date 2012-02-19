"""
models.py

design.book datastore models

"""

from google.appengine.ext import db

class Model(db.Model):

    def to_dict(self):
        self_dict = dict([(p, unicode(getattr(self, p))) for p in self.fields().keys()])
        self_dict['id'] = self.key().id_or_name()

        return self_dict

    def from_dict(self, src_dict):
        for p in self.properties():
            if p in src_dict:
                setattr(self, p, src_dict[p])

class Process(Model):
    """Processes with stages and activities"""
    title = db.StringProperty(required=True)

class Stage(Model):
    """Stage name and list of activities"""
    name = db.StringProperty(required=True)
    activities = db.StringListProperty(required=True)
    process = db.ReferenceProperty(Process, collection_name='stages')

class Project(Model):
    """Project information"""
    title = db.StringProperty(required=True)
    description = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    media = db.StringListProperty() # media keys
    process = db.ReferenceProperty(Process)
    deleted = db.BooleanProperty(default=False)

class Media(Model):
    mediaType = db.StringProperty(required=True, choices=("audio","video","image"))
    mimetype = db.StringProperty(required=True)
    blob = db.BlobProperty()
    filename = db.StringProperty()
    timestamp = db.DateTimeProperty() #From the image file
    uri = db.LinkProperty()

class Event(Model):
    project = db.ReferenceProperty(Project, collection_name='events', required=True)
    notes = db.TextProperty()
    eventTime = db.DateTimeProperty() #Time of media creation (not upload time)
    media = db.ReferenceProperty(Media, collection_name='media')
    activity = db.StringProperty()
    stage = db.ReferenceProperty(Stage, required=True)
    deleted = db.BooleanProperty(default=False)

#Test cases
"""
#Delete all entities
db.delete(Process.all().fetch(1000))
db.delete(Stage.all().fetch(1000))
db.delete(Project.all().fetch(1000))
db.delete(Media.all().fetch(1000))
db.delete(Event.all().fetch(1000))

process = Process(title="dschool process")
process.put()

stage1 = Stage(name="ideate", activities=["eat","sleep"], process = process)
stage1.put()

project = Project(title="new project", description="blah blha", media="http://www.google.com/images", process=process)

project.put()

blob = db.ByteString("testblob")

media = Media(mediaType="image", mimetype="image/jpeg", blob=blob, fileName="nav.png", uri="http://www.test.com")
media.put()

event1 = Event(project=project, notes="awesome notes", media=media, activity="eat", stage=stage1)
event1.put()
"""
