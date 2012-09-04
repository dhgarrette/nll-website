#!/usr/local/bin/python

import cgi
import os

import suggestor


#print cgi.escape(os.environ["REMOTE_ADDR"])

form = cgi.FieldStorage()
vote = form.getvalue('vote')
id = form.getvalue('id')

suggestor.record_vote(vote, id)

print 'Content-type: text/html'
print 'Location: ../nll/'
print ''
