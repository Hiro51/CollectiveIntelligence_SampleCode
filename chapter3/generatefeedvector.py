import feedparser
import re

# Returns title and ditionary of word counts for RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    # Extract a list of words
    words=getwords(e.title+''+summary)
    for word in words:
      wc.setdefault(word, 0)
      wc[word]+=1

  try:
   return d.feed.title,wc
  except AttributeError:
   return "nofeed",wc

def getwords(html):
  # Remove all the html tags
  txt=re.compile(r'<[^>]+>').sub('', html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowcase
  return [word.lower() for word in words if word!='']

apcount={}
wordcounts={}
feedlist=[]

for feedurl in file('feedlist.txt'):
  feedlist.append(feedurl)
  title, wc = getwordcounts(feedurl)
  wordcounts[title]=wc
  for word, count in wc.items():
    apcount.setdefault(word, 0)
    if count>1:
      apcount[word]+=1

print wordcounts

wordlist = []
for w, bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>0.1 and frac<0.5: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  print blog
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')