# xMatters Python Scripts
Various scripts for working with the xMatters API via Python. 

<kbd>
  <img src="https://github.com/xmatters/xMatters-Labs/raw/master/media/disclaimer.png">
</kbd>

# Pre-Requisites
* Python 2.7
* xMatters account - If you don't have one, [get one](https://www.xmatters.com)!

# Files
* [interacting-with-shifts.py](interacting-with-shifts.py) - A sample script to retrive shifts from a particular group, delete old shifts, create a new shift, and add members to the shift.
* [auth.json](auth.sample.json) - This file defines the instance and credentials for accessing the xMatters API.

# Installation

## Authentication File
1. Rename or copy `auth.sample.json` to `auth.json`.
2. Edit instance and credentials in `auth.json`.

## Python Setup
1. Basic python setup information can be found online.
2. You may need to install `HTTPBasicAuth` by running `pip install HTTPBasicAuth` in your terminal.
3. You can use `pip` to install any other missing libraries as well.

# Testing
As always, make sure to develop and test these scripts on a non-production environment. Running this code unmodified in production could have unintended consequences.

# Troubleshooting
Add this code anywhere you need to see the raw response from the API -- great for troubleshooting connection or data formatting issues.
```python
print '\n\n\n'+str(response.json())+'\n\n\n'
print str(data_string)+'\n\n\n'
```
