#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  year = 0
  name_dict = {}
  name_rank = []
  
  f = open(filename, 'rU')
  
  # 1. If we use f.read(), then f cannot be used again for the for loop.
  for line in f:
    match_year = re.search(r'Popularity\sin\s(\d\d\d\d)', line)
    if match_year:
      break

  if not match_year:
    sys.stderr.write('Couldn\'t find the year!\n')
    sys.exit(1)
  
  year = match_year.group(1)

  # 2. Here we can use findall() to find all the names and ranks.
  # Then loop through the list of tuples for putting into dict
  for line in f:
    match_name = re.search(r'td\>([\d]+).+td\>([\w]+).+td\>([\w]+)', line)
    if match_name:
      name1 = match_name.group(2)
      name2 = match_name.group(3)
      rank = match_name.group(1)
      if name1 not in name_dict:
        name_dict[name1] = rank
      if name2 not in name_dict: 
        name_dict[name2] = rank
      # print name1, name2, rank
  
  f.close()

  name_rank.append(str(year))
  
  sort_name_dict = sorted(name_dict)
  for name in sort_name_dict:
    #print name, name_dict[name]
    namerank = name + ' ' + name_dict[name]
    name_rank.append(namerank)
  
  # print the list to verify the correctness
  for namerank in name_rank[:10]:
    print namerank
  
  return name_rank


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # 3. Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
  for filename in args:
    name_rank = extract_names(filename)
    text = '\n'.join(name_rank) + '\n'
    
    if summary:
      # 4. write to a file, name it and write content into it
      outfile = open(name_rank[0] + '.txt', 'w')
      outfile.write(text)
      outfile.close()
    else:
      print text
  
if __name__ == '__main__':
  main()
