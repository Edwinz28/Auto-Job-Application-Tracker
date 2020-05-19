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

def find_data(page_soup, title_tag, title_class, company_tag, company_class):
    find_company = str()
    find_title = str()
    try:
        find_title = page_soup.find(title_tag, class_= title_class).text
        title.append(find_title)                  
    except:
        print("Job title not found")
    try:
        find_company = page_soup.find(company_tag, class_= company_class).text
        company.append(find_company)
    except:
        print("Company info not found")
    
    return find_title and find_company

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
                print("Exiting script...")
                sys.exit(1)

            #Stores relevant data to a job
            date.append(str(datetime.date(datetime.now())))
            url.append(job_url)

            #For now, we try each site until we find values

            #Try indeed
            if find_data(page_soup, constants.INDEED_TITLE_TAG, constants.INDEED_TITLE_CLASS, 
                        constants.INDEED_COMPANY_TAG, constants.INDEED_COMPANY_CLASS):
                print("Success!")
                continue
            else:
                print("Data not found, please enter them manually")
                title.append("N/A")
                company.append("N/A")

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

    try:
        #Appends new data with old
        prev_df = pd.read_excel('Applications.xlsx')
        
        prev_dates = prev_df['Date'].tolist()
        prev_titles = prev_df['Job Title'].tolist()
        prev_company = prev_df['Company'].tolist()
        prev_url = prev_df['Url'].tolist()
        
        append_dates = prev_dates + date
        append_titles = prev_titles + title
        append_company = prev_company + company
        append_url = prev_url + url
    except:
        print("Application.xlsx not found, no data to append.")
        print("Creating Application.xlsx and continuing with inserting data...")
    
    #Writes to excel
    df = pd.DataFrame({'Date': append_dates, 'Job Title': append_titles, 'Company': append_company, "Url": append_url})
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
print("Script completed. Happy job hunting!")