#Web Scraping
from bs4 import BeautifulSoup as soup

#Webclient
from urllib.request import urlopen as uReq

import sys

#Web posting class
from posting import Posting

#Data Containers
import constants
import data

def scrape():
    '''
    Driving function to web scrape

    Parameters:
        None

    Returns:
        None
    '''
    #Loads urls
    print("Running Auto Job Application Tracker")
    print("Attempting to open insert.txt")
    try:
        new_applications = open("Config/Insert.txt", "r")
        urls = new_applications.read().splitlines()
        new_applications.close()

        total = len(urls)
        if total == 0:
            print("Insert.txt is empty, please make sure you save the file before running this script.")
            print("Exiting script...")
            sys.exit(1)
        else:
            print("Found {} Urls, proceeding to scrape data".format(total))

        for num, job_url in enumerate(urls, 1):
            print("--------------------------------")
            print("Parsing application {}/{}".format(num, total))
            try:
                #Open connection to job url
                uClient = uReq(job_url)

                #Html Parsing
                page_soup = soup(uClient.read(), "html.parser")
                
                uClient.close()
            except:
                print("Incorrect url, please check: {}".format(job_url))
                empty = Posting(url=job_url)
                empty.set_empty()
                empty.append()
            else:
                #Creates appropriate posting object 
                if "indeed" in job_url:
                    ad = Posting("INDEED", job_url, page_soup, constants.INDEED_TITLE_TAG, constants.INDEED_TITLE_CLASS, constants.INDEED_COMPANY_TAG, constants.INDEED_COMPANY_CLASS, constants.INDEED_LOC_TAG, constants.INDEED_LOC_CLASS)
                elif "linkedin" in job_url:
                    ad = Posting("LINKEDIN", job_url, page_soup, constants.LINKEDIN_TITLE_TAG, constants.LINKEDIN_TITLE_CLASS, constants.LINKEDIN_COMPANY_TAG, constants.LINKEDIN_COMPANY_CLASS, constants.LINKEDIN_LOC_TAG, constants.LINKEDIN_LOC_CLASS)
                elif "workopolis" in job_url:
                    ad = Posting("WORKOPOLIS", job_url, page_soup, constants.WORKOPOLIS_TITLE_TAG, constants.WORKOPOLIS_TITLE_CLASS, constants.WORKOPOLIS_COMPANY_TAG, constants.WORKOPOLIS_COMPANY_CLASS, constants.WORKOPOLIS_LOC_TAG, constants.WORKOPOLIS_LOC_CLASS)
                elif "glassdoor" in job_url:
                    ad = Posting("GLASSDOOR", job_url, page_soup, constants.GLASSDOOR_TITLE_TAG, constants.GLASSDOOR_TITLE_CLASS, constants.GLASSDOOR_COMPANY_TAG, constants.GLASSDOOR_COMPANY_CLASS, constants.GLASSDOOR_LOC_TAG, constants.GLASSDOOR_LOC_CLASS)
                else:
                    print("URL not supported")
                    continue

                ad.find_data()
                ad.find_skills()
                ad.append()

    except FileNotFoundError:
        print("File does not exist, creating that file now...")
        print("Please copy your URLs into 'insert.txt'")
        new_applications = open("Config/Insert.txt", "w")
        print("Exiting script...")
        sys.exit(1)


