#!/usr/local/bin/python
print "Content-type: text/html\n"

import suggestor

try:
  for line in open('nll.html'):
    if line.find('__INSERT__') > 0:
      suggestor.process_suggestions()
    elif line.find('__INSERT_PAST__') > 0:
      suggestor.process_past_readings()
    else:
      print line
except:
  pass
