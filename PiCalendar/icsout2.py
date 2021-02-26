import argparse


def read_ics(path: str):
    """Read files with extension .ics and return a dictionary.
    :param path: str, path for the .ics file
    :return: dict
    """
    ics_dict = dict()
    with open(path, 'r') as file:
        for line in file:
            key, value = line.split(":")
            ics_dict[key] = value
    return ics_dict


if __name__=="__main__":
    parser = argparse.ArgumentParser() # Parser to get commad line arguments
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--file")
    kwargs = vars(parser.parse_args()) # Read arguments as dictionary

    ics_data = read_ics(kwargs['file'])
    print(ics_data)