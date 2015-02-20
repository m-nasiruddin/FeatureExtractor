import os
import argparse
import shutil

import FeatureExtractorSemCor


def __process__(srcdir):
    """This function processes the feature arguments."""
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
    * [features] = [c-1,-1.c+1,+1.c-2,-2.c+2,+2.c-2,-1.c-1,+1.c+1,+2.c-3,-1.c-2,+1.c-1,+2.c+1,+3_p-3,+3_all]
                = name of the features (according to the feature order)
        [c-N-N] = Lemma/word-form (lower-cased) of the N-th local collocation words before the target word
        [c-N+N] = Lemma/word-form (lower-cased) of the N-th local collocation words before and after the target word
        [c+N-N] = Lemma/word-form (lower-cased) of the N-th local collocation words after and before the target word
        [c+N+N] = Lemma/word-form (lower-cased) of the N-th local collocation words after the target word
        [p-N] = POS-tag of the N-th word before the target word
        [p+N] = POS-tag of the N-th word after the target word
        [all] = All single words/uni-grams (lemma/word-form lower-cased; except, stop-words, numbers and punctuation
                symbols) in the surrounding context

Example:
    python BatchFeatureExtractor.py -i semcor/semcor3.0 -o semcor_features -f
    c-1,-1.c+1,+1.c-2,-2.c+2,+2.c-2,-1.c-1,+1.c+1,+2.c-3,-1.c-2,+1.c-1,+2.c+1,+3_p-3,+3_all''')

parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('-o', '--output', help='Output file name', required=True)
parser.add_argument('-f', '--features', help='Feature names', required=True)
args = parser.parse_args()

# # show values ##
srcdir = args.input
srcdirpath = os.path.abspath(srcdir)

dstdir = args.output
dstdirpath = os.path.abspath(dstdir)

featurenames = args.features

retout = ""

if os.path.exists(dstdirpath):
    print("The destination directory already exists, backing up in " + dstdirpath + "_output")
    if os.path.exists(dstdirpath + "_backup"):
        shutil.rmtree(dstdirpath + "_backup")
    shutil.copytree(dstdirpath, dstdirpath + "_backup")
    shutil.rmtree(dstdirpath)

os.makedirs(dstdirpath)
if os.path.exists(srcdirpath):
    retout = __process__(srcdirpath)
else:
    print("The source directory does not exist!")
    exit(1)

print("Extracting features ...")
FeatureExtractorSemCor.__feature_extractor__(retout, dstdirpath, featurenames)