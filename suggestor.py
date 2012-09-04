#!/usr/local/bin/python

SUGGESTION_FILE = 'suggestions.txt'

TOP_FMT = """\
<tr>
  <td class="rank">%d.</td>
  <td class="vote">
    <form method="post" action="vote.cgi">
      <input class="voteup" type="image" class="vote" src="img/up.png" alt="vote up" />
      <input name="vote" value="up" type="hidden" />
      <input name="id" value="%s" type="hidden" />
    </form><br>
    <form method="post" action="vote.cgi">
      <input class="votedown" type="image" class="vote" src="img/down.png" alt="vote down" />
      <input name="vote" value="down" type="hidden" />
      <input name="id" value="%s" type="hidden" />
    </form>
  </td>
"""

TOP_PAST_FMT = """\
<tr>
"""

ACM_FMT = '<a href="%s"><nobr>(acm portal)</nobr></a>'
HTML_FMT = '<a href="%s">(html)</a>'
PDF_FMT = '<a href="%s">(pdf)</a>'
TXT_FMT = '%s'
URL_FMT = '<a href="%s">(url)</a>'

BOTTOM_FMT = """\
  <td>
    <span class="authors">%s</span>.
    <span class="title">%s</span>.
    <span class="venue">%s</span>,
    <span class="year">%d</span>
    %s
    <br>
    <span class="upvotes">(%d points: %d up, %d down)</span>
  </td>
</tr>
"""

SUGGEST_FMT = '%d:::%d:::%s:::%s:::%s:::%s:::%d:::%d\n'

import cgi
import cgitb; cgitb.enable()  # for troubleshooting


class Suggestion(object):
  def __init__(self):
    self.upvotes = -1
    self.downvotes = -1
    self.authors = None
    self.year = -1
    self.title = None
    self.url = None
    self.venue = None
    self.past = 0

  def __cmp__(self, other):
    if cmp(self.upvotes - self.downvotes, other.upvotes - other.downvotes) == 0:
      return cmp(self.year, other.year)
    else:
      return cmp(self.upvotes - self.downvotes, other.upvotes - other.downvotes)

  def __str__(self):
    return SUGGEST_FMT % (self.upvotes, self.downvotes, self.authors, self.url, self.title, self.venue, self.year, self.past)


def read_suggestions():
  suggestions = []
  for line in open(SUGGESTION_FILE):
    parts = line.split(':::')

    if len(parts) != 8:
      print "Invalid suggestion: %s" % line
    else:
      try:
        suggestion = Suggestion()
        suggestion.upvotes = int(parts[0])
        suggestion.downvotes = int(parts[1])
        suggestion.authors = parts[2]
        suggestion.url = parts[3]
        suggestion.title = parts[4]
        suggestion.venue = parts[5]
        suggestion.year = int(parts[6])
        suggestion.past = int(parts[7])
      except TypeError:
        print "Invalid suggestion " + line
    
      suggestions.append(suggestion)

  return suggestions

def write_suggestions(suggestions):
  f = open(SUGGESTION_FILE, 'w')

  for s in suggestions:
    f.write(str(s))

def get_link(s):
  if s.url.find('.pdf') > 0:
    return PDF_FMT % (s.url)
  elif s.url.find('.html') > 0:
    return HTML_FMT % (s.url)
  elif s.url.find('portal.acm') > 0:
    return ACM_FMT % (s.url)
  elif s.url.find('http') >= 0:
    return URL_FMT % (s.url)
  else:
    return TXT_FMT % (s.url)

def print_content(rank, s):
  id = cgi.escape(s.title)
  print TOP_FMT % (rank, id, id)
  print BOTTOM_FMT % (s.authors, s.title, s.venue, s.year, get_link(s), s.upvotes - s.downvotes, s.upvotes, s.downvotes)

def print_past_reading(s):
  id = cgi.escape(s.title)
  print TOP_PAST_FMT % ()
  print BOTTOM_FMT % (s.authors, s.title, s.venue, s.year, get_link(s), s.upvotes - s.downvotes, s.upvotes, s.downvotes)

def process_suggestions():
  suggestions = read_suggestions()

  # sort in descending order
  suggestions.sort()
  suggestions.reverse()

  print '<table class="discussion">'
  rank = 1
  for s in suggestions:
    if not s.past:
      print_content(rank, s)
      rank += 1
  print '</table>'

def process_past_readings():
  suggestions = read_suggestions()

  # sort in descending order
  suggestions.sort()
  suggestions.reverse()

  print '<table class="discussion">'
  for s in suggestions:
    if s.past:
      print_past_reading(s)
  print '</table>'

def record_vote(vote, id):
  suggestions = read_suggestions()
  
  for s in suggestions:
    if s.title == id:
      if vote == 'up':
        if s.upvotes < 1000:
          s.upvotes += 1
        else:
          return
      else:
        if s.downvotes < 1000:
          s.downvotes += 1
        else:
          return
      break

  write_suggestions(suggestions)

if __name__ == '__main__':
  process_suggestions()
