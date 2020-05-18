#Web Scraping
from bs4 import BeautifulSoup as soup

#Webclient
from urllib.request import urlopen as uReq

#Current Date
from datetime import datetime

#Output to excel
import xlsxwriter


#Loads urls
new_applications = open("Insert.txt", "r")
urls = new_applications.read().splitlines()
new_applications.close()


#Excel
workbook = xlsxwriter.Workbook('Applications.xlsx')
worksheet = workbook.add_worksheet()

#set column widths
#Date
worksheet.set_column('A:A', 30)
#Job Title
worksheet.set_column('B:B', 30)
#Company
worksheet.set_column('C:C', 30)
#URL
worksheet.set_column('D:D', 30)

#set bold
bold = workbook.add_format({'bold':True})

#Headers
worksheet.write(0,0,"Date", bold)
worksheet.write(0,1,"Job Title", bold)
worksheet.write(0,2,"Company", bold)
worksheet.write(0,3,"URL", bold)


row = 1
for x in urls:
    #Stores current url being iterated
    job_url = x

    #Open connection to job url
    uClient = uReq(job_url)

    #Html Parsing
    page_soup = soup(uClient.read(), "html.parser")

    uClient.close()

    #Stores relevant data to a job
    job_data = list()
    job_data.append(str(datetime.date(datetime.now())))
    job_data.append(page_soup.find("h3", class_= "jobsearch-JobInfoHeader-title").text)
    job_data.append(page_soup.find("div", class_= "icl-u-lg-mr--sm icl-u-xs-mr--xs").text)
    job_data.append(x)

    for col, data in enumerate(job_data):
        if col == 3:
            worksheet.write_url(row, col, data, string='Job URL')
        else:
            worksheet.write(row, col, data)

    row +=1


    print("------------------------------------------")
    print(job_data)

    

workbook.close()

