#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu  7 Sep 15:19:22 CEST 2017


from __future__ import print_function

"""This script evaluates the given score files and computes EER and Spoofing FAR with regards to 10 types of voice attacks"""

import bob.measure

import argparse
import numpy, math
import os
import os.path
import sys

import re

from collections import OrderedDict

import matplotlib.pyplot as mpl
import matplotlib.font_manager as fm

import bob.core

logger = bob.core.log.setup("bob.spoof.speech")


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    OUTPUT_FILE = os.path.join(basedir, 'statistics.txt')

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-t', '--score-types', required=False, nargs='+', default=[],
                        help="The type of the scores, can be a set of values.")
    parser.add_argument('-p', '--parameters', required=False, nargs='+', default=[],
                        help="The parameter for this type of the scores, can be a set of values.")

    parser.add_argument('-d', '--directory', type=str, required=True,
                        help="The the directory prefix with txt files that have FAR and FRR scores.")

    parser.add_argument('-o', '--out-file', type=str, default=OUTPUT_FILE,
                        help="The the directory to ouput the resulted plot (defaults to '%(default)s').")

    parser.add_argument('-s', '--style', required=False, type=str, help="The plot line-style.")

    # add verbose option
    bob.core.log.add_command_line_option(parser)

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    return args


def main(command_line_parameters=None):
    """Reads score files, computes error measures and plots curves."""

    args = command_line_arguments(command_line_parameters)

    #  if not os.path.exists(args.out_directory):
    #    os.makedirs(args.out_directory)

    results_table = OrderedDict()
    db_names = OrderedDict()
    fid = open(args.out_file, "w")
    # fid.write("{\bf Feat.\ type} &  & {\bf DEV Threshold} & {\bf DEV EER (\%)}  & {\bf EVAL HTER (\%)}  \\ \hline \n")
    for score_type in args.score_types:
        # for param in args.parameters:
        cur_dir = args.directory + "_" + score_type
        if not os.path.exists(cur_dir):
            continue
        for fn in sorted(os.listdir(cur_dir)):
            if fn.endswith(".txt"):
                print(cur_dir)
                # print (fn)
                resfile = open(os.path.join(cur_dir, fn), "r")
                text = resfile.read()
                text_lines = text.splitlines()

                title = text_lines[0]
                if 'Development' in text_lines[0]:
                    title = score_type
                # print("Results of " + title + ":")
                m = re.search(r"FAR = (\w+\.\w+)", text)
                far = 100.0 * float(m.group(1))  # the value in parenthesis
                m = re.search(r"FRR = (\w+\.\w+)", text)
                frr = 100.0 * float(m.group(1))  # the value in parenthesis
                m = re.search(r"threshold = (-*\w+\.\w+)", text)
                eer = (far+frr)*0.5
                if not m:
                    continue
                eer_thres = float(m.group(1))  # the value in parenthesis
                # print("far=%.5f, frr=%.5f, eer_thres=%.2f" % (far, frr, eer_thres))

                m = re.search(r"SFAR = (\w+\.\w+)", text)
                sfar = 100.0 * float(m.group(1))  # the value in parenthesis
                m = re.search(r"SFRR = (\w+\.\w+)", text)
                sfrr = 100.0 * float(m.group(1))  # the value in parenthesis
                m = re.search(r"attacks: a:[\'-]*(\w+([-\']*\w+)*)[\'-]*, ad:(\w+)", text)
                if m is not None:
                    type_attack = m.group(1)
                    type_device = m.group(2)
                else:
                    type_attack = 'all'
                    type_device = 'all'
                hter = (sfar + sfrr) * 0.5

                m = re.search(r"Cllr_eval = (\w+\.\w+)", text)
                cllr_eval = float(m.group(1))  # the value in parenthesis
                #
                m = re.search(r"minCllr_eval = (\w+\.\w+)", text)
                minCllr_eval = float(m.group(1))  # the value in parenthesis

                feature_name, db_name = title.split('#')
                # for ISBA Paper PAD
                # table_row = "%.2f" % (sfar)
                table_row = "%.2f & %.2f & %.2f" % (eer, sfar, sfrr)
                if feature_name in results_table:
                    print("appending %s" % db_name )
                    db_names[feature_name].append(db_name + "-" + type_attack)
                    results_table[feature_name].append(table_row)
                else:
                    print("initial %s" % db_name )
                    db_names.update({feature_name: [db_name + "-" + type_attack]})
                    results_table.update({feature_name: [table_row]})

####  The ISBA paper representation #######
    db_column = db_names.keys()
    fid.write("Databases & %s  \\\\ \\hline \n " % " & ".join(db_column))
    fid.write("\hline \n")
    db_names_list = db_names[db_column[0]]
    for i in range(len(db_names_list)):
        # write the name of the db
        fid.write("%s " % (db_names_list[i]))
        for feature_name, values in results_table.items():
            # get only correct range of values
            print(feature_name, values[i])
            fid.write("& %s" % values[i])
        # current_feature_values = results_table[db_column[i]]
        #
        # for j in range(len(current_feature_values)/len(db_names[db_column[i]])):
        #     fid.write("%s" % " & ".join(current_feature_values[j*3:(j+1)*3]))
        fid.write("\\\\ \n")
    fid.close()

if __name__ == '__main__':
    main()
