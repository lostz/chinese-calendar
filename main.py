from datetime import datetime
import time
import requests
iCal = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:中国节假日
PRODID:-//Apple Inc.//macOS 11.2.3//EN
X-APPLE-CALENDAR-COLOR:#711A76
X-WR-TIMEZONE:Asia/Shanghai"""


def get_events_in_year(days,envents):
    for day in days:
        date = time.strftime("%Y%m%d",time.strptime(day['date'],"%Y-%m-%d"))
        name = day['name']
        if day['isOffDay']==True:
            name = name+"放假"
        else:
            name = name+"调休"
        singleEvent =f"""
BEGIN:VEVENT
DTSTART;VALUE=DATE:{date}
DTEND;VALUE=DATE:{date}
SUMMARY:{name}
SEQUENCE:0
END:VEVENT"""
        envents.append(singleEvent)
    return envents


days_this_year =  requests.get('https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{}.json'.format(datetime.now().year)).json()['days']
envents =[]
envents = get_events_in_year(days_this_year,envents)
days_next_year =[]
try:
    days_next_year =  requests.get('https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{}.json'.format(datetime.now().year+1)).json()['days']
except:
    pass
envents = get_events_in_year(days_next_year,envents)
for envent in envents:
    iCal +=envent
iCal += "\nEND:VCALENDAR"

with open("chinese.ics", "w") as w:
	w.write(iCal)


