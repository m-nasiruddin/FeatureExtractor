__author__ = 'Mohammad'


def __argument_parser__(features):
    """This parse the input arguments."""
    mincolval = list()
    maxcolval = list()
    minposval = 0
    maxposval = 0
    singlewords = False
    ftrvalues = features.split("_")
    for ftrvalue in ftrvalues:
        if "c" in ftrvalue:
            colvals = ftrvalue.split(".")
            for colval in colvals:
                colposs = colval.split("c")
                cols = colposs[1].split(",")
                mincolval.append(int(cols[0]))
                maxcolval.append(int(cols[1]))
        elif "p" in ftrvalue:
            posposs = ftrvalue.split("p")
            poss = posposs[1].split(",")
            for pos in poss:
                if "-" in pos:
                    minposval = int(poss[0])
                    pos = pos.replace("-", "")
                    minposabsval = int(pos)
                else:
                    pos = pos.replace("+", "")
                    maxposval = int(pos)
        elif "all" in ftrvalue:
            singlewords = True
    return [singlewords, mincolval, maxcolval, minposval, maxposval]