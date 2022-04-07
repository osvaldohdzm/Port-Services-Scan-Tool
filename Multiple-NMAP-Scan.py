
# sudo python3 script-multiple-nmap-scan.py -d Scans

import os
import _thread
import subprocess
import platform
import time
from subprocess import Popen
import argparse
import sys
import progressbar
import glob
import pathlib
from time import sleep
from time import time, sleep
import sys 
import argparse
import pathlib
import os

cwd = os.getcwd() 

def split_txt_file(filename, parts):
    file_name_o_ext = os.path.splitext(os.path.basename(filename))[0]
        
    part = 1 
    file = pathlib.Path(filename)
    if file.exists ():
        print ("File exist")
    else:
        print ("File not exist")
        exit()
    infile = open(filename) 
    
    num_lines = sum(1 for line in infile)
    lines_per_file = int(num_lines/parts)
    smallfile = None
    
    with open(filename)  as bigfile:
        for lineno, line in enumerate(bigfile):
            if (part <= parts):
                if lineno % lines_per_file == 0:
                    if smallfile:
                        smallfile.close()            
                    small_filename = file_name_o_ext +'-'+ str(part) + '.txt'  
                    small_file_path = os.path.join(cwd,"Scans-Lists",small_filename) 
                    smallfile = open(small_file_path, "w")
                    part = part + 1
                smallfile.write(line)
            else:
                smallfile.write(line)
        if smallfile:
            smallfile.close()

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

def initialize_progress_bar(filename_list_compare):
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
  print("\nTotal {} targets".format(str(total_lines)))
  bar.start()
  return bar

parser = argparse.ArgumentParser(description='Multiple nmap scans all lists txt in directory')
parser.add_argument("-d", help='dictory name', required=True)
parser.add_argument("-p", help='ports', required=True)
parser.add_argument("-f", help='text filename', required=True)
parser.add_argument("-n", help='number of parts', required=True)
parser.add_argument("-progress", help='Show progress',action='store_true')
parser.add_argument("-savesql", help='Save in SQL Data base configuration.',action='store_true')
args = vars(parser.parse_args())

directory = args['d']
ports = args['p']

# Create target directory & all intermediate directories if don't exists
if not os.path.exists(directory):
    print('No existen el directorio')
    exit()

# Clean actual
arr = os.listdir('Actual')
try:
    arr.remove('.gitignore')
except Exception as e:
  print(e)
  exit()
for f in arr:
    os.remove(os.path.join("Actual", f))

arr = os.listdir(directory)
try:
    arr.remove('.gitignore')
except Exception as e:
	print(e)
	exit()



filename = cwd + '/'+ args['f'] 
parts = int(args['n'])
split_txt_file(filename, parts)
filename_list_compare = cwd + '/'+ args['f'] 

if(platform.system() == 'Linux'):    
    for filename in arr:
        file_name_no_ext = os.path.splitext(filename)[0]    
        print("scanning..."+file_name_no_ext)
        log = open('/tmp/'+file_name_no_ext+'.log', 'a')
        subprocess.Popen(['xargs','-a',directory+'/'+filename,'-I','{{{}}}','-d',"\\n" , 'nmap','-vv','--open','-Pn', '-sS', '-sV', '-p-', '-sC',  '--stats-every', '10s', '--script-timeout', '1000ms', '--host-timeout', '120m', '-oX', 'Actual/{{{}}} %Y-%m-%d %H-%M-%S.xml',  '{{{}}}'],stdout=log, stderr=log)     
elif(platform.system() == 'Windows'):
    poll_list = []
    for filename in arr:        
        file_name_no_ext = os.path.splitext(filename)[0]   
        log_name = os.environ['USERPROFILE']+'\\AppData\\Local\\Temp\\'+file_name_no_ext+'.log'
        log = open(log_name, 'a')
        if ports == '*':            
           p = subprocess.Popen(['cmd','/c','for','/F','%A','in','(%CD%\\' + directory +'\\'+ filename +')','do','(','nmap','--open','-Pn','-sSV','-p-','-sC','-n','--stats-every','10s','--script-timeout','1000ms','--host-timeout','120m','-oX','Actual\\%A %date:~0,2%-%date:~3,2%-%date:~6,8% %time:~0,2%-%time:~3,2%-%time:~6,2%.xml','%A)'],stdout=log, stderr=log)         
        else: 
           p = subprocess.Popen(['cmd','/c','for','/F','%A','in','(%CD%\\' + directory +'\\'+ filename +')','do','(','nmap','--open','-Pn','-sSV','-p',ports,'-sC','-n','--stats-every','10s','--script-timeout','1000ms','--host-timeout','120m','-oX','Actual\\%A %date:~0,2%-%date:~3,2%-%date:~6,8% %time:~0,2%-%time:~3,2%-%time:~6,2%.xml','%A)'],stdout=log, stderr=log)                 
        poll_list.append(p)
    if args['progress']:        
        bar = initialize_progress_bar(filename_list_compare)
        
        while all(p.poll() is None for p in poll_list):                
            total_lines = num_lines_in_file(filename_list_compare)
            current_progress = progress_num(filename_list_compare, total_lines) 
            bar.update(current_progress) 
            sleep(2 - time() % 2)
        bar.finish()   
        print("Scan complete")             
    if args['savesql']:
        subprocess.call(['python','Load-XML-to-SQL-Database.py','-d','Actual'])         
        subprocess.call(['cmd','/c','move','Actual\\*.xml','Historic'])    
else:
    exit()