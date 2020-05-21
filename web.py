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

def find_data(page_soup, title_tag=None, title_class=None, company_tag=None, company_class=None):
    '''
    Find general data about the posting: Job Title, Company

    Parameters:
        page_soup = BS4 of webpage
        title_tag = HTML tag of the job title
        title_class = HTML class of the job title
        company_tag = HTML tag of the company
        company_class = HTML class of the company
    
    Returns:
        Returns a boolean if the scraping was successful
    '''
    find_title = str()
    find_company = str()
    try:
        find_title = page_soup.find(title_tag, class_= title_class).text   
        data.title.append(find_title)              
    except:
        pass
    try:
        find_company = page_soup.find(company_tag, class_= company_class).text
        data.company.append(find_company)
    except:
        pass
    
    return find_title or find_company

def find_skills(page_soup):
    '''
    Scrapes web page for skills

    Parameters: 
        page_soup = BS4 of webpage
    
    Returns:
        None
    '''
    try:
        f = open("Skills_List.txt", "r")
        skills_list = f.read().splitlines()
        f.close()
        page_txt = page_soup.text.lower()
        temp = ""
        for x in skills_list:
            if x.lower() in page_txt:
                temp = temp + x + " "

        data.skills.append(temp)
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

            #For now, we try each site until we find values
            #Try Indeed
            if find_data(page_soup, constants.INDEED_TITLE_TAG, constants.INDEED_TITLE_CLASS, 
                            constants.INDEED_COMPANY_TAG, constants.INDEED_COMPANY_CLASS):
                pass
            #Try Linkedin
            elif find_data(page_soup, constants.LINKEDIN_TITLE_TAG, constants.LINKEDIN_TITLE_CLASS,
                            constants.LINKEDIN_COMPANY_TAG, constants.LINKEDIN_COMPANY_CLASS):
                pass
            #Try Workopolis
            elif find_data(page_soup, constants.WORKOPOLIS_TITLE_TAG, constants.WORKOPOLIS_TITLE_CLASS,
                            constants.WORKOPOLIS_COMPANY_TAG, constants.WORKOPOLIS_COMPANY_CLASS):
                pass
            #Try Eluta
            elif find_data(page_soup, constants.ELUTA_TITLE_TAG, constants.ELUTA_TITLE_CLASS,
                            constants.ELUTA_COMPANY_TAG, constants.ELUTA_COMPANY_CLASS):
                pass
            #Try WD3
            #elif find_data(page_soup, constants.WD3_TITLE_TAG, constants.WD3_TITLE_CLASS):
                #pass
            #Try Monster
            #elif split_title(page_soup, constants.MONSTER_INFO_TAG, constants.MONSTER_INFO_CLASS, constants.MONSTER_KEYWORD):
                #pass
            #Didnt find data
            else:
                print("Some data not found, please enter them manually")
                data.title.append("Not found")
                data.company.append("Not found")

            
            #Compare dataframe sizes
            if len(data.title) < len(data.url):
                data.title.append("Not found")
            elif len(data.company) < len(data.url):
                data.company.append("Not found")

            find_skills(page_soup)

    except FileNotFoundError:
        print("File does not exist, creating that file now...")
        print("Please copy your URLs into 'insert.txt'")
        new_applications = open("Insert.txt", "w")
        print("Exiting script...")
        sys.exit(1)


