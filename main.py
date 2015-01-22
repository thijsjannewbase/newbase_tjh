#!/usr/bin/env python
#

import webapp2
import jinja2
import json
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+ "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
        # logging.info(prjs)


        self.response.content_type = 'text/html'


        template = JINJA_ENVIRONMENT.get_template('master.html')
        self.response.write(template.render())

    def post(self):
        id = self.request.get('id')
        name = self.request.get('name')
        logging.info('Inserting project named ' + name + ' with id ' + str(id))

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

    def getDbInfo(self):
        # for now direct SQL queries, in the future use django as ORM
        db = getDb();
        cursor = db.cursor()
        result=cursor.execute('SELECT database()')
        response = json.dumps(cursor.fetchall())

        logging.info('returning: ' + response)

        self.response.content_type = 'text/plain'
        self.response.write(response + '\n')
        return response


class Del(webapp2.RequestHandler):
    def delete(self, id):
        db = getDb();
        cursor = db.cursor()
        result = cursor.execute('DELETE from projects where id = %s', [id])
        db.commit()
        db.close()
        if result == 0:
            self.response.write('could not delete')
            self.response.set_status(404)
        else:
            self.response.write(result)  # webapp2: https://webapp-improved.appspot.com/index.html

class ang_form(webapp2.RequestHandler):
    def get(self):
        db = getDb();
        cursor = db.cursor()
        prjs=cursor.execute('SELECT * from projects')
        # cursor.execute('SELECT database()')
        projects=cursor.fetchall()
        result = [{'id':rec[0], 'name': rec[1]} for rec in projects]
        print result
        self.response.content_type='text/json'
        self.response.write(json.dumps(result))


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/del/(\d+)', Del),
                                  ('/ang_form', ang_form)
                              ], debug=True)