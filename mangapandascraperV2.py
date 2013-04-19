'''
Better Manga Parser

Scapes manga from mangapanda.com

'''
import urllib
from bs4 import BeautifulSoup
import os
import tarfile
import shutil
import sys

MANGA_DOMAIN = 'www.mangapanda.com'


def get_issue_name(series_name , current_issue ):
	'''
	Get the issue name for current issue

	mangle
	'''
	first_page = urllib.urlopen('http://www.mangapanda.com/' + series_name + '/'+ str(current_issue) + '/1')
	soup = BeautifulSoup(first_page)
	bottomchapter = soup.find("div" , {"id": "bottomchapter"})
	mangainfo_bas = bottomchapter.find("div" , {"id": "mangainfo_bas"})
	tag =  mangainfo_bas.findAll('td')[1]
	return str(str(tag).split(':')[1][:-5].strip())


def scrape_issue(series_name , issue_number):
	'''
	Scrape a given issue of a series
	'''
	print 'scraping issue ' + str(current_issue) + ' ' + issue_name

	issue_directory = save_directory  + str(current_issue) + ' ' + issue_name
	os.makedirs(issue_directory)


	page_number = 1
	found_all_pages = True
	
	while found_all_pages:

		page = urllib.urlopen('http://www.mangapanda.com/' + series_name + '/'+ str(current_issue) + '/' + str(page_number))

		if page.code == 200:

			''' find the image url '''
			soup = BeautifulSoup(page)
			image_div = soup.find("div", {"id": "imgholder"})
			image_src = image_div.img.get('src')

			''' save the image '''
			urllib.urlretrieve(image_src, issue_directory+ '/' + str(page_number) + '.jpg')

			page_number+=1

		else:
			found_all_pages = False


	''' compress the new folder to a .cbz'''
	compressTar = tarfile.open(issue_directory + ".cbz", "w:gz")
	compressTar.add(issue_directory)
	compressTar.close()

	''' delete the folder '''
	shutil.rmtree(issue_directory)



if __name__ == "__main__":
	'''
	Scrape an Manga from mangapanda

	Args Required

	1) Series_Name i.e one-piece
	2) start_number
	3) end_number
	4) save directory

	'''
	series_name = str(sys.argv[1])
	start_issue_number = int(sys.argv[2])
	end_issue_number = int(sys.argv[3])
	save_directory = str(sys.argv[4])

	current_issue = start_issue_number

	print 'Start Number:%s end Number:%s' % (start_issue_number , end_issue_number)
	
	#save_directory = '/home/royka/Desktop/%s/' % series_name
	while current_issue <= end_issue_number:

		

		current_issue+=1


	

	'''
	Location to save the issues
	'''
	