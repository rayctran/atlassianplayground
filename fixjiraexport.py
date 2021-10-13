#!/usr/bin/python

import glob
import logging
import os
import shutil
import sys
import subprocess
import zipfile
import netrc
import re
import pandas as pd
import datetime

if len(sys.argv) != 2:
    raise ValueError('Please enter export file')

debug = True
myfile = sys.argv[1]
outfile = "updatedtickets.csv"
#mytmpfile = myfile+.+tmp
#print(mytmpfile)

# Summary,Issue key,Status,Priority,Assignee,Reporter,Creator,Created,Updated,Last Viewed,Description,Watchers,Watchers1,Watchers2,Watchers3,Watchers4,Custom field (ITSM Issue Type),Custom field (Request Type),Comment,Comment1,Comment2,Comment3,Comment4,Comment5,Comment6,Comment7,Comment8,Comment9,Comment10
issues = pd.read_csv(myfile, index_col=0)

# Rename Watchers and Comment Columns
cols=pd.Series(issues.columns)
for dup in issues.columns[issues.columns.duplicated(keep=False)]:
    cols[issues.columns.get_loc(dup)] = ([dup + '_' + str(d_idx)
                                     if d_idx != 0
                                     else dup
                                     for d_idx in range(issues.columns.get_loc(dup).sum())]
                                    )
issues.columns=cols

if debug:
    mycolumns = list(issues)
    print (mycolumns)


#issues(['Assignee','Reporter','Creator','Watchers']).str.replace(r'([a-z]*\.[a-z]*)', r'\1@torc\.ai')
name_columns = ['Assignee', 'Reporter', 'Creator', 'Watchers_1', 'Watchers_2', 'Watchers_3', 'Watchers_4', 'Watchers_5']
issues[name_columns] = issues[name_columns].replace(to_replace =r'([a-z]*.*[a-z]*)', value=r'\1@torc.ai', regex=True)
comment_columns = ['Comment_1', 'Comment_2', 'Comment_3', 'Comment_4', 'Comment_5', 'Comment_6', 'Comment_7', 'Comment_8', 'Comment_9', 'Comment_10', 'Comments_11']
issues[comment_columns] = issues[comment_columns].replace(to_replace=r';([a-z]*.*[a-z]*);', value=r';\1@torc.ai;', regex=True)

if debug:
    print(issues.Comment)
    print(issues.Assignee)
    #print(issues)

# Restore Watchers and Comment
issues.rename(columns={'Watchers1':'Watchers', 'Watchers2':'Watchers', 'Watchers3':'Watchers', 'Watchers4':'Watchers'}, inplace=True)
issues.rename(columns={'Comment1':'Comment', 'Comment2':'Comment', 'Comment3':'Comment', 'Comment4':'Comment', 'Comment5':'Comment', 'Comment6':'Comment', 'Comment7':'Comment', 'Comment8':'Comment', 'Comment9':'Comment', 'Comment10':'Comment'}, inplace=True)




# Dump output data into a file
issues.to_csv(outfile)

def fixcomments(comments):
   mycomment = pd.read_csv(comments, sep=";")
   print(comment)
   match = re.search('^\d{2}/\w+/\d{4}\s\d+:\d+\s(AM|PM)', comment)
   datefound = match.group(0)
   print ("initial date found " +str(datefound) )
   datefound = datetime.datetime.strptime(datefound,'%d/%b/%Y %H:%M %p')
   newdate = datefound.strftime('%m/%d/%Y %H:%M %p')
   print("Old date is " +str(datefound) + " new date is " + str(newdate))
   return newdate
