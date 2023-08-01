import csv
import copy
from IPython.display import display
import pandas as pd

entire_file = []
fields_of_file = []
contests = []
dateOfElection = "08-23-2022" # format however you want - i like MM-DD-YYYY

field_definitons = [
    "Contest number",
    "Candidate number",
    "Precinct code",
    "Number of registered voters or number of voters",
    "Party code",
    # "District type ID", # SEE field_idxs FOR WHY THIS IS COMMENTED OUT
    # "District code",
    "Contest title",
    "Candidate name",
    "Precinct name",
    # "District name"
    ]
field_idxs = [
       (0,4), # Contest number
       (4,7), # Candidate number
       (7, 11), # Precinct code
       (11, 17), # Number of registered voters or number of voters
       (17, 20), # Party code
       # (20, 23), # District type ID - DOES NOT SEEM TO EXIST, KEEP IT HERE IN CASE THEY USE IT IN THE FUTURE
       # (23, 27), # District code - DOES NOT SEEM TO EXIST, KEEP IT HERE IN CASE THEY USE IT IN THE FUTURE
       (27, 83), # Contest title
       (83, 121), # Candidate name
       (121, 151), # Precinct name
       # (151, 176) # District name - DOES NOT SEEM TO EXIST, KEEP IT HERE IN CASE THEY USE IT IN THE FUTURE
       ]

def line_parser(line):
   fields = []
   for beg,end in field_idxs:
       fields.append(line[beg:end].strip())
   return fields

# six digits - first one is unknown, next two are AD, next two are ED


with open('../Election results/August2022PRI.ASC', 'r') as asc_file:
    entire_file = asc_file.readlines() # split ascii files in list of strings where each string is a line

for line in entire_file: # turn string of line --> list of substrings in line based on defined character placement in PDF (Election results/ASCII File Specs Preinct Detail Text No Groups.pdf)
    fields_of_file.append(line_parser(line))





print(fields_of_file)


fields_table = pd.DataFrame(fields_of_file, columns = field_definitons)

print(fields_table.columns)

dfs = dict(tuple(fields_table.groupby('Contest number')))

for contest in dfs:
    dfs[contest].to_csv("/Users/tbrec/Documents/DSA work/Electoral/BOE Files/" + contest + "test.csv")

        
with open('DELETEWHENCOMPLETED.txt', 'w') as f:
    f.write('\n'.join(','.join(str(i) for i in x) for x in fields_of_file))

