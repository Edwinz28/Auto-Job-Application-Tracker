#Web Scraping
from bs4 import BeautifulSoup as soup
#Webclient
from urllib.request import urlopen as uReq
#Current Date
from datetime import datetime
#Pandas xlsxwriter
import pandas as pd
import sys
#constants
import constants

#Declare data structures
date = list()
title = list()
company = list()
url = list()
skills = list()


def find_data(page_soup, title_tag=None, title_class=None, company_tag=None, company_class=None):
    find_title = str()
    find_company = str()
    try:
        find_title = page_soup.find(title_tag, class_= title_class).text   
        title.append(find_title)              
    except:
        pass
    try:
        find_company = page_soup.find(company_tag, class_= company_class).text
        company.append(find_company)
    except:
        pass
    
    return find_title or find_company

def split_title(page_soup, title_tag, title_class, key_word):
    print("Splitting")
    find_job = str()
    find_company = str()
    find_title = page_soup.find(title_tag, class_= title_class).text
    #print(page_soup.findAll(id="JobViewHeader"))

    print("foo")
    return find_job and find_company


def scrape():
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
            date.append(str(datetime.date(datetime.now())))
            url.append(job_url)

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
                title.append("Not found")
                company.append("Not found")

            
            #Compare dataframe sizes
            if len(title) < len(url):
                title.append("Not found")
            elif len(company) < len(url):
                company.append("Not found")


            #Skills
            f = open("skills.txt", "r")
            skills_list = f.read().splitlines()
            f.close()
            page_txt = page_soup.text.lower()
            temp = ""
            for x in skills_list:
                if x.lower() in page_txt:
                    temp = temp + x + " "
            
            skills.append(temp)

    except FileNotFoundError:
        print("File does not exist, creating that file now...")
        print("Please copy your URLs into 'insert.txt'")
        new_applications = open("Insert.txt", "w")
        print("Exiting script...")
        sys.exit(1)


def add_to_excel():
    print("Appending to excel spread sheet...")
    
    append_dates = date
    append_titles = title
    append_company = company
    append_url = url
    append_skills = skills

    try:
        #Appends new data with old
        prev_df = pd.read_excel('Applications.xlsx')
        
        prev_dates = prev_df['Date'].tolist()
        prev_titles = prev_df['Job Title'].tolist()
        prev_company = prev_df['Company'].tolist()
        prev_url = prev_df['Url'].tolist()
        prev_skills = prev_df['Skills'].tolist()
        
        append_dates = prev_dates + date
        append_titles = prev_titles + title
        append_company = prev_company + company
        append_url = prev_url + url
        append_skills = prev_skills + skills
    except:
        print("Application.xlsx not found, no data to append.")
        print("Creating Application.xlsx and continuing with inserting data...")
    
    #Writes to excel
    df = pd.DataFrame({'Date': append_dates, 'Job Title': append_titles, 'Company': append_company, 'Skills':append_skills, 'Url': append_url})
    df.index += 1
    writer = pd.ExcelWriter("Applications.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Job Applications', startrow=1, header=False)

    workbook = writer.book
    worksheet = writer.sheets['Job Applications']

    #header format
    header_format = workbook.add_format({'bold':True, 'border':1})

    #Column format
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 30)
    worksheet.set_column('E:E', 30)

    for col, data in enumerate(df.columns.values):
        worksheet.write(0, col +1, data, header_format)

    writer.save()


#Main
scrape()
add_to_excel()
print("Script completed. Good luck job hunting!")