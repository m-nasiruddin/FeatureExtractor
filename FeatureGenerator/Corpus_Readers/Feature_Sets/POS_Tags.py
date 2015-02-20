#!/usr/bin/python
__author__ = 'Mohammad'

import os
import shutil


def pos_tag_features(full_sentence_info_list):
    """pos-tag features (takes a range (left and right) and prints pos-tag info, without the target word)"""
    # Open a file
    shutil.rmtree('../dataset/output')  # removes a directory with sub directories and files
    os.mkdir('../dataset/output')  # creates a new directory
    output_file = open('../dataset/output/jurry.pos.txt', 'a')  # open a file in append mode

    # for full_sentence_info in full_sentence_info_list:  # iterates ove the values (sentence_info(s)) list
    full_sentence_info = iter(full_sentence_info_list)  # explicitly create an iterator, use the built-in iter function
    full_sentence_info = full_sentence_info.next()  # fetch first value

    output_file.write('SENSE\t')  # sense id header
    for token_index, token_info_val in enumerate(full_sentence_info, start=1):  # iterates over the values
        # (sentence_info(s)) list
        output_file.write('A' + str(token_index) + '\t')  # writes the header with numbers
    output_file.write('\n')  # writes a newline

    for full_sentence_info in full_sentence_info_list:  # iterates ove the values (sentence_info(s)) list
        for token_info_val in full_sentence_info:  # iterates over the values (sentence_info(s)) list
            if token_info_val.lemma == 'jury':  # HARDCODED: search for a lemma and pos-tags in keys
                output_file.write(token_info_val.lexsn)
                for token_info_val2 in full_sentence_info:  # iterates over the values (sentence_info(s)) list
                    output_file.write(token_info_val2.pos + '\t')  # prints the pos-tag info
                output_file.write('\n')  # writes a newline
    # Close opend file
    output_file.close()  # closes the file