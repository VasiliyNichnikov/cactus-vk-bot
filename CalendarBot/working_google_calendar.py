# from __future__ import print_function
import pickle
import os.path

import gflags
# from apiclient.discovery import build
from oauth2client.tools import run_flow
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class WorkingGoogleCalendarAPI:
    def __init__(self):
        self.creds = None

    # ручная инициализация пользователя
    def manual_init_user(self, user_id):
        if os.path.exists(f'CalendarBot/token_{user_id}.pickle'):
            with open(f'CalendarBot/token_{user_id}.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # flow = run_flow('CalendarBot/credentials.json', SCOPES)
                flow = InstalledAppFlow.from_client_secrets_file('CalendarBot/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
                # print(flow.redirect_uri)
                # print(self.creds)
            with open(f'CalendarBot/token_{user_id}.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def create_event(self, name_event, description_event, color_event, day_month_year_event, time_event):
        service = build('calendar', 'v3', credentials=self.creds)
        # service = build(serviceName='calendar', version='v3', http=self.http,
        #                 developerKey='AI6456456456456456456456456456yKhI')
        GMT_OFF = '+03:00'
        time_start, time_end = self.get_time(time_event)
        new_event = {'summary': name_event,
                     'description': description_event,
                     'colorId': int(color_event),
                     'start': {'dateTime': f'{self.get_day_month_year_event(day_month_year_event)}T{time_start}%s' % GMT_OFF},
                     'end': {'dateTime': f'{self.get_day_month_year_event(day_month_year_event)}T{time_end}%s' % GMT_OFF}}
        new_event = service.events().insert(calendarId='primary', body=new_event).execute()
        print('Напоминание создано!')

    def get_day_month_year_event(self, day_month_year_event):
        day, month, year = day_month_year_event.split('.')
        if len(day) < 2:
            day = '0' + day
        if len(month) < 2:
            month = '0' + month
        return f'{year}-{month}-{day}'

    def get_time(self, time_event):
        time_start, time_end = time_event.split('-')
        time_start += ':00'
        time_end += ':00'
        return time_start, time_end
