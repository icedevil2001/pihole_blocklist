import requests
import re


## See: https://github.com/StevenBlack/hosts 

def process_host_file(text):
    for line in text.strip().split('\n'):
        if line.startswith('#'):
            continue
        line = line.strip().replace('0.0.0.0 ','')
        if line:
            yield line 
            

def process_url(url):
    # url = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/data/StevenBlack/hosts'
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        for line in process_host_file(req.text):
            yield line
        # content = base64.decodestring(req['content'])


URLS = ['https://raw.githubusercontent.com/StevenBlack/hosts/master/data/StevenBlack/hosts',
        "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt",
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts",
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Dead/hosts",
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts",
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts",
        "https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts",
        "https://raw.githubusercontent.com/bigdargon/hostsVN/master/option/hosts-VN",
        "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt",
        "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/hosts.txt",
        "https://raw.githubusercontent.com/jamiemansfield/minecraft-hosts/master/lists/tracking.txt",
        "https://winhelp2002.mvps.org/hosts.txt",
        "https://raw.githubusercontent.com/shreyasminocha/shady-hosts/main/hosts",
        "https://someonewhocares.org/hosts/zero/hosts",
        "https://raw.githubusercontent.com/tiuxo/hosts/master/ads",
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts",
        "https://urlhaus.abuse.ch/downloads/hostfile/",
        "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&mimetype=plaintext&useip=0.0.0.0"]

filename = "/Users/icedevil2001/Dropbox/Documents/Documents-Priyesh_MacBookPro13/git/pihole_blocklist/blocklist/StevenBlack.txt"

with open(filename, 'w') as fh:
    for url in URLS:
        for line in process_url(url):
            fh.write(line + "\n")