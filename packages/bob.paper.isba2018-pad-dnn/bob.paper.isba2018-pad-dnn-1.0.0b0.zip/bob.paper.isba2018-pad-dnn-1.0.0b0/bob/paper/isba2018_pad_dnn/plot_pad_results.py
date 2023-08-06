#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu  7 Sep 15:19:22 CEST 2017


from __future__ import print_function

"""This script evaluates the given score files and computes EER and Spoofing FAR with regards to 10 types of voice attacks"""

import bob.measure
from ..utils import scores

import argparse
import numpy, math
import os
import os.path
import sys

import matplotlib.pyplot as mpl
import matplotlib.font_manager as fm

import bob.core

logger = bob.core.log.setup("bob.spoof.speech")


def plot_det_curves(scores_dev, scores_eval, outname):
    from matplotlib.backends.backend_pdf import PdfPages
    pdf_name = outname + '_det_curves.pdf'
    pp = PdfPages(pdf_name)

    fig = mpl.figure()
    ax1 = mpl.subplot(111)

    bob.measure.plot.det(scores_dev[0], scores_dev[1], 100,
                         color='blue', linestyle='-', label='Dev set', linewidth=2)
    bob.measure.plot.det(scores_eval[0], scores_eval[1], 100,
                         color='red', linestyle='--', label='Eval set', linewidth=2)

    bob.measure.plot.det_axis([0.1, 99, 0.1, 99])
    mpl.xlabel('FRR (%)')
    mpl.ylabel('FAR (%)')
    mpl.legend()
    mpl.grid()
    pp.savefig()
    pp.close()


def plot_histograms(settype, scores, threshold, outname, histbins_real=100, histbins_attacks=100, attack_scores=None,
                    impostor_scores=None, attacktype="all", realtype="all"):
    from matplotlib.backends.backend_pdf import PdfPages

    pdf_name = outname + '_distributions_' + settype + '.pdf'
    pp = PdfPages(pdf_name)

    negatives = attack_scores
    positives = scores

    fig = mpl.figure()
    ax1 = mpl.subplot(111)

    # mpl.hist(negatives, bins=histbins, color='red', alpha=0.5, label="Spoofed %s @ %s" % (attacktype, settype), normed=True)
    # mpl.hist(positives, bins=histbins, color='blue', alpha=0.5, label="Valid Users @ %s" % (settype),
    #   normed=True)

    mpl.rcParams.update({'font.size': 18})
    if attack_scores is not None:
        mpl.hist(attack_scores, bins=histbins_attacks, color='black', alpha=0.4, label="Spoofing Attacks", normed=True)
    # mpl.hist(impostor_scores, bins=histbins_real, color='red', alpha=0.8, label="Impostors", normed=True)
    mpl.hist(scores, bins=histbins_real, color='blue', alpha=0.6, label="Genuine Accesses", normed=True)

    # plot the line
    mpl.axvline(x=threshold, ymin=0, ymax=1, linewidth=2, color='black', linestyle='--', label="EER threshold")

    mpl.xlabel("Scores")
    mpl.ylabel("Normalized Count")

    # mpl.ylim([0, 0.10])
    # mpl.xlim([-80, 40])
    mpl.legend(loc='upper left', prop=fm.FontProperties(size=16))

    mpl.title("Score distributions and EER, %s set" % (settype))
    mpl.grid()
    pp.savefig()
    pp.close()


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    OUTPUT_DIR = os.path.join(basedir, 'plots')

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--real-dev-file', required=False, default=None,
                        help="The score file of the development set.")
    parser.add_argument('-e', '--real-eval-file', required=False, default=None,
                        help="The score files of the evaluation set.")
    parser.add_argument('-f', '--attacks-eval-file', type=str, required=True,
                        help="The score file with attacks scores.")
    parser.add_argument('-t', '--attacks-dev-file', type=str, required=True, help="The score file with attacks scores.")
    parser.add_argument('-n', '--histogram-bins-real', required=False, type=int, default=20,
                        help="The number of bins in computed histogram of score distribution for real data.")
    parser.add_argument('-m', '--histogram-bins-attacks', required=False, type=int, default=20,
                        help="The number of bins in computed histogram of score distribution for spoof data.")
    parser.add_argument('-o', '--out-directory', dest="directory", default=OUTPUT_DIR,
                        help="This path will be prepended to every file output by this procedure (defaults to '%(default)s')")
    parser.add_argument('-s', '--support', required=False, type=str, nargs='+', default=[], help="Type of attack.")
    parser.add_argument('-k', '--attackdevice', required=False, type=str, default="all", help="Attack device.")
    parser.add_argument('-r', '--device', required=False, type=str, default="all", help="Recording device.")
    parser.add_argument('-b', '--session', required=False, type=str, default="all", help="Recording session.")
    parser.add_argument('-p', '--pretty-title', required=False, type=str,
                        help="Title of the results. Default is the auto-generated file name.")
    parser.add_argument('-c', '--criterion-eval', required=False, type=str, default="hter",
                        help='The criterion for Evaluation scores')

    # add verbose option
    bob.core.log.add_command_line_option(parser)

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    return args


def compute_evals(args, attack, adevice, recdevice, scores_eval_zimp, eer_threshold, flipped_sign):
    if args.real_eval_file is not None:
        print("Loading %s real score file of the evaluation set" % (args.real_eval_file))
        scores_eval_zimp, scores_eval = bob.measure.load.split_four_column(args.real_eval_file)

    # scores_eval_attacks = scores.load_attack_scores(args.attacks_eval_file, support, adevice, recdevice)[1]
    if len(scores_eval_zimp) == 0:
        print("Loading %s score file of the evaluation set with attacks" % (args.attacks_eval_file))
        scores_eval_attacks, scores_eval = scores.load_attack_scores(args.attacks_eval_file, attack, adevice,
                                                                     recdevice)
    else:
        scores_eval_attacks = scores.load_attack_scores(args.attacks_eval_file, attack, adevice, recdevice)[
            0]  # negative

    # far, frr = bob.measure.farfrr(scores_dev_attacks, scores_dev, eer_threshold) # for ASV scores
    # print("Development set attacks: FAR = %2.12f \t FRR = %2.12f HTER = %2.12f \t \t EER threshold = %2.12f" % (far, frr, (far+frr)/2, eer_threshold))
    if len(scores_eval_zimp) == 0:
        scores_eval_neg = scores_eval_attacks
    else:
        scores_eval_neg = scores_eval_zimp

    # find threshold from eval set itself
    if args.criterion_eval == "eer":
        eer_threshold = bob.measure.eer_threshold(scores_eval_neg, scores_eval)

    if flipped_sign:
        sfar, sfrr = bob.measure.farfrr(-1 * scores_eval_neg, -1 * scores_eval, eer_threshold)
    else:
        sfar, sfrr = bob.measure.farfrr(scores_eval_neg, scores_eval, eer_threshold)
    return sfar, sfrr, scores_eval_neg, scores_eval


def main(command_line_parameters=None):
    """Reads score files, computes error measures and plots curves."""

    args = command_line_arguments(command_line_parameters)

    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    histbins_real = int(args.histogram_bins_real)
    histbins_attacks = int(args.histogram_bins_attacks)

    ####################
    ## Read scores ###
    ####################
    scores_dev_zimp = []
    if args.real_dev_file is not None:
        print("Loading %s real score file of the development set" % (args.real_dev_file))
        scores_dev_zimp, scores_dev = bob.measure.load.split_four_column(args.real_dev_file)
    scores_eval_zimp = []

    attacks = 'all'
    if args.support:
        attacks = "-".join(args.support)
    adevice = args.attackdevice
    recdevice = args.device

    attacktype = 'a:' + attacks + ', ad:' + adevice  # + ', rd:' + recdevice
    outname = 'attack_%s_adevice_%s' % (attacks, adevice)

    resfile = open(os.path.join(args.directory, outname + '_results.txt'), "w")
    # print the title of the experiment
    results_title = outname
    if args.pretty_title:
        results_title = args.pretty_title
    print(results_title)
    resfile.write(results_title + "\n")

    print("Loading %s score file of the development set with attacks" % (args.attacks_dev_file))
    # scores_dev_attacks  = scores.load_attack_scores(args.attacks_dev_file, attacks, adevice, recdevice)[1] # only positive values
    # scores_dev_attacks  = scores.load_attack_scores(args.attacks_dev_file)[1] # only positive values
    if len(scores_dev_zimp) == 0:
        scores_dev_attacks, scores_dev = scores.load_attack_scores(args.attacks_dev_file)  # only positive values
    else:
        scores_dev_attacks = scores.load_attack_scores(args.attacks_dev_file)[0]  # only negative values

    print(
        "Size dev-gen: %d, dev-zim: %d, dev-att: %d" % (len(scores_dev), len(scores_dev_zimp), len(scores_dev_attacks)))
    if len(scores_dev_zimp) == 0:
        scores_dev_neg = scores_dev_attacks
    else:
        scores_dev_neg = scores_dev_zimp

    ####################
    ## Compute Stats ###
    ####################

    eer_threshold = bob.measure.eer_threshold(scores_dev_neg, scores_dev)
    far, frr = bob.measure.farfrr(scores_dev_neg, scores_dev, eer_threshold)
    # if the EER is too high (higher than 50%, we try to compute it for the flipped scores)
    # may be the sign of the scores is flipped, so we compute for scores multiplied by -1
    flipped_sign = False
    if (far + frr) / 2 > 0.5:
        eer_threshold_t = bob.measure.eer_threshold(-1 * scores_dev_neg, -1 * scores_dev)
        far_t, frr_t = bob.measure.farfrr(-1 * scores_dev_neg, -1 * scores_dev, eer_threshold)  # for ASV scores
        print("Trying to see if sign flipping helps, EER_flipped=%f" % ((far_t + frr_t) / 2))
        # if the EER for flipped scores is smaller, then keep it
        if (far_t + frr_t) / 2 < (far + frr) / 2:
            eer_threshold = eer_threshold_t
            far = far_t
            frr = frr_t
            flipped_sign = True
            attacktype = 'a:' + attacks + ', ad:FlippedSign'

    print("Development set: FAR = %2.12f \t FRR = %2.12f \t HTER = %2.12f \t EER threshold = %2.12f" % (
        far, frr, (far + frr) / 2, eer_threshold))
    resfile.write(
        "Development set: FAR = %2.12f \t FRR = %2.12f \t EER threshold = %2.12f\n" % (far, frr, eer_threshold))

    sfar = 0
    sfrr = 0
    if args.criterion_eval == "eer" and args.support:
        for attack in args.support:
            cur_sfar, cur_sfrr, scores_eval_neg, scores_eval = compute_evals(args, [attack], adevice, recdevice,
                                                                             scores_eval_zimp, eer_threshold,
                                                                             flipped_sign)
            print("Size eval-gen: %d, eval-negative: %d for attack: %s" %
                  (len(scores_eval), len(scores_eval_neg), attack))
            print("SFAR: %f, SFRR: %f for attack: %s" % (cur_sfar, cur_sfrr, attack))
            sfar += cur_sfar
            sfrr += cur_sfrr
        sfar /= len(args.support)
        sfrr /= len(args.support)
    else:
        sfar, sfrr, scores_eval_neg, scores_eval = compute_evals(args, args.support, adevice, recdevice,
                                                                 scores_eval_zimp, eer_threshold, flipped_sign)
        print("Size eval-gen: %d, eval-negative: %d" % (len(scores_eval), len(scores_eval_neg)))

    print("Evaluation set with attacks: %s, SFAR = %2.12f, SFRR = %2.12f, HTER = %2.12f \t " % (
        attacktype, sfar, sfrr, (sfar + sfrr) / 2))
    resfile.write("Evaluation set with attacks: %s, SFAR = %2.12f, SFRR = %2.12f\n" % (attacktype, sfar, sfrr))

    if flipped_sign:
        cllr = bob.measure.calibration.cllr(-1 * scores_dev_neg, -1 * scores_dev)
        min_cllr = bob.measure.calibration.min_cllr(-1 * scores_dev_neg, -1 * scores_dev)
    else:
        cllr = bob.measure.calibration.cllr(scores_dev_neg, scores_dev)
        min_cllr = bob.measure.calibration.min_cllr(scores_dev_neg, scores_dev)
    print("Development set Calibration: Cllr = %1.5f and minCllr = %1.5f " % (cllr, min_cllr))
    resfile.write("Development set Calibration: Cllr = %1.5f and minCllr = %1.5f \n" % (cllr, min_cllr))

    if flipped_sign:
        cllr = bob.measure.calibration.cllr(-1 * scores_eval_neg, -1 * scores_eval)
        min_cllr = bob.measure.calibration.min_cllr(-1 * scores_eval_neg, -1 * scores_eval)
    else:
        cllr = bob.measure.calibration.cllr(scores_eval_neg, scores_eval)
        min_cllr = bob.measure.calibration.min_cllr(scores_eval_neg, scores_eval)
    print("Evaluation set Calibration: Cllr_eval = %1.5f and minCllr_eval = %1.5f " % (cllr, min_cllr))
    resfile.write("Evaluation set Calibration: Cllr_eval = %1.5f and minCllr_eval = %1.5f\n" % (cllr, min_cllr))
    resfile.close()

    ####################
    ## Plot graphs ###
    ####################

    outname = os.path.join(args.directory, outname)
    plot_histograms("Dev", scores_dev, eer_threshold, outname, histbins_real, histbins_attacks, scores_dev_attacks,
                    scores_dev_zimp, attacktype=attacktype)
    plot_histograms("Eval", scores_eval, eer_threshold, outname, histbins_real, histbins_attacks, scores_eval_neg,
                    scores_eval_zimp, attacktype=attacktype)

    plot_det_curves([scores_dev_attacks, scores_dev], [scores_eval_neg, scores_eval], outname)


if __name__ == '__main__':
    main()
