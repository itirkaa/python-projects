import argparse
from datetime import date, datetime, timedelta

def read_ics(path: str):
    """Read files with extension .ics and return a dictionary.
    :param path: str, path for the .ics file
    :return: dict
    """
    ics_dict = dict()
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split(":")
            ics_dict[key] = value
    return ics_dict


def event_dates(start, end, rules):
    """Returns list of dates between start and end with rules being followed
    :param start: datetime, start date
    :param end: datetime, end date
    :param rules: str, string of rules separated by ;
    :return: list of valid dates
    """
    days = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FRI": 4, "SA": 5, "SU": 6}
    date = start
    dates = []

    rules = rules.split(";")
    rules_dict = dict()
    for rule in rules:
        key, value = rule.split("=")
        rules_dict[key] = value
    
    byday = rules_dict['BYDAY'][:2]
    until = datetime.strptime(rules_dict['UNTIL'], "%Y%m%dT%H%M%S")
    end = min(end, until)
    
    date += timedelta(days = days[byday] - date.weekday())
    while date <= end:
        dates.append(date)
        date += timedelta(days=7)
    
    return dates

  
def print_calendar(date, start_time, end_time, summary, location):
    """Prints the output
    """
    date = datetime.strftime(date, "%B %d, %Y (%a)")
    start_time = datetime.strftime(start_time, "%I:%M %p")
    end_time = datetime.strftime(end_time, "%I:%M %p")
    location = "{{" + location + "}}"
    
    print(f"{date}")
    print('-' * len(date))
    print(f"{start_time} to {end_time}: {summary} {location}\n")


def icsout(data: dict):
    """Funtion to print the data in .ics files for the given range of dates.
    :param data: dict, command line arguments
    """
    start_date = datetime.strptime(data['start'], "%Y/%m/%d")
    end_date = datetime.strptime(data['end'], "%Y/%m/%d")
    
    ics_data = read_ics(data['file'])
    event_start = datetime.strptime(ics_data['DTSTART'], "%Y%m%dT%H%M%S")
    event_end = datetime.strptime(ics_data['DTEND'], "%Y%m%dT%H%M%S")
    
    start = max(start_date, event_start)

    events = [start]
    if 'RRULE' in ics_data:
        events = event_dates(start, end_date, ics_data['RRULE'])
    
    for event in events:
        print_calendar(event, event_start, event_end, ics_data['SUMMARY'], ics_data['LOCATION'])


if __name__=="__main__":
    parser = argparse.ArgumentParser() # Parser to get commad line arguments
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--file")
    data = vars(parser.parse_args()) # Read arguments as dictionary

    icsout(data)