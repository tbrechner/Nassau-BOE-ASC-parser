# Nassau BOE ASC parser

# Data Visualizations

Utilizing the files I parsed, I created [this](https://public.tableau.com/shared/Q7X69RX7F?:display_count=n&:origin=viz_share_link) visualization of results from an August 2022 NY state senate district 7 primary election using Tableau. I also created visualizations on Datawrapper for [an August 2022 NY gubernatorial primary](https://datawrapper.dwcdn.net/7pWT3/6/), [an August 2022 NY Congressional district 3 primary](https://datawrapper.dwcdn.net/fjA27/6/), and [an August 2022 NY state senate district 7 primary](https://datawrapper.dwcdn.net/h3b3e/15/).

The Nassau County Board of Elections provides election data in the form of hard-to-read .asc files. This Python script converts them to CSV files.

Make sure to configure the `asc_directory` and `csv_directory` variables with relevant paths on your computer. Also, this parser requires the Python library pandas.

## Instructions

1. Modify the first two variables to set up your paths.
- `ASC directory` is the directory on your computer where the plain text ASCII file is (this is one that is usually provided by the Nassau BOE).
- `CSV directory` is the directory on your computer where the parsed results will be stored. Make sure to complete this path with a slash (/) at the end in order to allow the data to be saved in the right place. A folder named `Election results` will be created in that directory. These can be the same directory if you would like.
- Below is example code.

```python
asc_directory = "/Users/username/Documents/"
csv_directory = "/Users/username/Documents/BOE Files/" # make sure there is a slash at the end
```
2. Modify the latter two variables to configure which code is going to run.
- Set `is_primary` to `True` if the plain text ASCII file contains results of ANY primary election; otherwise, set it to `False`.
- I recommend always setting `superior_formatting` to `True` as it does not just take the results of the ASCII file and convert them to CSV. It also formats the results such that each candidate's results are on the same line for each precinct and displays the number of total votes in the election and percentages received by each candidate. This is especially helpful if one is creating maps. However, superior formatting currently [does not currently work for general election data](https://github.com/tbrechner/Nassau-BOE-ASC-parser/issues/1), and if any bugs occur, try turning it off; it may fix them.
- Below is a continuation of above's example code curated for this step.

```python
is_primary = True
superior_formatting = True
```
3. Run the code on your IDE or in the Terminal. FYI, I used Python 3.11, but it may work for earlier versions too. Create an issue on this GitHub if you run into any errors.

4. If you are making a map, do not the `ID` criteria to differentiate the precincts. Use the `DISTRICT` criteria—it is linked the `Precinct name` field in the CSV file. Do not use the `Precinct code` field for this purpose (or do, I just can't figure how to use it with the maps I have).
