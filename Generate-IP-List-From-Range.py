from ipaddress import ip_address
import argparse
import itertools

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

    return address

def ips(start, end):
    '''Return IPs in IPv4 range, inclusive.'''
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]


parser = argparse.ArgumentParser(description='Multiple nmap scans all lists txt in directory')
parser.add_argument("-range", help='dictory name', required=True)
args = vars(parser.parse_args())

ip_range = args['range']

ip_min = ip_range.split('-')[0]
ip_max = ip_range.split('-')[1]

print(ip_min , ip_max)

myips = ips(ip_min, ip_max)

with open('ip-list.txt', 'w') as f:
    for item in myips:
        last_octet = item.split('.')[3]
        if not (last_octet == '0' or last_octet == '255'):
            f.write("%s\n" % item)