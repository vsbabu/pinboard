#!/usr/bin/env python
import sys
import os
import datetime 

#--------------------------------------------------------------------------
#
# prints an html styled like a pin board. run it like
#   python this-script.py project1 project2 project3 etc
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
TOTAL_TASKS_TO_SHOW = 16
#timezone offset in hours from Zulu
TZ_OFFSET=5.5

html_header="""
<!DOCTYPE html>
<html lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Pin Board!</title>
</head>
<body>
<!-- fancy font - uncomment this if you like it
<link href='http://fonts.googleapis.com/css?family=Nothing+You+Could+Do' rel='stylesheet' type='text/css'>
//-->
<!-- putting style in body and not header so that the content can be copy-pasted from browser to a mail client -->
<style type="text/css">
body {
    /*
    // fancy background; better to download and keep it locally as below
    background: #CF7C29 url(http://fc07.deviantart.net/fs71/i/2010/245/0/c/pinboard_texture_by_nikky81-d2xuip9.png);
    */
    background: #CF7C29 url(Pictures/pinboard.png);
}
dl.project-box {
    display: block;
    float: left;
    margin: 0.3em 0.25em;
    padding: 0;
    font-size: 90%;
}
dl.project-box dt {
    font-weight: bold;
    padding: 0;
    margin: 0;
}
dl.project-box dt.project-name {
    font-size: 120%;
    color: #959289;
    padding: .5em;
    font-weight: bold;
    text-align: left;
    text-transform: uppercase;
    border-bottom: 1px solid #131210;
    font-family: 'Nothing You Could Do', Futura, "Trebuchet MS", Arial, sans-serif;
}
dl.project-box dd {
    margin: 0 0 .2em 0;
    text-align: left;
    padding: 0 .2em;
    font-style: normal;
}
dl.project-box dd ul  {
    margin-top: 0;
    padding-top: 0;
    list-style-type: none;
    margin-left: 0;
    padding-left: 1em;
    text-indent: -0.5em;
} 
dl.project-box dd ul li  {
    padding-bottom: 1px;
    border-bottom: 1px dotted silver;
}
dl.project-box dd ul li:first-letter  {
    text-transform: uppercase;
}
dl.project-box dd ul li.risk  {
    color: brown;
} 
dl.project-box dd ul li.overdue  {
    color: red;
} 
dl.project-box dd ul li.duesoon  {
    color: #FF3300;
    color: #FF33FF;
} 
dl.project-box dd ul li.completed  {
    color: darkslategray;
    text-decoration: line-through;
} 
dl.project-box dd ul li.completed em {
	color: darkslategray;
    text-decoration: line-through;
} 

/* http://www.binvisions.com/tutorials/post-it-sticky-note-css-3-html-5/ */
.sticky {
    margin: 0;
    padding: 8px 24px;
    width: 260px;
    height: 300px;
    font-family: Sans,'Nothing You Could Do', Arial;
    border:1px #E8Ds47 solid;
    -moz-box-shadow:0px 0px 6px 1px #333333
    -webkit-box-shadow:0px 0px 6px 1px #333333;
    box-shadow:0px 0px 6px 1px #333333;
    background: #fefdca; /* Old browsers */
    background: -moz-linear-gradient(top, #fefdca 0%, #f7f381 100%); /* FF3.6+ */
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#fefdca), color-stop(100%,#f7f381)); /* Chrome,Safari4+ */
    background: -webkit-linear-gradient(top, #fefdca 0%,#f7f381 100%); /* Chrome10+,Safari5.1+ */
    background: -o-linear-gradient(top, #fefdca 0%,#f7f381 100%); /* Opera11.10+ */
    background: -ms-linear-gradient(top, #fefdca 0%,#f7f381 100%); /* IE10+ */
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fefdca', endColorstr='#f7f381',GradientType=0 ); /* IE6-9 */
    background: linear-gradient(top, #fefdca 0%,#f7f381 100%); /* W3C; A catch-all for everything else */
    overflow-y:hidden;
}


em.due {
    margin: 1px 1px 1px 1px;
    padding: 1px 1px 1px 1px;
    font-style: normal;
    font-size: 7pt;
    display: block;
    float: right;
}

em.ongoing  {
    background-color: #3c9;
    color: black;
    padding: 1px 1px 1px 1px;
    margin: 0px 1px 0px 0px;        
    border: 1px solid black;
    font-size: xx-small;
    font-style: normal;        
    font-weight: normal;
}        
em.done {
    background-color: transparent;
    color: green;
    padding: 1px 1px 1px 1px;
    margin: 0px 1px 0px 0px;        
    font-size: xx-small;
    font-style: normal;        
    font-weight: bold;
}            
em.shouldhavestarted  {
    background-color: orange;
    color: white;
    padding: 1px 1px 1px 1px;
    margin: 0px 1px 0px 0px;        
    border: 1px solid black;
    font-size: xx-small;
    font-style: normal;        
    font-weight: normal;
}    
em.duesoon  {
    background-color: #f90;
    color: brown;
    padding: 1px 1px 1px 1px;
    margin: 0px 1px 0px 0px;
    border: 1px solid black;
    font-size: xx-small;
    font-style: normal;
    font-weight: normal;
}            

</style>
"""

html_footer="""
</body>
</html>
"""


today = datetime.datetime.now().date()
def print_html_descriptions(tasks):
    for t in tasks:
        style = ""
        flags = ""
        alt = t['id']
        if 'tags' in t:
            for g in t['tags']:
                if g[0]=='#':
                    flags = flags + " " + g
            if '@risk' in t['tags']:
                style = style + " risk"
                flags = flags + """ <em class="duesoon" title="dependency">D</em>"""
                alt = "%s %s" % (t['id'], t['tags'])
        if t['status'] == 'completed':
            style = style + " completed"
            due = datetime.datetime.strptime(t['end'], "%Y%m%dT%H%M%SZ") + datetime.timedelta(hours=TZ_OFFSET)
            due = due.date();
            print """ <li class="%s" title="%s">%s %s<em class="due">%s</em></li>""" % (style, alt, t['description'], flags, due.strftime("%m/%d"))
        elif 'due' in t:
            due = datetime.datetime.strptime(t['due'], "%Y%m%dT%H%M%SZ") + datetime.timedelta(hours=TZ_OFFSET)
            due = due.date();
            if due < today :
                style = style + " overdue"
            if due == today :
                style = style + " duesoon"
            if 'depends' in t:
                flags = flags + """ <em class="shouldhavestarted" title="waiting">W</em>"""
            if 'start' in t:
                flags = flags + """ <em class="ongoing" title="ongoing">O</em>"""
            print """ <li class="%s" title="%s">%s %s<em class="due">%s</em></li>""" % (style, alt, t['description'], flags, due.strftime("%m/%d"))
        else:
            print """ <li class="%s" title="%s">%s %s</li>""" % (style, alt, t['description'], flags)

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
    
def main():
    for project in sys.argv[1:]:
        #todo = get_tasks_for_project(project, "status:pending due.before:60days")
        todo = get_tasks_for_project(project, "status:pending")
        try:
            tmp = sorted(todo, key=itemgetter('due'), reverse=False)
            todo = tmp
        except:
           pass 
        done = get_tasks_for_project(project, "status:completed")
        done = sorted(done, key=itemgetter('end'), reverse=True)
        if 0 == len(todo) + len(done): 
            continue
        if len(todo) > TOTAL_TASKS_TO_SHOW:
            todo = todo[0:TOTAL_TASKS_TO_SHOW]
            done = []
        if len(todo) + len(done) > TOTAL_TASKS_TO_SHOW:
            done = done[0 : TOTAL_TASKS_TO_SHOW - len(todo)]
        print """<dl class="project-box sticky">"""
        print """<dt class="project-name">%s</dt>""" % project
        print("<dd><ul>")
        print_html_descriptions(todo)
        print_html_descriptions(done)
        print("</ul></dd>")
        print
        print """</dl>\n\n"""


if __name__ == '__main__':
    print html_header
    main()
    print html_footer
