import requests
from time import sleep
from pathlib import Path
import re

### THIS IS NOT WORKING YET!

def checkheader(url):
    try:
        if requests.head(url).headers:
            return True 
    except:
        return False

def read_blocklist():
    p = Path(__file__).parent
    URLS = set()
    for filename in p.glob('*.txt'):
        print(f'######## {filename.name} #########\n')
        with open(filename) as fh:
            for url in fh:
                url = url.strip()
                URLS.add(url)
                # print(url)
    return URLS

def page_content(url):
    # url_dedup = set()
    try:
        page = requests.get(url)
        if page.status_code == 200:   
            for line in page.content.decode().strip():#.split():
                if line.startswith('#') or line == "":
                    continue
                if line.startwith('0.0.0.0'):
                    line = line.split()[-1]
                # url_dedup.append(line)
                yield line
    except:
        print(f'Bad URL {url}')
    
            # if checkheader(line):
            #     print(f'Active {line}')

def main():
    dedup_url = set()
    for site_list in read_blocklist():
        for url in page_content(site_list):
            dedup_url.add(url)

    path = Path(__file__).resolve().parents[1]
    output = path / 'blocklist' / 'pihole_blocklist.txt'
    
    with open(output, 'w') as fh:
        for site in dedup_url:
            fh.write(f'0.0.0.0   {site}\n')
    print('*'*25)
    print(f'Total in block list  {len(dedup_url)}')
    print(f'File written to {output}')
    print('*'*25)

# url = 'https://www.github.developerdan.com/hosts/lists/facebook-extended.txt'
# page_content(url)

if __name__ == "__main__":
    main()