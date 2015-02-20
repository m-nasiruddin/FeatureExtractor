import os
import argparse

import FeatureExtractor


def __process__(srcdir):
    out = ""
    names = os.listdir(srcdir)
    for name in names:
        srcfpath = srcdir + "/" + name
        if os.path.isdir(srcfpath):
            print("Processing the directory - " + name + " ...")
            out += __process__(srcfpath)
        else:
            print("Processing the file - " + name + " ...")
            infile = open(srcfpath, "r")
            filestr = infile.read()
            if "<s snum=1>" in filestr:
                out += filestr
            infile.close()
    return out


parser = argparse.ArgumentParser(description='''Command to run the script:
    python BatchFeatureExtractor.py -i [source] -o [destination] -f [features]

Explanation:
    * [source] = Name of the source directory
    * [destination] = Name of the destination directory
    * [features] = [l-3_l+1_t-1_t+2_tw_twt] = name of the features (according to your feature order)
        [l-N] = Lemma of the N-th word before the target word
        [l+N] = Lemma of the N-th word after the target word
        [t-N] = Morphological tag of the N-th word before the target word
        [t+N] = Morphological tag of the N-th word after the target word
        [tw] = Target word
        [twt] = Morphological tag of the target word

Example:
    python BatchFeatureExtractor.py -i semcor/semcor3.0 -o semcor_features -f l-3_l+1_t-1_t+2_tw_twt''')

parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('-o', '--output', help='Output file name', required=True)
parser.add_argument('-f', '--features', help='Feature names', required=True)
args = parser.parse_args()

## show values ##
srcdir = args.input
srcdirpath = os.path.abspath(srcdir)

dstdir = args.output
dstdirpath = os.path.abspath(dstdir)

featurenames = args.features

retout = ""
if not os.path.exists(dstdirpath):
    os.makedirs(dstdirpath)
    if os.path.exists(srcdirpath):
        retout = __process__(srcdirpath)
    else:
        print("The source directory is not exist!")
else:
    print("The destination directory is already exist!")

print("Extracting the features ...")
FeatureExtractor.__featureextractor__(retout, dstdirpath, featurenames)