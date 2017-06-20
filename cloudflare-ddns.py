#!/usr/bin/env python
#
# CloudFlare DDNS script.
#
# usage:
#   cloudflare-ddns.py --help
#
# See README for details

import requests
import json
import yaml
import os
import sys
import logging
import argparse
from subprocess import Popen, PIPE

# CLI usage
parser = argparse.ArgumentParser( 'cloudflare-ddns.py' )
parser.add_argument( '-k',            dest="cf_api_key", help="Cloudflare API key" )
parser.add_argument( '-e',            dest="cf_email", help="Cloudflare email" )
parser.add_argument( '-c',            dest="cf_config", help="Config file to load" )
parser.add_argument( '-t', '--ttl',   dest="cf_ttl", help="Record TTL", type=int )
parser.add_argument( '-d',            dest="cf_domain", help="Domain name", )
parser.add_argument( '-r',            dest="cf_record", help="Record to update" )
parser.add_argument( '-x',            dest="cf_record_type", help="Record type", choices=[ 'A', 'AAAA' ] )
parser.add_argument( '-p', '--proxy', dest="cf_proxied", action="store_true", help="Set proxied" )
parser.add_argument( '--dig',         dest="cf_use_dig", action="store_true" )
args = parser.parse_args()

# Logging
# ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')
cf_log_level = logging.INFO

logging.basicConfig(filename=os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'logs', 'cloudflare-ddns.log' ), level=cf_log_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logging.getLogger().addHandler( logging.StreamHandler() )
logger = logging.getLogger( __name__ )

# Cloudflare API endpoint
CLOUDFLARE_URL = 'https://api.cloudflare.com/client/v4'

# Let's go
def main():
    if args.cf_config:
        config_path = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), 'configs', args.cf_config )
        if os.path.isfile( config_path ):

            # Read config file
            with open( config_path, 'r' ) as file:
                config = yaml.safe_load( file )
                cf_api_key = args.cf_api_key or config.get('cf_api_key')
                cf_email = args.cf_email or config.get('cf_email')
                cf_domain = args.cf_domain or config.get('cf_domain')
                cf_record = args.cf_record or config.get('cf_record')
                cf_record_type = args.cf_record_type or config.get('cf_record_type')
                cf_proxied = args.cf_proxied or config.get('cf_proxied') or False
                cf_ttl = args.cf_ttl or config.get('cf_ttl')
                cf_use_dig = args.cf_use_dig or config.get('cf_use_dig')
        else:
            logger.error( "Config file '{}' not found".format( config_path ) )
            sys.exit(1)
    else:
        if args.cf_api_key is None:
            logger.error( "Please specify an API key" )
            sys.exit(1)
        logger.warning( "You better not use the API key argument from CLI since it can be exposed to practically anyone on your system." )
        cf_api_key = args.cf_api_key
        if args.cf_email is None:
            logger.error( "Please specify your Cloudflare e-mail" )
            sys.exit(1)
        cf_email = args.cf_email
        if args.cf_domain is None:
            logger.error( "Please specify your domain name" )
            sys.exit(1)
        cf_domain = args.cf_domain
        if args.cf_record is None:
            logger.error( "Please specify your record name" )
            sys.exit(1)
        cf_record = args.cf_record
        cf_record_type = args.cf_record_type or 'A'
        cf_proxied = args.cf_proxied or False
        cf_ttl = args.cf_ttl or 1
        cf_use_dig = args.cf_use_dig or False

    # Validate TTL
    if not 120 <= cf_ttl <= 2147483647 and not cf_ttl == 1:
        logger.error( "The TTL must be between 120 and 2147483647 seconds" )
        sys.exit(1)

    # Authentication header
    auth_header = {
        'X-Auth-Key': cf_api_key,
        'X-Auth-Email': cf_email,
    }

    # Retrieve the public IP address
    if cf_use_dig:
        p = Popen([ "dig", "+short", "myip.opendns.com", cf_record_type, "@resolver1.opendns.com" ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        public_ip = output.decode().strip()
    else:
        if cf_record_type == 'A':
            public_ip = requests.get( "https://ipv4.icanhazip.com", timeout=5 ).text.strip()
        elif cf_record_type == 'AAAA':
            public_ip = requests.get( "https://ipv6.icanhazip.com", timeout=5 ).text.strip()

    # Retrieve the zone corresponding to the domain
    results = get_paginated_results(
        'GET',
        CLOUDFLARE_URL + '/zones',
        auth_header,
    )
    cf_zone_id = None
    for zone in results:
        zone_name = zone['name']
        zone_id = zone['id']
        if zone_name == cf_domain:
            cf_zone_id = zone_id
            break
    if cf_zone_id is None:
        logger.error( "Domain '{}' not found".format( cf_domain ) )
        sys.exit(1)

    # Get the record corresponding to the zone
    if cf_record == '@':
        domain = cf_domain
    else:
        domain = cf_record + '.' + cf_domain
    results = get_paginated_results(
        'GET',
        CLOUDFLARE_URL + '/zones/' + cf_zone_id + '/dns_records',
        auth_header,
    )
    cf_record_obj = None
    for record in results:
        record_id = record['id']
        record_name = record['name']
        if record_name == domain:
            cf_record_obj = record
            break
    if cf_record_obj is None:
        logger.error( "Record '{}' not found".format( domain ) )
        sys.exit(1)

    # Update the record if needed
    if not cf_record_obj['content'] == public_ip or not cf_record_obj['proxied'] == cf_proxied or not cf_record_obj['ttl'] == cf_ttl and not cf_record_obj['proxied']:
        update( auth_header, cf_zone_id, cf_record_obj, public_ip, cf_ttl, cf_proxied )
    else:
        logger.info( "Record '{}' unchanged".format( domain ) )

# Update function
def update( auth_header, cf_zone_id, cf_record_obj, public_ip, cf_ttl, cf_proxied ):
    cf_record_obj['content'] = public_ip
    cf_record_obj['ttl'] = cf_ttl
    cf_record_obj['proxied'] = cf_proxied
    r = requests.put(
        CLOUDFLARE_URL
            + '/zones/'
            + cf_zone_id
            + '/dns_records/'
            + cf_record_obj['id'],
        headers=auth_header,
        json=cf_record_obj
    )
    if r.status_code < 200 or r.status_code > 299:
        logger.error( "Cloudflare responded with unintended status code: {}".format( r.status_code ) )
        sys.exit(1)
    else:
        logger.info( "Record '{}' updated to IP: {}".format( cf_record_obj['name'], public_ip ) )

# Get paginated results function
def get_paginated_results( method, url, auth_header ):
    results = []
    page = 0
    total_pages = None
    while page != total_pages:
        page += 1
        r = requests.request(
            method,
            url,
            params= { 'page': page },
            headers = auth_header
        )
        if r.status_code < 200 or r.status_code > 299:
            logger.error( "Cloudflare responded with unintended status code: {}".format( r.status_code ) )
            sys.exit(1)
        data = r.json()
        results.extend( data['result'] )
        total_pages = data['result_info']['total_pages']
    return results

# Main
if __name__ == '__main__':
    main()
