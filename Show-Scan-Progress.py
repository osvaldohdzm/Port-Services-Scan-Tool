import os
import sys
import progressbar
import glob
import pathlib
from time import sleep
from time import time, sleep

import argparse



def deleteFile():
   for f in glob.glob("comp*"):
      os.remove(f)
   for f in glob.glob("all*"):
      os.remove(f)


def num_lines_in_file(filename_list_compare):
    file = open(filename_list_compare, "r")
    line_count_original = 0
    for line in file:
        if line != "\n":
            line_count_original += 1
    file.close()
    return line_count_original

def progress_num(filename_list_compare, total_lines):
    arr = os.listdir('Actual')
    
    with open('comp_temp.txt', 'w') as f:
        for item in arr:
            f.write("%s\n" % item)    
    
    file = open("comp_temp.txt", "r")
    line_count_progress = 0
    for line in file:
        if line != "\n":
            line_count_progress += 1
    file.close()
    line_count_progress = line_count_progress - 1 #Beceause fit ignore file 
    deleteFile()
    return line_count_progress

arser = argparse.ArgumentParser(description='Compare percetage progress from file scan nmap text file')
parser.add_argument("-f", help='list file to compare', required=True)
parser.add_argument('-c', action='store_true')
args = vars(parser.parse_args())

cwd = os.getcwd() 
filename_list_compare = cwd + '/'+ args['f'] 

file = pathlib.Path(filename_list_compare)
if file.exists ():
    print ("File exist")
else:
    print ("File not exist")
    exit()

total_lines = num_lines_in_file(filename_list_compare)



bar = progressbar.ProgressBar(maxval=total_lines, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
current_progress = progress_num(filename_list_compare, total_lines)
print("\nTotal {}".format(str(total_lines)))
bar.start()
if args['c']:
  while current_progress < total_lines:    
    current_progress = progress_num(filename_list_compare, total_lines)  
    bar.update(current_progress)
    sleep(2 - time() % 2)
  bar.finish()
else:
  current_progress = progress_num(filename_list_compare, total_lines)
  print(str(current_progress)+'/'+str(total_lines))
  bar.start()
  bar.update(current_progress)
  #print()
  #input("\n Press Enter to continue...")
  exit()
