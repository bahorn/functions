from datetime import datetime
import requests
import pytz
from icalendar import Calendar, Event
from bs4 import BeautifulSoup
from flask import make_response

calendar_summary = """
Unofficial iCalendar for the Information and Computing Sciences Colloquium at \
Utrecht University.

Maintained by b.a.a.horn AT students DOT uu DOT nl
"""


def ics_daterange(datestr):
    day, time = datestr.split('\n')
    start, end = time.split(' – ')

    start = datetime.strptime(
        f"{day} {start}",
        '%A, %d.%m.%Y %H:%M'
    ).replace(tzinfo=pytz.timezone('Europe/Amsterdam'))
    end = datetime.strptime(
        f"{day} {end}",
        '%A, %d.%m.%Y %H:%M'
    ).replace(tzinfo=pytz.timezone('Europe/Amsterdam'))

    return (start, end)


def ics_ical():
    url = 'https://icsc.sites.uu.nl/schedule/'

    r = requests.get(url)

    page = BeautifulSoup(r.text, features="html5lib")
    rows = []

    for table in page.find_all('table'):
        # Check if this is the table containing the events.
        if table.find('th').text != "Date":
            continue
        rows = table.find_all('tr')[1::]
        break

    cal = Calendar()
    cal.add('name', 'ICS Colloquium')
    cal.add('dtstamp', datetime.now())
    cal.add('summary', calendar_summary)
    cal['dtstart'] = '20200101T000000'

    cal.add('prodid', '-//ICS Colloquium//ics.sites.uu.nl//')
    cal.add('version', '2.0')

    for row in rows:
        event = Event()
        date, location, speaker = map(lambda x: x.text, row.find_all('td'))
        event.add('location', location)
        event.add('summary', speaker)
        start, end = ics_daterange(date)
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now())
        uid = f'{start.isoformat()}-{location}@ics.sites.uu.nl'
        event.add('uid', uid)
        cal.add_component(event)

    return cal.to_ical()


def calendar_req(request):
    response = make_response(
        ics_ical()
    )

    response.headers['Content-Type'] = 'text/calendar'

    return response


if __name__ == "__main__":
    print(ics_ical())
