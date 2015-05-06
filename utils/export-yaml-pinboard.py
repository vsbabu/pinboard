#!/usr/bin/env python
import sys
import os
import datetime

#--------------------------------------------------------------------------
#
# prints an yaml styled like a pin board. run it like
#   python this-script.py project1 project2 project3 etc
#
# You can use the word all to generate a list not based on project name
#
# author : vsbabu_AT_gmail_._com
#
# license - just do whatever you want with it at your own risk!
#
# notes: All my project  names have exactly one word (ie., no spaces)
#        A tag #xy indicates the task being done by person xy; # tags are printed in output
#        A tag @risk indicates this is an external dependency
#
#--------------------------------------------------------------------------

from numpy import array,append
from operator import itemgetter

#--------- todo + done; how many tasks in one project sticky note?
TOTAL_TASKS_TO_SHOW = 50
#timezone offset in hours from Zulu
TZ_OFFSET=5.5

output_header="""
var boxesInput = function(){/*
"""

output_footer="""

*/}.toString().slice(14,-3);
"""


today = datetime.datetime.now().date()
def print_yml_descriptions(tasks):
    for t in tasks:
        style = ""
        flags = ""
        alt = t['id']
        if 'tags' in t:
            for g in t['tags']:
                if g[0]=='#':
                    flags = flags + " " + g
            if '@risk' in t['tags']:
                style = style + "~"
                flags = flags + """ ^"""
        if t['status'] == 'completed':
            style = style + "-"
            due = datetime.datetime.strptime(t['end'], "%Y%m%dT%H%M%SZ") + datetime.timedelta(hours=TZ_OFFSET)
            due = due.date();
            print """     - %s %s %s""" % (style, t['description'], due.strftime("%m/%d"))
        elif 'due' in t:
            due = datetime.datetime.strptime(t['due'], "%Y%m%dT%H%M%SZ") + datetime.timedelta(hours=TZ_OFFSET)
            due = due.date();
            if due < today :
                style = style + "^^"
            if due == today :
                style = style + "^"
            if 'depends' in t:
                style = style + "~"
            if 'start' in t:
                style = style + "!"
            print """     - %s %s %s""" % (style, t['description'], due.strftime("%m/%d"))
        else:
            print """     - %s %s""" % (style, t['description'])

def get_tasks_for_project(project, tags=""):
    tasks = array([])
    p = os.popen('task export pro:%s %s' % (project, tags),"r")
    while 1:
        line = p.readline()
        if not line: break
        try:
            lin = eval(line)
        except:
            #print "****[%s]****" % line
            continue
        tasks = append(tasks, lin)
    return tasks

def get_all_tasks(tags=""):
    tasks = array([])
    p = os.popen('task export %s' % (tags),"r")
    while 1:
        line = p.readline()
        if not line: break
        try:
            lin = eval(line)
        except:
            #print "****[%s]****" % line
            continue
        tasks = append(tasks, lin)
    return tasks


def main():
    colors = "yellow greenyellow yellowgreen cornsilk orange  skyblue  khaki lightpink".split()
    count = 0
    for project in sys.argv[1:]:
        #todo = get_tasks_for_project(project, "status:pending due.before:60days")
        if project == "all":
            todo = get_all_tasks("status:pending")
        else:
            todo = get_tasks_for_project(project, "status:pending")
        try:
            tmp = sorted(todo, key=itemgetter('due'), reverse=False)
            todo = tmp
        except:
           pass
        if project == "all":
            done = ()
        else:
            done = get_tasks_for_project(project, "status:completed")
            done = sorted(done, key=itemgetter('end'), reverse=True)
        if 0 == len(todo) + len(done):
            continue
        if len(todo) > TOTAL_TASKS_TO_SHOW:
            todo = todo[0:TOTAL_TASKS_TO_SHOW]
            done = []
        if len(todo) + len(done) > TOTAL_TASKS_TO_SHOW:
            done = done[0 : TOTAL_TASKS_TO_SHOW - len(todo)]
        print """
- title: %s
  color: %s
  items:""" % (project, colors[count % len(colors)])
        print_yml_descriptions(todo)
        print_yml_descriptions(done)
        print
        count = count + 1


if __name__ == '__main__':
    print output_header
    main()
    print output_footer
