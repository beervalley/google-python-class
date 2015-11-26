#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def order_url_word(url):
	match = re.search(r'[\w]+\-([\w]+)\.', url)
	if match:
		return match.group(1) 
	else:
		return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  urllist = []
  
  # 1. filename can be used directly as a string without parsing its data
  match = re.search(r'_(.+)', str(filename))
  server_name = match.group(1)
  url_with_servername = 'http://' + server_name
  
  f = open(filename, 'rU')
  for line in f:
  	match = re.search(r'GET\s(.*puzzle.*)\sHTTP', line)
  	# 2. After searching, remember always check if the result is None or not
  	if match:
  		url = match.group(1)
  		full_url = url_with_servername + url
  		if full_url not in urllist:
  			urllist.append(full_url)
  
  # 3. Always remember to close the file after processing it
  f.close()
  
  return sorted(urllist, key=order_url_word)
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  # 4. Check if the dest_dir exists, if not create it
  if not os.path.exists(dest_dir):
  	os.makedirs(dest_dir)
  
  # 5. Create a file with the path. It will create a file in the current
  # directory if the path is not given.
  f = open(os.path.join(dest_dir, 'index.html'), 'w')
  f.write('<verbatim>' + '\n' + '<html>' + '\n')
  
  i = 0
  for url in img_urls:
  	print "Retrieving img" + str(i) + " with url: " + url
  	filename = 'img' + str(i)
  	# 6. Notice how to use urllib.urlretrieve() with two parameters:
  	#    first one is the given url to retrieve data, second one is
  	#    destination filename with *its path*
  	urllib.urlretrieve(url, os.path.join(dest_dir, filename))
  	# 7. In html, if only gives filename without path, it will search the current directory for the file.
  	f.write("<img src=\"" + filename  + "\">")
  	i += 1
  
  f.write('\n' + '</body>' + '\n' + '</html>')
  f.close()
  
  
# Answer for the animal image: it is a rabbit reading a book on campus! :)
# Answer for the famous place image: it's the Eiffel Tower in beautiful Paris!!!

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  # print urls to verify it's working
  for url in img_urls:
  	print url

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
