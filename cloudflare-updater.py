import requests
import sys
import json

"""
GET STARTED:
See README.md
https://github.com/corleyscotte/cloudflare-updater
"""

# User Configuration Values
CLOUDFLARE_GLOBAL_API_KEY = '<REPLACE_WITH_YOUR_GLOBAL_API_KEY>'
CLOUDFLARE_ZONE_ID = '<REPLACE_WITH_YOUR_CLOUDFLARE_ZONE_ID>'
CLOUDFLARE_EMAIL = '<REPLACE_WITH_YOUR_CLOUDFLARE_EMAIL>'
SUBDOMAINS_TO_UPDATE = ['connect', 'vpn', 'home']
DOMAIN = '<REPLACE_WITH_YOUR_DOMAIN.TLD>'


# App Variables
cloudflare_base_url = 'https://api.cloudflare.com/client/v4/'
headers = {
           'X-Auth-Email': CLOUDFLARE_EMAIL,
           'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
           'Content-Type': 'application/json'
          }


def getPublicIP():
    """ Get public IP address of system

    :return: public IP
    :rtype: str
    """
    public_ip = requests.get('https://api.ipify.org').text
    return public_ip


def getZoneRecords():
    """ Get CloudFlare Zone Records

    Get zone records for zone specified in user config varibles
    :return: DNS Records
    :rtype: list(dict)
    """
    dns_records = []
    url = cloudflare_base_url + 'zones/' + CLOUDFLARE_ZONE_ID + '/dns_records'

    try:
        r = requests.get(url, headers=headers).json()
    except requests.exceptions.RequestException as e:
        print(e)
        raise sys.exit(1)

    if r['success']:
        for re in r['result']:
            dns_records.append(re)
    else:
        ecode = str(r['errors'][0]['code'])
        emsg = str(r['errors'][0]['message'])
        print('Response failed with error code '
                + ecode + 'and message: \n' + emsg)

    return dns_records


def updateZoneRecord(id, name, new_ip, type='A', proxied=False):
    """ Update CloudFlare Zone Record

    Cloudflare API requires type, name and content (ip)

    :param id: str CloudFlare unique ID for DNS record
    :param name: str Record name - subdomain.domain.tld
    :param new_ip: str New IP for record
    :param type: str DNS record type - default A
    :param proxied: bool Enable CloudFlare DNS/HTTP Proxy
    :return: Update success
    :rtype: bool
    """
    #TODO: Update requires record to already exist in CloudFlare
    #TODO: Create new record if not already existing

    url = f'{cloudflare_base_url}zones/{CLOUDFLARE_ZONE_ID}/dns_records/{id}'
    data = {
            "type": type,
            "name": name,
            "content": new_ip,
            "proxied": proxied
            }
    data = json.dumps(data)
    r = requests.put(url, headers=headers, data=data).json()

    if r['success']:
        return True
    else:
        ecode = str(r['errors'][0]['code'])
        emsg = str(r['errors'][0]['message'])
        print('Update failed with error code '
                + ecode + 'and message: \n' + emsg)
        return False


def filterRecords(zone_records, subdomains):
    """ Filter zone records for subdomains to update

    Find record id, name, type, ip for SUBDOMAINS_TO_UPDATE

    :param zone_records: list(dict) All records for specified user zone
    :param name: list Subdomains in FQDN format
    :return: Records to update
    :rtype: list
    """
    records = []
    for r in zone_records:
        for s in subdomains:
            if r['name'] == s:
                record = {
                    "id": r['id'],
                    "name": r['name'],
                    "type": r['type'],
                    "content": r['content'],
                    "proxied": r['proxied'],
                }
                records.append(record)
    return records


def main():
    """ Main Function - Updates CloudFlare records to system's public IP """
    #TODO: Add logging functionality

    # Get your public IP
    my_ip = getPublicIP()

    # Format subdomains to fully qualified domain name (FQDN)
    subdomains = [sd + '.' + DOMAIN for sd in SUBDOMAINS_TO_UPDATE]
    zone_records = getZoneRecords()

    # Records we want to update
    to_update = filterRecords(zone_records, subdomains)

    # Update subdomains to your public IP address
    for t in to_update:
        id = t.get('id')
        name = t.get('name')
        new_ip = my_ip
        updateZoneRecord(id, name, new_ip)


if __name__ == "__main__":
    main()
