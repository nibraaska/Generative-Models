import requests
import os
from bs4 import BeautifulSoup
from IPython.display import clear_output

dir = "/home/nibraas/Coding/GenerativeModels/StyleTransfer/degas/"


def update_progress(progress, episode):
    bar_length = 50
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = "Episode {0}, Progress: [{1}] {2:.1f}%".format(episode, "=" * block + "." * (bar_length - block), progress * 100)
    print(text)


def main():
	URL = "https://www.wikiart.org/en/edgar-degas/all-works/text-list"
	links = []

	r = requests.get(url=URL)
	c = r.content
	soup = BeautifulSoup(c, 'html.parser')
	paintings = soup.findAll("li", {"class": "painting-list-text-row"})

	for p in paintings:
		links += [[p.find('a').getText(), "https://www.wikiart.org" + str(p.find('a')['href'])]]


	for ind, link in enumerate(links):
		r = requests.get(url=link[1])
		c = r.content
		soup = BeautifulSoup(c, 'html.parser')
		p = soup.findAll("img", {"itemprop": "image"})

		src = ""
		file_name = dir + link[0].replace(' ', '')

		count = 0
		while os.path.exists(file_name):
			file_name += "_" + count
			count += 1
		file_name += ".jpg"

		for image in p:
			src = image['src']
		if src != "":
			img = requests.get(src)	
			if img.status_code == 200:
				f = open(file_name, 'wb')
				f.write(img.content)
				f.close()

		update_progress(ind / len(links), ind)
main()		
