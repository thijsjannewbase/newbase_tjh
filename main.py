#!/usr/bin/env python
#

import webapp2
import json
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import logging


def getDb():
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        # Connecting from App Engine
        db = MySQLdb.connect(
            unix_socket='/cloudsql/newbase-thijsjan:db',
            user='root',
            db='Newbase')

    else:
        db = MySQLdb.connect(
            host='173.194.228.208',
            port=3306,
            user='root',
            passwd='diskette9911',
            db='Newbase')
        return db


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # for now direct SQL queries, in the future use django as ORM
        db = getDb();
        cursor = db.cursor()
        cursor.execute('SELECT * from projects')
        response = json.dumps(cursor.fetchall())

        logging.info('returning: ' + response)

        self.response.content_type = 'text/json'
        self.response.write(response)
        # other response stuff? https://webapp-improved.appspot.com/guide/response.html

    def post(self):
        id = self.request.get('id')
        name = self.request.get('name')
        logging.info('Inserting project named ' + name + ' with id '+ str(id))

        db = getDb();
        cursor = db.cursor()
        cursor.execute('INSERT INTO projects (id, name) VALUES (%s, %s)', [id, name])
        db.commit()
        db.close()

        self.redirect("/")

    def put(self):
        name = self.request.get('name')
        id = int(self.request.get('id'))
        logging.info('updating project with ID ' + str(id) + ' with name ' + name)

        db = getDb();
        cursor = db.cursor()
        result = cursor.execute('UPDATE projects set name = %s where id = %s', [name, id])
        db.commit()
        db.close()
        if result == 0:
            self.response.write('could not update')
            self.response.set_status(404)
        else:
            self.response.write(result)


# webapp2: https://webapp-improved.appspot.com/index.html
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)