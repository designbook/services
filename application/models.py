"""
models.py

App Engine datastore models

"""

from google.appengine.ext import db
	
class Process(db.Model):
    """Processes with stages and activities"""
    title = db.StringProperty(required=True)
	
class Stage(db.Model):
	"""Stage name and list of activities"""
	name = db.StringProperty(required=True)
	activities = db.StringListProperty(required=True)
	process = db.ReferenceProperty(Process, collection_name='stages')
		
class Project(db.Model):
	"""Project information"""
	title = db.StringProperty(required=True)
	description = db.StringProperty()
	media = db.LinkProperty() #Should this be a blobProperty? may be even a media item?
	process = db.ReferenceProperty(Process)
	
class Media(db.Model):
	mediaType = db.StringProperty(required=True, choices=("audio","video","image"))
	mimetype = db.StringProperty(required=True, choices=("image/jpeg","audio/mpeg"))
	blob = db.BlobProperty()
	filename = db.StringProperty()
	timestamp = db.DateTimeProperty() #From the image file
	uri = db.LinkProperty()

class Event(db.Model):
	project = db.ReferenceProperty(Project, collection_name='events', required=True)
	notes = db.TextProperty()
	eventTime = db.DateTimeProperty() #Time of media creation (not upload time)
	media = db.ReferenceProperty(Media, required=True)
	activity = db.StringProperty()
	stage = db.ReferenceProperty(Stage, required=True)
	
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