import requests
import os
import tarfile
import shutil
import urllib
import argparse

from BeautifulSoup import BeautifulSoup


MANGA_DOMAIN = 'http://www.mangapanda.com'


def get_issue_name(series_name, issue_number):
    '''
    Find the name of a issue of
    the manga via it's issue number

    :param series_name: name of the manga
    :param issue_number: issue number to find
    :returns: the issue name
    '''
    resp = requests.get(MANGA_DOMAIN + '/' + series_name +
                        '/' + str(issue_number) + '/1')

    soup = BeautifulSoup(resp.text)
    bottomchapter = soup.find("div", {"id": "bottomchapter"})
    mangainfo_bas = bottomchapter.find("div", {"id": "mangainfo_bas"})
    tag = mangainfo_bas.findAll('td')[1]
    return str(str(tag).split(':')[1][:-5].strip())


def scrape_issue(series_name, issue_number, save_directory):
    '''
    Scrape a given issue of a series
    save it to a given folder based
    on the issue name, then convert
    that folder to a 'cbz'

    :param series_name: name of the manga
    :param issue_number: issue number to find
    :param save_directory: directory to save to
    '''
    issue_name = get_issue_name(series_name, issue_number)
    issue_directory = '%s%s/%s_%s' % (save_directory,
                                      series_name, issue_number, issue_name)
    os.makedirs(issue_directory)

    page_number = 1

    issue_url = u'{0}/{1}/{2}/'.format(MANGA_DOMAIN, series_name, issue_number)

    while True:
        page_url = issue_url + str(page_number)
        response = requests.get(page_url)

        if response.ok:
            # end of the issue
            break

        # find the image url
        soup = BeautifulSoup(response.text)
        image_div = soup.find("div", {"id": "imgholder"})
        image_src = image_div.img.get('src')

        # save the image
        urllib.urlretrieve(image_src, issue_directory +
                           '/' + str(page_number) + '.jpg')

        page_number += 1

    # compress the new folder to a .cbz
    compress_tar = tarfile.open(issue_directory + ".cbz", "w:gz")
    compress_tar.add(issue_directory)
    compress_tar.close()

    # delete the folder
    shutil.rmtree(issue_directory)


if __name__ == "__main__":
    '''
    Scrape an Manga from mangapanda and save it as a .CBZ
    '''
    parser = argparse.ArgumentParser(description='Scrape Some Manga')
    parser.add_argument('start', type=int, help='start issue number')
    parser.add_argument('end', type=int, help='end issue number')
    parser.add_argument('name', type=str, help='name of manga')
    parser.add_argument('folder', type=str, help='folder path to output to path (inlude trailing /)')

    args = parser.parse_args()
    series_name = args.name
    start_issue_number = args.start
    end_issue_number = args.end
    save_directory = args.folder

    current_issue_number = start_issue_number

    print('Start Number:{0} end Number:{1}'.format(start_issue_number, end_issue_number))
    while current_issue_number <= end_issue_number:

        print('Scraping Issue: {0}'.format(current_issue_number))
        scrape_issue(series_name, current_issue_number, save_directory)

        current_issue_number += 1
