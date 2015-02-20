__author__ = 'Mohammad'

import re
import string


def __surrounding_words_without_stopwords__(locs, stoplist, feature_list, window_file):
    """This generates the surrounding words feature set with the (maximum number of words) surrounding words in a given
    context, except not considering stopwords, punctuations, numbers and the target word. Please see the
    NUSPTSemEval2007 system for more info."""
    regex_is_number = re.compile(r'^\-?[0-9]+\.?[0-9]*')
    lnnumber = 0
    contexts = list()
    target_indices = list()
    min_window = 0
    max_window = 0

    for ln in range(0, len(feature_list)):
        line = feature_list[ln]
        lnnumber += 1
        current_features = line.split('"\t"')
        # Removing heading and training quote characters
        current_features[0] = current_features[0][1:len(current_features[0])]
        current_features[len(current_features) - 1] = \
            current_features[len(current_features) - 1][0:len(current_features[len(current_features) - 1]) - 1]
        features_without_stopwords = list()
        i = 0
        trgwindex = locs[ln]
        while i != len(current_features):
            if ((current_features[i].lower() not in stoplist) or (
                    current_features[i].lower() in stoplist and i != trgwindex)) and \
                            regex_is_number.match(current_features[i]) is None and \
                            current_features[i].lower()[0] not in string.punctuation:
                features_without_stopwords.append(current_features[i])
            else:
                if i <= trgwindex:
                    trgwindex -= 1
            i += 1
        if (trgwindex - 1 > min_window):
            min_window = trgwindex - 1
        if len(features_without_stopwords) - trgwindex > max_window:
            max_window = len(features_without_stopwords) - trgwindex
        target_indices.append(min(len(features_without_stopwords) - 1, max(0, trgwindex)))
        contexts.append(features_without_stopwords)
    outlist = list()
    window_file.write("\t" + str(min_window) + "\t" + str(max_window) + "\n");
    for j in range(0, len(contexts)):
        c = contexts[j]
        output_string = ""
        for i in range(target_indices[j] - min_window + 1, target_indices[j] + max_window):
            if i >= 0 and i < len(c):
                if i != target_indices[j]:
                    output_string += '\"' + c[i] + '\"\t'
            else:
                output_string += '\"0\"\t'
        output_string += '\n'
        outlist.append(output_string)
    return outlist