from __future__ import print_function
import httplib2
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, timedelta

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

import os
import pytz

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]
APPLICATION_NAME = 'Google Calendar API Python'

class google_calendar_api:

    def build_service(self):
        BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        credential_dir = os.path.join(BASE_DIR, 'credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'python-calendar-api.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_event(self, calendar_id, start, **kwargs):

        credentials = google_calendar_api.build_service(self)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        event = service.events().insert(calendarId=calendar_id, body={
            'start':{'dateTime':  datetime.isoformat(start)},
            'end':{'dateTime':  (start+timedelta(minutes=60)).isoformat()},
        }).execute()
        for property, values in kwargs.items():
            event[property] = values
            updated_event = service.events().update(calendarId=calendar_id, eventId=event['id'],
                                                    body=event).execute()
        return event['id']

    def update_event(self,calendar_id, event_id, **kwargs):
        credentials = google_calendar_api.build_service(self)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        for property,values in kwargs.items():
            if (property=='end') or (property=='start'):
                values = datetime.isoformat(values)
                event[property] ={'dateTime':(values)}
                updated_event = service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()
            else:
                event[property] = values
                updated_event = service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()


