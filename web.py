#Web Scraping
from bs4 import BeautifulSoup as soup

#Webclient
from urllib.request import urlopen as uReq

#Current Date
from datetime import datetime
import sys

#Data Containers
import constants
import data

class Posting:

    company = str()
    title = str()
    skills = str()

    def __init__(self, site_type, page_soup, title_tag, title_class, company_tag, company_class):
        self.type = site_type
        self.page = page_soup
        self.title_tag = title_tag
        self.title_class = title_class
        self.company_tag = company_tag
        self.company_class = company_class

    def find_data(self):
        '''
        Find general data about the posting: Job Title, Company

        Parameters:
            None
        Returns:
            None
        '''
        #Tries to scrape the job title
        try:
            self.title = self.page.find(self.title_tag, class_= self.title_class).text                
        except:
            self.title = "Not found"

        #Tries to scrape the job company
        try:
            self.company = self.page.find(self.company_tag, class_= self.company_class).text
        except:
            self.company = "Not found"

    def find_skills(self):
        '''
        Scrapes web page for skills

        Parameters: 
            None
        
        Returns:
            None
        '''
        try:
            f = open("Skills_List.txt", "r")
            skills_list = f.read().splitlines()
            f.close()
            page_txt = self.page.text.lower()

            for x in skills_list:
                if x.lower() in page_txt:
                    self.skills = self.skills + x + " "

        except FileNotFoundError:
            print("Skills_List.txt not found, please make a txt file with a list of skills you want to scrape")


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
        new_applications = open("Insert.txt", "r")
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
                print("Skipping this url")
                continue

            #Stores relevant data to a job
            data.date.append(str(datetime.date(datetime.now())))
            data.url.append(job_url)

            if "indeed" in job_url:
                ad = Posting("INDEED", page_soup, constants.INDEED_TITLE_TAG, constants.INDEED_TITLE_CLASS, constants.INDEED_COMPANY_TAG, constants.INDEED_COMPANY_CLASS)
                ad.find_data()
                ad.find_skills()
                data.title.append(ad.title)
                data.skills.append(ad.skills)
                data.company.append(ad.company)
            elif "linkedin" in job_url:
                ad = Posting("LINKEDIN", page_soup, constants.LINKEDIN_TITLE_TAG, constants.LINKEDIN_TITLE_CLASS, constants.LINKEDIN_COMPANY_TAG, constants.LINKEDIN_COMPANY_CLASS)
                ad.find_data()
                ad.find_skills()
                data.title.append(ad.title)
                data.skills.append(ad.skills)
                data.company.append(ad.company)
            else:
                print("URL not supported")

    except FileNotFoundError:
        print("File does not exist, creating that file now...")
        print("Please copy your URLs into 'insert.txt'")
        new_applications = open("Insert.txt", "w")
        print("Exiting script...")
        sys.exit(1)


