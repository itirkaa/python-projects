import argparse
from datetime import date, datetime, timedelta

def read_ics(path: str):
    """Read files with extension .ics and return a dictionary.
    :param path: str, path for the .ics file
    :return: list of dictionaries
    """
    events = list()
    ics_dict = dict()
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split(":")
            ics_dict[key] = value
            if key=='END':
                events.append(ics_dict)
                ics_dict = dict()
    return events[:-1]


def event_dates(start, end, rules=None):
    """Returns list of dates between start and end with rules being followed
    :param start: datetime, start date
    :param end: datetime, end date
    :param rules: str, string of rules separated by ;
    :return: list of valid dates
    """
    days = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
    date = start
    dates = []
    if rules:
        rules = rules.split(";")
        rules_dict = dict()
        for rule in rules:
            key, value = rule.split("=")
            rules_dict[key] = value
        
        byday = rules_dict['BYDAY'][:2]
        until = datetime.strptime(rules_dict['UNTIL'], "%Y%m%dT%H%M%S")       
        date += timedelta(days = days[byday] - date.weekday())
        while date <= until:
            dates.append(date)
            date += timedelta(days=7)
    else:
        dates.append(date) 
    return dates

  
def event_details(start_time, end_time, summary, location):
    """Prints the output
    """
    start_time = datetime.strftime(start_time, "%I:%M %p")
    end_time = datetime.strftime(end_time, "%I:%M %p")
    location = "{{" + location + "}}"
    
    return f"{start_time} to {end_time}: {summary} {location}\n"

def print_calendar(calendar, start, end):
    """Print the events in calendar is proper format.
    :param calendar: 
    """
    for date in sorted(calendar.keys()):
        if date < start.date():
            continue
        if date > end.date():
            break
        date_str = datetime.strftime(date, "%B %d, %Y (%a)")
        print(date_str)
        print("-" * len(date_str))
        print("\n".join(calendar[date]))


def icsout(data: dict):
    """Funtion to print the data in .ics files for the given range of dates.
    :param data: dict, command line arguments
    """
    start_date = datetime.strptime(data['start'], "%Y/%m/%d")
    end_date = datetime.strptime(data['end'], "%Y/%m/%d")
    
    events = read_ics(data['file'])    
    calendar = dict()
       
    for event in events:
        event_start = datetime.strptime(event['DTSTART'], "%Y%m%dT%H%M%S")
        event_end = datetime.strptime(event['DTEND'], "%Y%m%dT%H%M%S")
        
        start = max(start_date, event_start)

        dates = event_dates(start, end_date, event.get('RRULE'))
        
        info = event_details(event_start, event_end, event['SUMMARY'], event['LOCATION'])

        for date in dates:
            date = date.date()
            if date in calendar:
                calendar[date].append(info)
            else:
                calendar[date] = [info]
    print_calendar(calendar, start_date, end_date)


if __name__=="__main__":
    parser = argparse.ArgumentParser() # Parser to get commad line arguments
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--file")
    data = vars(parser.parse_args()) # Read arguments as dictionary

    icsout(data)