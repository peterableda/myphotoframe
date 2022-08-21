from __future__ import print_function
import os 
import pickle
import json
import sys
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_httplib2  # This gotta be installed for build() to work

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
token_path = '/home/pi/myphotoframe/token.pickle'
if os.path.exists(token_path):
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds:
    sys.exit('No credentials available.') # The token generation can't work on raspberry

if not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

google_photos = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# Call the Photo v1 API
results = google_photos.albums().list(
    pageSize=10, fields="nextPageToken,albums(id,title)").execute()
items = results.get('albums', [])
if not items:
    print('No albums found.')
else:
    print('Albums:')
    for item in items:
        print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))


day, month, year = ('0', '6', '2019')  # Day or month may be 0 => full month resp. year
date_filter = [{"day": day, "month": month, "year": year}]  # No leading zeroes for day an month!
nextpagetoken = 'Dummy'
while nextpagetoken != '':
    nextpagetoken = '' if nextpagetoken == 'Dummy' else nextpagetoken
    results = google_photos.mediaItems().search(
            body={"filters":  {"dateFilter": {"dates": [{"day": day, "month": month, "year": year}]}},
                  "pageSize": 10, "pageToken": nextpagetoken}).execute()
    # The default number of media items to return at a time is 25. The maximum pageSize is 100.
    items = results.get('mediaItems', [])
    nextpagetoken = results.get('nextPageToken', '')
    for item in items:
            print(f"{item['filename']} {item['mimeType']} '{item.get('description', '- -')}'"
                      f" {item['mediaMetadata']['creationTime']}\nURL: {item['productUrl']}")