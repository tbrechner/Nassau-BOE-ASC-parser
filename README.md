# Nassau BOE ASC parser

The Nassau County Board of Elections sucks. They barely ever respond to FOIAs, and when they do, they are nothing short of intentionally incompetent. When you ask for simple elections data by precinct they provide these horrible .ASC files that can drive you mad figuring them out even though the manual for their voting machine says they can provide CSVs. Thankfully, I have automated the process in converting them to readable CSV files. I have foiled your evil plans of restricting election information to county committees Nassau BOE!

Make sure to configure the `asc_directory` and `csv_directory` with relevant paths on your computer. Also, this parser requires the Python library pandas.
