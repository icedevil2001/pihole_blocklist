#!/usr/bin/env python
import requests
from time import sleep
from pathlib import Path
import re

def readblocklist():
	p = Path(__file__).parent
	fn = p / 'raw_blocklist.txt'
	tmp = set()  ## remove dups
	with open(fn) as fh:
		for f in fh:
			f = f.strip()
			if f.startswith('#') or f == '':
				continue
			tmp.add(f)
	return list(tmp)

def load_whitelist():
	whitelist = set()
	p = Path(__file__).parents[1]
	with open( p / 'whitelist' / 'pihole.whitelist.txt' ) as fh:
		for l in fh:
			l = l.strip()
			whitelist.add(l)
	
	return list(whitelist)

def page_content(url, captured_url, whitelist=load_whitelist()):

	try:
		page = requests.get(url)
		if page.status_code == 200:
			## only for text files
			for line in page.content.decode().strip().split():
				line = line.strip()
				if line in whitelist:
					print('_'*50)
					print('SKIPPING', line)
					print('_'*50)
					continue 
				# r = re.search(r'.*?(smartsheet|notion)', str(line) )
				# if r:
				# 	print("_"*50)
				# 	print(url, line)
				# 	print("_"*50)
				if line.startswith('#') or line == "":
					continue
				else:
					if line.startswith('<'):
						raise ValueError('The url is a html', url)
					else:
						captured_url.add(line)
		else:
			print('Error! page status:',  page.status_code, url)

	except requests.exceptions.Timeout as e:
	    # Maybe set up for a retry, or continue in a retry loop
		print('TimeOut:', e)
	except requests.exceptions.TooManyRedirects as e:
	    # Tell the user their URL was bad and try a different one
		print('TooManyRedirects',e)
	except requests.exceptions.RequestException as e:
	    # catastrophic error. bail.
		print('ERROR! ',e)
    	# raise SystemExit(e)
	

def main():
	path = Path(__file__).resolve().parents[1]	
	output = path / 'blocklist' / 'pihole_blocklist.txt'
	captured_url = set()
	URLS = readblocklist()
	for url in URLS:
		print(url)
		page_content(url, captured_url)
		sleep(0.1)

	captured_url = list(captured_url)
	print('Blocklist contents {} urls'.format(len(captured_url)))
	with open(output, 'w') as fh:
		for site in captured_url:
			fh.write('{}\n'.format(site))
	print('Written to: ', output)

if __name__ == '__main__':
	main()
