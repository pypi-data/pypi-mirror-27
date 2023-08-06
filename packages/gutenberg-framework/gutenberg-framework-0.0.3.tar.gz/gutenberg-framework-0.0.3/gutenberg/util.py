import dateutil.parser as parser;

def isDate(string):
    if not isinstance(string, str):
        return False;
    try:
        parser.parse(string);
        return True;
    except ValueError:
        return False;
