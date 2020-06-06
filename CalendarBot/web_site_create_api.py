import google.oauth2.credentials
from googleapiclient.discovery import build
import datetime
from flask import session, Blueprint, request, jsonify

blueprint = Blueprint('create_event_api', __name__)


@blueprint.route('/create_event/<name_event>/<description_event>/<color_event>/<day_month_year_event>/<time_event>', methods=['GET'])
def create_event(name_event, description_event, color_event, day_month_year_event, time_event):
    if 'credentials' not in session:
        return jsonify({'error': 'error need authorization'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['name_event', 'description_event', 'color_event',
                                               'day_month_year_event', 'time_event']):
        return jsonify({'error': 'not all elements are transferred!'})

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=credentials)

    GMT_OFF = '+03:00'
    time_start, time_end = get_time(time_event)
    new_event = {'summary': name_event,
                 'description': description_event,
                 'colorId': int(color_event),
                 'start': {
                     'dateTime': f'{get_day_month_year_event(day_month_year_event)}T{time_start}%s' % GMT_OFF},
                 'end': {'dateTime': f'{get_day_month_year_event(day_month_year_event)}T{time_end}%s' % GMT_OFF}}
    new_event = service.events().insert(calendarId='primary', body=new_event).execute()
    return jsonify({'success': 'reminder created'})


def get_day_month_year_event(day_month_year_event):
    day, month, year = day_month_year_event.split('.')
    if len(day) < 2:
        day = '0' + day
    if len(month) < 2:
        month = '0' + month
    return f'{year}-{month}-{day}'


def get_time(time_event):
    time_start, time_end = time_event.split('-')
    time_start += ':00'
    time_end += ':00'
    return time_start, time_end


@blueprint.route('/get_events')
def get_events():
    #  print(session)
    if 'credentials' not in session:
        return 'Error'

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + '+03:00'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return 'Напоминания получены'
