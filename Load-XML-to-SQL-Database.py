#!/usr/bin/env python3
####################################################################################
#
#
#
####################################################################################

# Module Imports
import mariadb
import os
import re
import time
import logging
import sys
import datetime
import subprocess

from argparse import ArgumentParser

from lxml import etree

import xml.etree.ElementTree as ET


def database_connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="LTypLAkeroSa",
            host="127.0.0.1",
            port=3306,
            database="ports_services_scans",
            autocommit=True
        )
        print("Conecction succesfully!")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn



# Get cur
conn = database_connection()



if sys.version_info <= (3, 0):
    sys.stdout.write("This script requires Python 3.x\n")
    sys.exit(1)

parser = ArgumentParser()
parser.add_argument(
    "-d", "--dir", dest="directory", help="Parse all xml in directory", metavar="DIR"
)
args = parser.parse_args()
xmlSet = set()

if args.directory is not None:
    if os.path.isdir(args.directory):
        path = args.directory

        for f in os.listdir(path):
            # For now we assume xml is nMap
            if f.endswith(".xml"):
                fullname = os.path.join(path, f)
                logging.debug("Adding: %r", fullname)
                xmlSet.add(fullname)
    else:
        logging.warn("Not a directory: %r", args.directory)
else:
    print("usage issues =(")
    parser.print_help()
    exit()


# Check to ensute we have work to do
if not xmlSet:
    print("No XML files were found ... No work to do")
    exit()
for xml in xmlSet:
    if xml.endswith(".xml"):

        logging.debug("Parsing: %r", xml)

        try:
            doc = etree.parse(xml)
            tree = ET.parse(xml)
            root = tree.getroot()
        except Exception as e:
            print(e)
            pass

        time_of_scan = ""
        args = ""
        mac = ""
        ip = ""
        hostnames = []
        ports = []
        services_names = []
        products = []
        versions = []
        operative_system = []

        for x in doc.xpath("//nmaprun"):
            time_of_scan = datetime.datetime.fromtimestamp(float(x.attrib["start"]))
            args = str(x.attrib["args"])
            startstr = str(x.attrib["startstr"])
            startstr = datetime.datetime.strptime(startstr, "%a %b %d %X %Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        for element in root.findall(".//finished"):
            timestr = element.attrib["timestr"]
            timestr = datetime.datetime.strptime(timestr, "%a %b %d %X %Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        for element in root.findall(".//hosts"):
            up = element.attrib["up"]

        for x in doc.xpath("//port"):
            port = str(x.attrib["portid"])
            current_state = list(x.iter())[1].attrib["state"]
            
            try:
                current_service_name = list(x.iter())[2].attrib["name"]
                print(current_service_name)
            except:
                current_service_name = "unknown"
            try:
                current_product = list(x.iter())[2].attrib["product"]
            except:
                current_product = ""
            try:
                current_os = list(x.iter())[2].attrib["ostype"]
            except:
                current_os = ""
            try:
                current_version = list(x.iter())[2].attrib["version"]
            except:
                current_version = ""

            ports.append([port, current_state, current_service_name, current_product, current_version, current_os])

      

        for x in doc.xpath("//hostname"):
            hostname = str(x.attrib["name"])
            hostnames.append(hostname)
            hostnames = list(set(hostnames))
            print(hostname)
            print(hostnames)


        for x in doc.xpath("//address"):
            if str(x.attrib["addrtype"]) == "mac":
                mac = str(x.attrib["addr"])
        for x in doc.xpath("//address"):
            if str(x.attrib["addrtype"]) == "ipv4":
                ip = str(x.attrib["addr"])

        nmap_version = subprocess.check_output("nmap --version", shell=True, text=True)
        nmap_version = nmap_version.splitlines()[0]

        
        result = 1
        cur = conn.cursor()

        
        
        if (ip != "" ):

            try:
                query1 = ("SELECT COUNT(1) FROM scans INNER JOIN hosts ON scans.scan_id=hosts.scan_id WHERE start=%s AND ip=%s")
                query1_data = (startstr, ip)
                cur.execute(query1, query1_data)

            except mariadb.Error as e:
                print(f"Error in count element sentence: {e}")        

            count_row = cur.fetchone()                
            count = count_row[0]

            print(count_row[0])

            if count == 0:
                print("Element {} is new, adding...".format(ip))
                
                try:                    
                    add_scan = ("INSERT INTO scans (start,end,version,arguments) VALUES (%s, %s, %s, %s)")
                    data_scan = (startstr, timestr, nmap_version, args)
                    cur.execute(add_scan, data_scan)
                         
                except mariadb.Error as e:
                    print(f"Error al insertar scan: {e}")
                except:
                    conn.rollback()

                scan_id = str(cur.lastrowid)
                print("Inserted scan_id " + scan_id)

                try:      
                    add_hosts = ("INSERT INTO hosts (scan_id, ip, mac_address, status, hostname, operative_system) VALUES (%s, %s, %s, %s, %s, %s)")
                    if hostnames:                            
                        for h in hostnames:  
                            data_host = (scan_id, ip, mac, up, h, "")
                            print("inserting hosntame:" + h)                 
                            cur.execute(add_hosts, data_host)    
                    else:
                        data_host = (scan_id, ip, mac, up, "", "")
                        cur.execute(add_hosts, data_host)
                         
                except mariadb.Error as e:
                    print(f"Error al insertar host: {e}")
                except:
                    conn.rollback()


                try:      
                    add_ports = ("INSERT INTO ports (scan_id, host_ip, number, status, service_name, product, version, operative_system) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")                    
                    
                    for p in ports:   
                        print(p)       
                        data_ports = (scan_id, ip, p[0] ,p[1], p[2], p[3], p[4], p[5])   
                        cur.execute(add_ports, data_ports)                          
                except mariadb.Error as e:
                    print(f"Error al insertar port: {e}")
                except:
                    conn.rollback()
            
 
                # Close Connection
                # Cleanup
                     
                
            else :
                print("Element {} already loaded!".format(ip))
                pass
    
cur.close()         
conn.close() 
print("Done.")      
