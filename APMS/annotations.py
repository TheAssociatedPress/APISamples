#!/usr/bin/env python
try:
	import config
except ImportError:
    raise ImportError('Please create config.py with your API key.\nIf you need a key, please visit https://developer.ap.org/ap-metadata-services and contact apmetadata@ap.org.\nIf you have a key, then create a file named "config.py" with\napms_api_key="<YOUR API KEY>"')
import argparse
import requests
import json
import sys
from jinja2 import Environment, PackageLoader


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--infile", type=argparse.FileType('r'), default=sys.stdin, help="The file you would like to tag (default: read from STDIIN)")
	parser.add_argument("-o", "--outfile", type=argparse.FileType('w'), default=sys.stdout, help="Write the output to a file (default: write to STDOUT)")
	parser.add_argument("-p", "--payload", dest="action", action="store_const", const="payload", default="invoke", help="Output the payload without invoking the API (default: call the API)")
	parser.add_argument("-t", "--template", dest="template", action="store", default="payload.json", help="Select the payload template (default: payload.json)")
	return parser.parse_args()

def parse_env():
	j2_env = Environment(loader=PackageLoader('apms', 'templates'))
	j2_env.filters['jsonify'] = json.dumps
	return j2_env

def create_payload(args, template_env):
	document={ "document" : args.infile.read()}
	payload = template_env.get_template(args.template).render(payload=document)
	return payload

args = parse_args()
template_env = parse_env()

payload = create_payload(args, template_env)

if args.action == "payload":
	result = payload
else:
	apms_url="http://cv.ap.org/annotations?apikey=" + config.apms_api_key
	response = requests.post(apms_url, data=payload)
	#print(response.status_code)
	result = response.text

args.outfile.write(result)

