#Pandas xlsxwriter
import pandas as pd

#Data containers
import data
import constants

class Excel:
    #Cell properties
    firstCell = 'C1'
    largestCol = "F"

    #Dataframe data structures
    dfDates = list()
    dfTitles = list()
    dfCompany = list()
    dfLocation = list()
    dfSkills = list()
    dfUrls = list()

    def __init__(self):
        #Loads previous data in excel into dataframe
        try:
            df_old = pd.read_excel('Applications.xlsx')
            self.dfDates = df_old['Date'].tolist()
            self.dfTitles = df_old['Job Title'].tolist()
            self.dfCompany = df_old['Company'].tolist()
            self.dfUrls = df_old['Url'].tolist()
            self.dfSkills = df_old['Skills'].tolist()
            self.dfLocation = df_old['Location'].tolist()
        except:
            print("No previous data found")
    
    def get_last_row(self, df)-> int:
        '''
        Finds the last row (in row number)

        Parameters:
            df: Pandas dataframe

        Return:
            int: The number of the last row
        '''
        return int(df.size / 6) + 1
    
    def get_df_range(self, df)->str:
        '''
        Gets dataframe range in the form of A1:F1

        Parameters:
            df: The dataframe to analyze

        Returns:
            Str: a string of the dataframe range
        '''
        return self.firstCell + ':' + self.largestCol + str(self.get_last_row(df))
    
    def append_df_elements(self)-> None:
        '''
        Appends old data points in dataframe with new points. This function updates data structures in Excel class

        Parameters:
            None
        
        Returns:
            None

        '''

        self.dfDates += data.date
        self.dfTitles += data.title
        self.dfCompany += data.company
        self.dfLocation += data.location
        self.dfSkills += data.skills
        self.dfUrls += data.url

    def create(self)-> None:
        '''
        Main driving function to create the excel spreadsheet

        Parameters:
            None
        
        Returns:
            None
        '''
        print("Writing to Application.xlsx")

        self.append_df_elements()

        #Writes to excel
        df = pd.DataFrame({'Date': self.dfDates, 'Job Title': self.dfTitles, 'Company': self.dfCompany, 'Location': self.dfLocation, 'Skills':self.dfSkills, 'Url': self.dfUrls})
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
        worksheet.set_column('F:F', 30)


        red_format = workbook.add_format({'bg_color':'red'})
        worksheet.conditional_format(self.get_df_range(df), {'type': 'text',
                                        'criteria': 'containing',
                                        'value':     'Not found',
                                        'format': red_format})
        for col, info in enumerate(df.columns.values):
            worksheet.write(0, col +1, info, header_format)

        writer.save()
