import requests
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep

## https://zeltser.com/malicious-ip-blocklists/

headers = 'Url Site_Name Status Date_Added Updated Project'.split()


p  = Path(__file__).parents[1]
blocklist = set()
# pagenum = 1
prev = None 
end = False 
counter = 0
with open( p / 'blocklist' / 'fakebankslist.scaped.txt', 'w') as fh:
	for pagenum in range(1,10000000,20):
		URL = "https://db.aa419.org/fakebankslist.php?start={}".format(pagenum)
		print(URL,counter, end='\r',flush=True)
		page = requests.get(URL)
		if page.status_code != 200:
			break
		if end:
			break
		soup = BeautifulSoup(page.content, 'html.parser')
		c = 0
		for tr in soup.find_all('tr'):
			for num, tb in enumerate( tr.find_all('td') ):
				if num > 0:
					if num == 1:
						blockweb = tb.text
			
						if blockweb == prev:
							print(f'Exiting!! Finished at page: {pagenum}')
							end =True
							break
					if num == 3:
						active = tb.text.strip()
						if active == "active":
							counter +=1
							# print(f'Page Num: {pagenum}\r\n Total sites added: {counter}\r\n Adding: {blockweb}\r',flush=True)
							fh.write('{}\n'.format(blockweb))
		sleep(.5)

				

	
# print('Total urls: ', len(blocklist))
# with open( p / 'blocklist' / 'fakebankslist.scaped.txt', 'w') as fh:
# 	for url in blocklist:
# 		fh.write('{}\n'.format(url))