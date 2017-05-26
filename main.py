import smtplib
import config
import quickstart
import httplib2
import os
import re
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

carrierDomain = {
	'alltel': 'sms.alltelwireless.com',
	'at&t': 'txt.att.net',
	'boost': 'sms.myboostmobile.com',
	'republic': 'text.republicwireless.com',
	'sprint': 'messaging.sprintpcs.com',
	'tmobile': 'tmomail.net',
	'uscellular': 'email.uscc.net',
	'verizon': 'vtext.com',
	'virgin': 'vmobl.com'
}

message = """Subject: %s
%s
""" % (config.subject, config.body)

currentList = []

SMTPserver = smtplib.SMTP("smtp.gmail.com",587)
SMTPserver.starttls()
SMTPserver.login(config.email, config.password)


credentials = quickstart.get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                          discoveryServiceUrl=discoveryUrl)

def createList():
	result = service.spreadsheets().values().get(
		spreadsheetId=config.spreadsheet_id, range=config.range_name).execute()

	for entry in result['values']:
		carrier = entry[0].lower()
		number = re.sub(r'\D', '', entry[1])
		currentList.append({carrier:number})

def getNumberEmail(numberObject):
	fullAddress = ''
	number = numberObject.values()
	number = number[0]
	carrier = numberObject.keys()
	carrier = carrier[0]
	try:
		if(carrierDomain[carrier] != None):
			fullAddress = number + '@' + carrierDomain[carrier]
			return fullAddress
	except KeyError:
		print(number + ' does not have a valid carrier. Current carrier is: ' + carrier)
		raise KeyError

def sendToList():
	for number in currentList:
		try:
			print(message)
			SMTPserver.sendmail('Testing',getNumberEmail(number), message)
			print('sending to number')
		except KeyError:
			print('Not valid')

createList()
sendToList()