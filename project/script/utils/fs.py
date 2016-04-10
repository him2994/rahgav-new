import re

def clean_filename(filename):
    """ Removes illegal characters  from file name. """
    #return re.sub("[\\/:\"\*\?<>|]", "_", filename.strip())
    return re.sub("[^a-zA-Z0-9\. -+_]", "_", filename.strip())