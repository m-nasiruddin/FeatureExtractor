__author__ = 'Mohammad'


def __stopwords_loader__(filename):
    """This load the stopwords from a file (each stop-word per line)."""
    stoplist = list()
    stopwords = open(filename, "r")
    stopwordsstring = stopwords.read()
    for stopword in stopwordsstring.split("\n"):
        stoplist.append(stopword)
    return stoplist