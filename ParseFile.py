import csv
import copy
import pandas as pd
import os

asc_directory = ""
csv_directory = "" # make sure there is a slash at the end
is_primary = True # make sure to change or else there will be issues if there is more than party primary for the same race, it is possible to do this automatically by seeing if the string "PRI" is in the directory, but then this won't work if the BOE doesn't include that substring, so I'm not implemented that way b/c I will forgot that I did it, and then wonder why my code doesn't work
entire_file = []
fields_of_file = []
contests = []
superior_formatting = False # true makes data suitable for making choropleths, also gets rid of over and under votes. false just takes the ASC and does an almost direct conversion to an CSV.


field_definitions = [
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
    # "District name", # This may be referred to as a district on some mapping websites. On Datawrapper, make sure to use the DISTRICT option instead of ID and to use this value.
    "Town",
    "AD",
    "ED"
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
    fields.append(fields[-1][0:1])
    fields.append(fields[-2][1:3])
    fields.append(fields[-3][3:6])
    return fields

with open(asc_directory, 'r') as asc_file:
    entire_file = asc_file.readlines() # split ascii files in list of strings where each string is a line

for line in entire_file: # turn string of line --> list of substrings in line based on defined character placement in PDF (Election results/ASCII File Specs Preinct Detail Text No Groups.pdf)
    fields_of_file.append(line_parser(line))

fields_table = pd.DataFrame(fields_of_file, columns = field_definitions)

for field_definition in field_definitions[:4] + field_definitions[:-2]: # gets rid of leading zeroes in first four columns and last two that can occur, note that columns with just zeroes in them will appear blank now
    fields_table[field_definition] = fields_table[field_definition].str.replace(r'^0+(\d*)$', r'\1', regex=True)

results_directory = csv_directory + "Election results/" + os.path.basename(asc_directory[:-4]) + "/"

dfs = dict(tuple(fields_table.groupby('Contest number')))

if not os.path.exists(results_directory):
    os.mkdir(results_directory)

for contest in dfs:
    candidate_tables = dict(tuple(dfs[contest].groupby('Candidate number')))
    if len(candidate_tables) > 1 and superior_formatting:
        for candidate in candidate_tables:
            new_column_name = candidate_tables[candidate]["Candidate name"].iloc[0] + " votes"
            print(new_column_name)
            candidate_tables[candidate].rename(columns = {'Number of registered voters or number of voters':new_column_name}, inplace = True)
            candidate_tables[candidate].reset_index(drop=True, inplace=True)
        superior_table = pd.concat(candidate_tables, axis = 1)
        superior_table.columns = superior_table.columns.droplevel() # fix weird multi-index issue post concatenation
        superior_table = superior_table.T.drop_duplicates().T
        superior_table = superior_table[superior_table.columns.drop(list(superior_table.filter(regex='Candidate number')))]
        superior_table = superior_table[superior_table.columns.drop(list(superior_table.filter(regex='Candidate name')))]

        # reordering table
        col_names = superior_table.columns.tolist()
        col_names = col_names[0:2] + col_names[3:9] + col_names[2:3] + col_names[9:]
        superior_table = superior_table[col_names]

        superior_table = superior_table.replace("", 0) # replaces all blank votes cells with zeroes
        # superior_table.iloc[:,8:] = superior_table.iloc[:,8:].apply(lambda x: x.str.strip()).replace('', 0) # does the same thing as the above line but is less efficient. i'm keeping it in just in case i screwed something up with the above line.
        superior_table["Total votes"] = superior_table.iloc[:,8:8+len(candidate_tables)-2].astype(int).sum(axis=1) # these do not include over and under votes as they are all spoiled ballots

        candidate_tables.popitem() # removes under and over votes from candidate tables dictionary since we no longer need them for percent calculation
        candidate_tables.popitem() 

        for candidate in candidate_tables:
            superior_table[candidate_tables[candidate]["Candidate name"].iloc[0] + " pct"] = superior_table[candidate_tables[candidate]["Candidate name"].iloc[0] + " votes"].astype(int) / superior_table["Total votes"]

        if is_primary:
            superior_table.to_csv(results_directory + fields_table.loc[fields_table["Contest number"] == contest, "Party code"].iloc[0] + " " + fields_table.loc[fields_table["Contest number"] == contest, "Contest title"].iloc[0] + ".csv")
        else:
            superior_table.to_csv(results_directory + fields_table.loc[fields_table["Contest number"] == contest, "Contest title"].iloc[0] + ".csv")
    else:
        if is_primary:
            dfs[contest].to_csv(results_directory + fields_table.loc[fields_table["Contest number"] == contest, "Party code"].iloc[0] + " " + fields_table.loc[fields_table["Contest number"] == contest, "Contest title"].iloc[0] + ".csv")
        else:
            dfs[contest].to_csv(results_directory + fields_table.loc[fields_table["Contest number"] == contest, "Contest title"].iloc[0] + ".csv")
