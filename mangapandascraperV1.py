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


manga_domain = 'www.mangapanda.com'
series_name = 'one-piece'

issue_name = 'Groggy Ring'

''' Range of issues to get '''
start_issue_number = sys.argv[1]
end_issue_number = sys.argv[2]

print 'Start Number:%s end Number:%s' % (start_issue_number , end_issue_number)
'''
Location to save the issues
'''
save_directory = '/home/royka/Desktop/' + series_name + '/'


current_issue = int(start_issue_number)

while current_issue <= end_issue_number:
	''' scrape an issue '''
	
	page_number = 1
	found_all_pages = True
	

	print 'scraping issue ' + str(current_issue) + ' ' + issue_name

	issue_directory = save_directory  + str(current_issue) + ' ' + issue_name
	os.makedirs(issue_directory)
	
	

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
	
	''' find the next issue name, bit of a mangle '''
	first_page = urllib.urlopen('http://www.mangapanda.com/' + series_name + '/'+ str(current_issue) + '/' + str(page_number))
	first_soup = BeautifulSoup(first_page)
	bottomchapter = first_soup.find("div" , {"id": "bottomchapter"})
	mangainfo_bas = bottomchapter.find("div" , {"id": "mangainfo_bas"})
	tag =  mangainfo_bas.findAll('td')[1]
	issue_name =  str(str(tag).split(':')[1][:-5].strip())

	current_issue+=1
