#Pandas xlsxwriter
import pandas as pd

import matplotlib.pyplot as plt

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
    
    def format(self, workbook, worksheet, df, smWidth, width, lgWidth, headerCol, highlightCol )->None:
        '''
        Formats excel to present the information in an organized manner

        Parameters:
            Workbook: xlsx workbook
            Worksheet: xlsx worksheet
            df: working dataframe
            smWidth: width of normal cols
            lgWidgth: width of larger columns
            headerCol: color of header
            highlightCol: cell highlight color
        
        Returns:
            None
        '''
                
        #header format
        header_format = workbook.add_format({'bg_color':headerCol,'bold':True, 'border':1})

        #Column format
        worksheet.set_column('B:B', smWidth)
        worksheet.set_column('C:E', width)
        worksheet.set_column('F:G', lgWidth)
    
        format1 = workbook.add_format({'bg_color':highlightCol})
        worksheet.conditional_format(self.get_df_range(df), {'type': 'text',
                                        'criteria': 'containing',
                                        'value':     'Not found',
                                        'format': format1})
        for col, info in enumerate(df.columns.values):
            worksheet.write(0, col +1, info, header_format)
    
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
        
    def plot_activity(self, df)-> None:
        '''
        Plots the user's application activity on a line graph

        Parameters:
            df: The excel dataframe that contains at the minimum a 'Date' series

        Returns:
            None
        '''
        temp = pd.DataFrame({'Date':df['Date']})
        temp['Date'] = temp['Date'].astype("datetime64")
        graph = temp.groupby([temp['Date'].dt.year, temp['Date'].dt.month, temp['Date'].dt.day]).count().plot()

        #Graph Labels
        plt.title("My Application Activity")
        plt.ylabel('# Of Applications')
        plt.xlabel('Date')
        graph.get_legend().remove()
        plt.savefig('Graphs/Activity.png')

    def plot_companies(self, df)-> None:
        '''
        Plots the user's application distribution by company

        Parameters:
            df: The excel dataframe that contains at the minimum a 'Company' series

        Returns:
            None
        '''
        temp = pd.DataFrame({'Company':df['Company']})
        temp = temp['Company'].value_counts().reset_index().rename(columns={'index': 'Company', 'Company': 'Count'})

        x = temp['Company'].values
        y = temp['Count'].values

        fig = plt.figure()
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.set_xlabel("Company")
        axes.set_ylabel("# Of Applications")
        axes.set_title("Applications Distribution By Company")

        axes.bar(x,y)
        fig.savefig('Graphs/Companies.png')
    
    def plot_locations(self, df)-> None:
        '''
        Plots the user's application distribution by company

        Parameters:
            df: The excel dataframe that contains at the minimum a 'Company' series

        Returns:
            None
        '''
        temp = pd.DataFrame({'Location':df['Location']})
        temp = temp['Location'].value_counts().reset_index().rename(columns={'index': 'Location', 'Location': 'Count'})

        x = temp['Location'].values
        y = temp['Count'].values

        fig = plt.figure()
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.set_xlabel("Location")
        axes.set_ylabel("# Of Applications")
        axes.set_title("Applications Distribution By Job Location")

        axes.bar(x,y)
        fig.savefig('Graphs/Locations.png')

    def plot_skills_distribution(self, df)-> None:
        
        #Creates tally of common skills required
        def count_skills(skills):
            skill_list = skills.split()
            for s in skill_list:
                data.add_to_skillsDB(s)

        df['Skills'].apply(count_skills)

        x = list()
        y = list()
        for key, val in data.skillsDB.items():
            x.append(key)
            y.append(val)

        fig = plt.figure()
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.set_xlabel("Skill")
        axes.set_ylabel("Count")
        axes.set_title("Common Skills Required For My Applications")

        axes.bar(x,y)
        fig.savefig('Graphs/Skills_Distribution.png')

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

        #Graphs
        self.plot_activity(df)
        self.plot_companies(df)
        self.plot_locations(df)
        self.plot_skills_distribution(df)



        

        

        #Formats excel
        self.format(workbook, worksheet, df, 10, 30, 50, '#919190', '#e84a3f')
        
        writer.save()
