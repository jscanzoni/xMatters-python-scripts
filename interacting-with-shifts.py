#################################################################
##
##      Python Script to access xMatters API to:
##          1. retrive shifts from a particular group
##          2. delete old shifts
##          3. create a new shift
##          4. add members to the shift
##
#################################################################

print '\n\n\n--START SCRIPT--\n\n\n'

############################
#settings
############################

group = 'Daily + Off Hours'             #set to group that needs to be modified

############
#imports
############

import time
import requests
from requests.auth import HTTPBasicAuth
import json

############################
#authenticate
############################

settings = json.load(open('auth.json')) #if auth.json doesn't exist, copy auth.json.sample
base_URL = 'https://'+settings['instance']+'/api/xm/1' 
auth = HTTPBasicAuth(settings['username'], settings['password'])
headers = {'Content-Type': 'application/json'}


############################
#get shifts from group
############################

print '\n\n--ORIGINAL SHIFT LIST--\n\n'

endpoint_URL = '/groups/' + group + '/shifts'
url = base_URL + endpoint_URL 
response = requests.get(url, auth=auth)

if (response.status_code == 200):
    
    print 'Retrieved ' + str(response.json()['count']) + ' of ' + str(response.json()['total']) + " shifts"          
    print '\n'
    for shift in response.json()['data']:
        print shift['name']
    print '\n\n'

    #loop through again and delete all shifts 
    #TODO: might want to add criteria for after x date

    for shift in response.json()['data']:
        print 'DELETING: ' + shift['name']

        endpoint_URL = '/groups/'+group+'/shifts/'+shift['name']
        url = base_URL + endpoint_URL
        response = requests.delete(url, auth=auth)

        responseCode = response.status_code
        if (responseCode == 200):
            print '\tDeleted shift ' +  shift['name']
        elif (response.status_code == 204):
            print '\tThe shift could not be found.'
        else: #debug delete shift
            print '\n\n\n'+str(response.json())+'\n\n\n'

else: #debug retrieve shifts
    print '\n\n\n'+str(response.json())+'\n\n\n'




####################
#create a shift
####################

print '\n\n--CREATE SHIFT--\n\n'

endpoint_URL = '/groups/' + group + '/shifts'
url = base_URL + endpoint_URL

data = {
    'name': 'Brand new shift created - ' + str(time.time()),
    'description' : 'created via API',
    'start' : '2018-04-24T13:00:00.000Z', #must be in UTC
    'end' : '2018-04-24T22:00:00.000Z', #must be in UTC
    'timezone' : 'US/Eastern', #this is a shift setting, but does not affect the passed-in "start" and "end"
    'recurrence' : {
        "frequency" : 'ONCE'
    }
}
data_string = json.dumps(data)

response = requests.post(url, headers=headers, data=data_string, auth=auth)

if (response.status_code == 201):
    print 'Created shift ' + response.json().get('name') + '. ID = ' + response.json().get('id')

    #add members by (username)
    print '\n\n--ADD USERS--\n\n'

    endpoint_URL = '/groups/'+group+'/shifts/'+response.json().get('name')+'/members'
    url = base_URL + endpoint_URL

    data = {
            'position': 1,
            'inRotation' : True,
            'recipient' : {                       
                'id': 'ksmith',
                'recipientType': 'PERSON'
                }
            }
    
    data2 = {
            'position': 2,
            'delay': 15,
            'escalationType': 'Peer',
            'inRotation' : True,
            'recipient' : {                       
                'id': 'bafflac',
                'recipientType': 'PERSON'
                }
            }

    data_string = json.dumps(data)

    response = requests.post(url, headers=headers, data=data_string, auth=auth)

    if (response.status_code == 200):
        rjson = response.json()
        print 'Added member ' + rjson.get('recipient').get('id')
    else: #debug add member
        print '\n\n\n'+str(response.json())+'\n\n\n'
        print str(data_string)+'\n\n\n'

    data_string = json.dumps(data2)

    response = requests.post(url, headers=headers, data=data_string, auth=auth)

    if (response.status_code == 200):
        rjson = response.json()
        print 'Added member ' + rjson.get('recipient').get('id')
    else: #debug add member
        print '\n\n\n'+str(response.json())+'\n\n\n'
        print str(data_string)+'\n\n\n'


else: #debug shift
    print '\n\n\n'+str(response.json())+'\n\n\n'
    print str(data_string)+'\n\n\n'





################################
#re-list shifts from group
################################

print '\n\n--CURRENT SHIFT LIST--\n\n'

endpoint_URL = '/groups/' + group + '/shifts'
url = base_URL + endpoint_URL 
response = requests.get(url, auth=auth)

if (response.status_code == 200): 
    print 'Retrieved ' + str(response.json()['count']) + ' of ' + str(response.json()['total']) + " shifts"          
    print '\n'
    for shift in response.json()['data']:
        print shift['name']
    print '\n\n'
else: #debug retrieve shift
    print '\n\n\n'+str(response.json())+'\n\n\n'
    print str(data_string)+'\n\n\n'








#these are great for debugging
#prints out the response code and the json passed onto the API
'''
print '\n\n\n'+str(response.json())+'\n\n\n'
print str(data_string)+'\n\n\n'
'''



#read groups
#not needed for this script, but commented out if needed
'''
endpoint_URL = '/groups'
url = base_URL + endpoint_URL 
response = requests.get(url, auth=auth)

if (response.status_code == 200):
    json = response.json()
    print ("Retrieved " + str(json['count']) + " of " +  str(json['total']) + " groups.")
    for d in json['data']:
        print d['targetName']
'''