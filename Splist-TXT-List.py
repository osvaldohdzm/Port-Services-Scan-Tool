import sys 
import argparse
import pathlib
import os

parser = argparse.ArgumentParser(description='Split text file into multitple')
parser.add_argument("-f", help='text filename', required=True)
parser.add_argument("-p", help='number of parts', required=True)
args = vars(parser.parse_args())
cwd = os.getcwd()  

filename = cwd + '/'+ args['f'] 
file_name_o_ext = os.path.splitext(filename)[0]
infile = open(filename) 
part = 1 
parts = int(args['p'])

file = pathlib.Path(filename)
if file.exists ():
    print ("File exist")
else:
    print ("File not exist")
    exit()

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
                smallfile = open(small_filename, "w")
                part = part + 1
            smallfile.write(line)
        else:
            smallfile.write(line)
    if smallfile:
        smallfile.close()