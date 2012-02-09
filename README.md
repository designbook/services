*The design.book application web services, built using flask; deployed
using google app engine to api.designbook.in*

# design.book API Design

## Projects API

The server will allow the client to create a new project, including all
the metadata and resources related to it.

   POST api/v1/projects

   {
      "title": "sample title",
      "description": "project description",
      "media": "media-uri-or-blob",

      "process": "proces-name-or-id",

      "events": [

         {
            "name": "event-name",
            "notes": "user notes for the event",
            "add-time": "2011-01-02 13:23 GMT",

            "media": { }

            "activity": "activity-name-or-id",
            "stage": "stage-name-or-id",
         }

         {
            "name": "no-name",
            "notes": "chalkboard image of brainstorm",
            "add-time": "2011-01-03 13:23 GMT",

            "activity": "brainstorm",
            "stage": "IDEATE",

            "media": {

               "uri": "http://twitpic.com/JH65GVX",
               "type": "image",
            }
         }
      ]
   }

The server **WILL** validate the JSON and if project creation is
successful return a 201 with an *id* of the project created. The client
**SHOULD** make note of the *id* for the project.

   HTTP 201 CREATED

   {
      "id": 1           # we could also a REST id eg. "api/v1/projects/1"
   }

### Add event to existing project

   POST api/v1/projects/<id>/events

   {
      "name": "activity-6",
      "notes": "interview audio recording",
      "add-time": "2011-02-03 13:30 GMT",

      "activity": "interview",
      "stage": "DEFINE",

      "media": {

         "type": "audio",
         "mimetype": "audio/mpeg"
         "filename": "recording-3.mp3",

         "blob": ""
      }
   }

The client for ease of upload, **MAY** upload the actual media blob
seperately with the mimetype headers correctly set. The server will
**ONLY** retain the last media submitted. Currently *mutliple* media for
the same event are **NOT** allowed.

   POST api/v1/projects/<id>/events/<3>/media

# design.book models

For v1, all of the models will **NOT** be implemented by the server.
However, most of the models need to be implemented on the client for
*locally storing* application data. 

The server and client **WILL** implement the following models:

   - *project*
   - *event*
   - *media*

The client **WILL** implement the following models for local storage:

   - *process*
   - *activity*

## Project

   project {

      "id": 1,
      "title": "sample title",
      "description": "project description",
      "media": "media-uri-or-blob",

      "process": "proces-name-or-id",

      "events": [

         {
            "name": "event-name",
            "notes": "user notes for the event",
            "add-time": "2011-01-02 13:23 GMT",

            "media": { }

            "activity": "activity-name-or-id",
            "stage": "stage-name-or-id",
         }

         {
            "name": "no-name",
            "notes": "chalkboard image of brainstorm",
            "add-time": "2011-01-03 13:23 GMT",

            "activity": "brainstorm",
            "stage": "IDEATE",

            "media": {

               "uri": "http://twitpic.com/JH65GVX",
               "type": "image",
            }
         }
      ]
   }


## Process and Stages

   process {

      "id": 2,

      "title": "process name, ux design",
      "description": "abhishek invented this",

      "stages": [       # the order of stages is important

         {
            "name": "empathize",
            "description": "empathize damn it!",
            "img-uri": "http://cute-cats.jpg",

            "activities": ["brainstorming", "feeling", "compassion"]
         },
         {
            "name": "define",
            "description": "what are you doing??",
            "img-uri": "http://cute-cats.jpg",

            "activities": ["pointfication", "pen to paper"]
         },
         {
            "name": "ideate",
            "description": "think about it",
            "img-uri": "http://cute-cats.jpg"

            "activities": ["throw post-its", "doodle"]
         },
         {
            "name": "prototype",
            "description": "build some",
            "img-uri": "http://cute-cats.jpg",

            "activities": ["pointification", "model building"]
         },
         {
            "name": "test",
            "description": "break a leg",
            "img-uri": "http://cute-cats.jpg"

            "activities": ["monkey tests", "real world exposure"]
         }
      ]

   }

## Activities

For now, Activities must have unique names.

   activity {

      "name": "pointificate",
      "description": "sit with hand on chin",
      "img-uri": "http://people.pointificating.com"

   }

## Media

   media {

      "id": 121
      "type": "audio"|"video"|"img",
      "mimetype": "image/jpeg","audio/mpeg",

      "blob": RAW-DATA,
      "filename": "dsc0001.jpg",
      "timestamp":

      "uri": optional uri,

   }
