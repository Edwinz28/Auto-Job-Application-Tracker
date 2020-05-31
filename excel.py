#Pandas xlsxwriter
import pandas as pd

#Data containers
import data
import constants

def add_new():
    print("Appending to excel spread sheet...")
    append_dates = data.date
    append_titles = data.title
    append_company = data.company
    append_url = data.url
    append_skills = data.skills
    try:
        #Appends new data with old
        prev_df = pd.read_excel('Applications.xlsx')
        
        prev_dates = prev_df['Date'].tolist()
        prev_titles = prev_df['Job Title'].tolist()
        prev_company = prev_df['Company'].tolist()
        prev_url = prev_df['Url'].tolist()
        prev_skills = prev_df['Skills'].tolist()
        
        append_dates = prev_dates + data.date
        append_titles = prev_titles + data.title
        append_company = prev_company + data.company
        append_url = prev_url + data.url
        append_skills = prev_skills + data.skills
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

    for col, info in enumerate(df.columns.values):
        worksheet.write(0, col +1, info, header_format)

    writer.save()
