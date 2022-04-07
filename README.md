# Port-Services-Scan-Tool (for NMAP)

[TOC]





Create Actual direcotory 
Create Historic Directory



1. To run multiple scan run: script-multiple-nmap-scan





## Windows Instalation

```
https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.6.5&os=windows&cpu=x86_64&pkg=msi&m=gigenet

pip install -r /path/to/requirements.txt

https://nmap.org/download.html


```

## Linux Instalation

```
mariadb -u root -p

mariadb -u root -p < ports_services_scans.sql

```





## Generate multiple ip list files to scan from range of ips

Windows:

```
cd Desktop/port-services-enumeration-tools

python script-split-list.py -f Lists\extern-list-v1.txt -p 12
move Lists\extern-list-v1-*.* Scans
```

### Generate multiple ip list files to scan from text file list

Windows:

Go to location:
```
cd Desktop/port-services-enumeration-tools
```

Example usage:
```
python Splist-TXT-List.py -f Lists\IP-list-intern-v2.txt -p 12
move Lists\IP-list-intern-v2-*.* Scans-Lists
```

## External Scans

### Linux 

```
cd Desktop/port-services-enumeration-tools 

# Kill previous scan
sudo ps aux | grep nmap
sudo killall nmap

python3 script-progress.py -f Lists/all-list-extern-v1.txt
sudo ps aux | grep nmap
sudo killall nmap
ls Actual
python3 script-xml-to-sql.py -d Actual

ls /tmp
sudo rm -r /tmp/* 

mv Actual/* Historic
ls -la Actual

sudo python3 script-multiple-nmap-scan.py -d Scans

python3 script-progress.py -f Lists/all-list-extern-v1.txt
```



### Windows

Go to folder location:
```
cd Desktop/port-services-enumeration-tools 

```

Execute scan:
```
python script-multiple-nmap-scan.py -d Scans

# Check progress
python script-progress.py -f Lists/extern-list-v1.txt

python script-xml-to-sql.py -d Actual

```

Load XMLs in Actual folder to database.
```
python script-xml-to-sql.py -d Actual
```

Then move the content in Actual to Historic.
```
move Actual\*.* Historic
```



## Internal Scans

### Windows

Go to folder location:
```
cd Desktop/port-services-enumeration-tools 

```

Kill previuous scans jobs:
```
taskkill /IM "cmd.exe" /F
```

Execute scan Specifid ports:
```
python Multiple-NMAP-Scan.py -f Lists/Demo-list.txt -n 5 -d Scans-Lists -p 7,19,20,21,22,23,25,37,53,69,79,80,110,111,135,137,138,139,143,161,443,465,512,513,514,993,1433,1434,1720,1723,2077,2078,2222,2776,3306,3389,5060,5061,5222,5269,5986,8080,8443,9002 -progress
```

Execute scan all ports:
```
python Multiple-NMAP-Scan.py -d Scans-Lists -p *
```

Execute scan all ports and all features:
```
python Multiple-NMAP-Scan.py -d Scans-Lists -p * -progress -savesql

python Multiple-NMAP-Scan.py -d Scans-Lists -p * -progress
```


### Check progress
```
python Show-Scan-Progress.py -f Lists/IP-list-intern-v2.txt
```
See coontinously:
```
python Show-Scan-Progress.py -f Lists/IP-list-intern-v2.txt -c
```

### Save scans resuls to database

Load XMLs in Actual folder to database.
```
python Load-XML-to-SQL-Database.py -d Actual
```

Then move the content in Actual to Historic.
```
move Actual\\*.xml Historic
```


### Schedule Full Port Scan 



