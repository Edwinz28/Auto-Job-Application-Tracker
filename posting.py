#Web Scraping
from bs4 import BeautifulSoup as soup

#Webclient
from urllib.request import urlopen as uReq

#Current Date
from datetime import datetime

#Global Lists
import data

#Job Posting Class
class Posting:

    company = str()
    title = str()
    skills = str()
    location = str()

    def __init__(self, site_type=None, url=None, page_soup=None, title_tag=None, title_class=None, company_tag=None, company_class=None, loc_tag=None, loc_class=None):
        self.type = site_type
        self.url = url
        self.page = page_soup
        self.title_tag = title_tag
        self.title_class = title_class
        self.company_tag = company_tag
        self.company_class = company_class
        self.loc_tag = loc_tag
        self.loc_class = loc_class

    def find_data(self)-> None:
        '''
        Find general data about the posting: Job Title, Company, Location

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

        #Tries to scrape job location
        try:
            self.location = self.page.find(self.loc_tag, class_ = self.loc_class).text
        except:
            self.location = "Not found"

    def find_skills(self)-> None:
        '''
        Scrapes web page for skills

        Parameters: 
            None
        
        Returns:
            None
        '''
        try:
            f = open("Config/Skills_List.txt", "r")
            skills_list = f.read().splitlines()
            f.close()
            page_txt = self.page.text.lower()

            for x in skills_list:
                if x.lower() in page_txt:
                    self.skills = self.skills + x + " "
            
            if not self.skills:
                self.skills = "Not found"

        except FileNotFoundError:
            print("Skills_List.txt not found, please make a txt file with a list of skills you want to scrape")
    
    def get_hyperlink(self, link, short)-> str:
        '''
        Converts url to excel hyperlink equation

        Parameter:
            Link: The url to be converted
            Short: The short form replacement text

        Returns:
            Excel hyperlink equation in string form
        '''
        #return '=HYPERLINK("{}", "{}")'.format(link, short)
        return '<a href="{}">{}</a>'.format(link,short)

    def append(self)-> None:
        '''
        Appends scrapped data to global lists

        Parameters:
            None
        
        Returns:
            None
        '''
        data.title.append(self.title)
        data.skills.append(self.skills)
        data.company.append(self.company)
        data.url.append(self.url)
        data.location.append(self.location)
        data.date.append(str(datetime.date(datetime.now())))
    
    def set_empty(self)->None:
        '''
        Sets data components to "Not found" for a Posting object with an invalid URL

        Parameters:
            None
        
        Returns:
            None
        '''

        self.title = "Not found"
        self.company = "Not found"
        self.location = "Not found"





