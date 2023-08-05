### To setup a virtual environment
> $ pip install virtualenv

> $ virtualenv --python=/path/to/python venvpy36

### To activate the virtual environment
>  $ source venvpy36/bin/activate (for Linux)

> $ venvpy36\Scripts\activate (for Windows)

### To install the package
> $ pip install negconvert

### To run the package
> $ negconvert unalteredTweets.csv

### To deactivate the virtual environment
> $ venvpy36\Scripts\deactivate.bat (for Windows)

### Input file
The input file has the following requirements:
- Is a comma delimited csv file
- The header includes these fields: user,text,date,state,takeFlushot,negativeFlushot
- The date format is yyyyMMdd (e.g. 20140109)
- takeFlushot and negativeFlushot are flags, which have the value of 0 or 1

### Output files
#### 1. _freq.csv
This file contains the frequency of the words in the text. This file is only used for word normalization.
#### 2. _converted.csv
This file contains the original text and the converted text.
