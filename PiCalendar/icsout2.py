import argparse
from datetime import date, datetime, timedelta

def read_ics(path: str):
    """Read files with extension .ics and return a dictionary.
    :param path: str, path for the .ics file
    :return: list of dictionaries
    """
    events = list()   # list to store all the events
    ics_dict = dict() # dictionary to store info for given event
    
    # Open .ics file in read mode
    with open(path, 'r') as file:
        # Read lines in the file (skipping 1st and last line)
        for line in file:
            key, value = line.strip().split(":")
            if key=='BEGIN': continue
            elif key=='END':
                # if event ends, add the info to the events list
                events.append(ics_dict)
                ics_dict = dict()
            else:
                ics_dict[key] = value
            
    return events[:-1]


def event_dates(start: datetime, rules: str = None):
    """Returns list of dates between start and end with rules being followed
    :param start: datetime, start date
    :param rules: str, string of rules separated by ;
    :return: list of valid dates
    """
    if not rules:
        return [start]

    date = start
    dates = list()
    days = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}

    rules = rules.split(";") # list of rules
    rules_dict = dict()
    for rule in rules:
        key, value = rule.split("=")
        rules_dict[key] = value
    
    byday = rules_dict['BYDAY'][:2] # Day to repeat the event
    until = datetime.strptime(rules_dict['UNTIL'], "%Y%m%dT%H%M%S")     
    date += timedelta(days = days[byday] - date.weekday()) # Getting date for the day
    
    while date <= until:
        dates.append(date) 
        date += timedelta(days=7) # Updating dates by 7 days

    return dates


def format_details(events: list):
    """Prints the output
    """
    # sorting events by start time
    events = sorted(events, key = lambda k: k['start'].time())
    event_list = list()

    for event in events:
        start = datetime.strftime(event['start'], "%#I:%M %p").rjust(8, " ")
        end = datetime.strftime(event['end'], "%#I:%M %p").rjust(8, " ")
        location = "{{" + event['location'] + "}}"
        event_detail = f"{start} to {end}: {event['summary']} {location}"
        event_list.append(event_detail)
    
    return event_list


def print_calendar(calendar: dict):
    """Print the events in calendar is proper format.
    :param calendar: 
    """
    dates = sorted(calendar.keys())
    for date in dates:
        calendar[date] = format_details(calendar[date])

        date_str = datetime.strftime(date, "%B %d, %Y (%a)")

        print(date_str)
        print("-" * len(date_str))
        print("\n".join(calendar[date]), "\n")


def icsout(data: dict):
    """Funtion to print the data in .ics files for the given range of dates.
    :param data: dict, command line arguments
    """
    start_date = datetime.strptime(data['start'], "%Y/%m/%d")
    end_date = datetime.strptime(data['end'], "%Y/%m/%d")
    
    events = read_ics(data['file']) 
    calendar = dict() # store list of events for a given date
       
    for event in events:
        event_start = datetime.strptime(event['DTSTART'], "%Y%m%dT%H%M%S")
        event_end = datetime.strptime(event['DTEND'], "%Y%m%dT%H%M%S")
        dates = event_dates(event_start, event.get('RRULE')) # Getting all the dates for given event
        # info = event_details(event_start, event_end, event['SUMMARY'], event['LOCATION'])
        details = {
            "start": event_start,
            "end": event_end,
            "summary": event['SUMMARY'],
            "location": event['LOCATION']
        }
        
        for date in dates:
            date = date.date()
            if date < start_date.date() or date > end_date.date(): continue            
            elif date in calendar:
                calendar[date].append(details)
            else:
                calendar[date] = [details]
    
    print_calendar(calendar)


if __name__=="__main__":
    parser = argparse.ArgumentParser() # Parser to get commad line arguments
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--file")
    data = vars(parser.parse_args()) # Read arguments as dictionary

    icsout(data)