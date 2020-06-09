#Global Lists used across multiple files

#Declare data structures
date = list()
title = list()
company = list()
url = list()
skills = list()
location = list()
skillsDB = dict()

def add_to_skillsDB(skill):
    if skill not in skillsDB.keys():
        skillsDB[skill] = 0
    else:
        skillsDB[skill] += 1

