#! /usr/bin/env python
"""
Standard sequence quality control tool that can be used for base cropping, 
trimming sequences by quality score, and filtering reads that fail to meet
a minimum length threshold post cropping and trimming.

For single-end and interleaved reads:
    qtrim [options] [-o output] input
 
For split paired-end reads:
    qtrim [option] -o out.forward -v out.reverse -s out.singles in.forward 
        in.reverse

Input files must be in FASTQ format. Output can be in either FASTQ or FASTA 
format. Compression using gzip and bzip2 algorithms is automatically detected 
for input files. To compress output, add the appropriate file extension to the 
file names (.gz, .bz2). For single-end or interleaved reads, use '-' to 
indicate that input should be taken from standard input (stdin). Similarly, 
leaving out the -o argument will cause output to be sent to standard output 
(stdout).
"""

from __future__ import print_function
from __future__ import division

from arandomness.argparse import CheckThreads, Open
import argparse
from multiprocessing import cpu_count, Process, Queue
from multiprocessing.managers import BaseManager
from seq_qc import seq_io, trim
from subprocess import check_output
import sys

__author__ = "Christopher Thornton"
__date__ = "2016-11-06"
__version__ = "1.5.9"


def apply_trimming(record, steps, qual_type, start=0, end=0, trunc=False):
    qual = record.quality
    seq = record.sequence
    slen = len(seq)

    scores = trim.translate_quality(qual, qual_type)
    for step, value in steps:
        newstart, newend = step(scores[start: slen - end], value)
        start += newstart
        end += newend

    last = slen - end
    if trunc:
        try:
            nstart = seq[start: last].index('N')
        except ValueError:
            nstart = last
        seq, qual = seq[start: nstart], qual[start: nstart]
    else:
        seq, qual = seq[start: last], qual[start: last]

    record.sequence, record.quality = seq, qual

    return record

def parse_colons(argument):
    try:
        window, score = argument.split(':')
    except ValueError:
        seq_io.print_error("error: the input provided to sliding-window is "
                           "formatted incorrectly. See --help for usage")
    else:
        if score.isdigit():
            score = int(score)
        else:
            seq_io.print_error("error: the quality score threshold provided "
                               "to sliding-window must be an integer value")
        if window.isdigit():
            window = int(window)
        else:
            try:
                window = float(window)
            except ValueError:
                seq_io.print_error("error: the window-size provided to "
                                   "sliding-window must be either an integer "
                                   "value or a fraction")

    return (window, score)

def parse_commas(args, argname):
    args = [i.lstrip() for i in args.split(",")]

    if 1> len(args) > 2:
        seq_io.print_error("error: only one or two integer values should be "
            "provided to {0}".format(argname))

    try:
        arg1 = int(args[0])
        arg2 = int(args[1])
    except ValueError:
        seq_io.print_error("error: input to {0} must be one or more integer "
                           "values in the form INT or INT,INT".format(argname))
    except IndexError:
        arg1 = arg2 = int(args[0])

    return (arg1, arg2)


def do_nothing(*args):
    pass

def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('fhandle', 
        metavar='in1.fastq',
        type=str,
        action=Open,
        mode='rb',
        default=sys.stdin,
        help="input reads in fastq format. Can be a file containing either "
        "single-end or forward/interleaved reads if reads are paired-end "
        "[required]")
    input_arg = parser.add_mutually_exclusive_group(required=False)
    input_arg.add_argument('--interleaved',
        action='store_true',
        help="input is interleaved paired-end reads")
    input_arg.add_argument('--force',
        action='store_true',
        help="force process as single-end reads even if input is interleaved "
        "paired-end reads")
    input_arg.add_argument('-r', '--reverse',
        dest='rhandle', 
        metavar='in2.fastq', 
        action=Open,
        mode='r',
        help="input reverse reads in fastq format")
    parser.add_argument('-o', '--out', 
        metavar='FILE', 
        dest='out_f',
        type=str,
        action=Open,
        mode='w',
        default=sys.stdout,
        help="output trimmed reads [default: stdout]")
    output_arg = parser.add_mutually_exclusive_group(required=False)
    output_arg.add_argument('-v', '--out-reverse', 
        metavar='FILE', 
        dest='out_r',
        type=str,
        action=Open,
        mode='w',
        help="output trimmed reverse reads")
    output_arg.add_argument('--out-interleaved', 
        dest='out_interleaved',
        action='store_true',
        help="output interleaved paired-end reads, even if input is split")
    parser.add_argument('-s', '--singles', 
        metavar='FILE', 
        dest='out_s',
        type=str,
        action=Open,
        mode='w',
        help="output trimmed orphaned reads")
    parser.add_argument('-l', '--log',
        type=str,
        action=Open,
        mode='w',
        help="output log file to keep track of trimmed sequences")
    parser.add_argument('-q', '--qual-type', 
        metavar='TYPE', 
        dest='qual_type',
        type=int, 
        choices=[33, 64],
        default=33,
        help="ASCII base quality score encoding [default: 33]. Options are "
            "33 (for phred33) or 64 (for phred64)")
    parser.add_argument('-m', '--min-len', 
        metavar='LEN [,LEN]', 
        dest='minlen',
        type=str, 
        help="filter reads shorter than the minimum length threshold [default:"
             " 0]. Different values can be provided for the forward and "
             "reverse reads, respectively, by separating them with a comma "
             "(e.g. 80,60), or a single value can be provided for both")
    trim_args = parser.add_argument_group('trimming options')
    trim_args.add_argument('-O', '--trim-order', 
        metavar='ORDER',
        dest='trim_order',
        type=str,
        default='ltw',
        help="order of trimming steps [default: ltw (corresponds to leading, "
        "trailing, and sliding-window)]")
    trim_args.add_argument('-W', '--sliding-window', 
        metavar='FRAME',
        dest='sw',
        type=parse_colons,
        help="trim both 5' and 3' ends of a read using a sliding window "
        "approach. Input should be of the form 'window_size:qual_threshold', "
        "where 'qual_threshold' is an integer between 0 and 42 and "
        "'window_size' can either be length in bases or fraction of the total "
        "read length")
    trim_args.add_argument('-H', '--headcrop', 
        metavar='INT [,INT]',
        type=str,
        help="remove exactly the number of bases specified from the start of "
        "the reads [default: off]. Different values can be provided for the "
        "forward and reverse reads, respectively, by separating them with a "
        "comma (e.g. 2,0), or a single value can be provided for both")
    trim_args.add_argument('-C', '--crop', 
        metavar='INT [,INT]',
        type=str,
        help="remove exactly the number of bases specified from the end of "
        "the reads [default: off]. Different values can be provided for the "
        "forward and reverse reads, respectively, by separating them with a "
        "comma (e.g. 2,0), or a single value can be provided for both")
    trim_args.add_argument('-L', '--leading', 
        metavar='SCORE', 
        dest='lead_score',
        type=int,
        help="trim by removing low quality bases from the start of the read")
    trim_args.add_argument('-T', '--trailing', 
        metavar='SCORE', 
        dest='trail_score',
        type=int,
        help="trim by removing low quality bases from the end of the read")
    trim_args.add_argument('--trunc-n', 
        dest='trunc_n',
        action='store_true',
        help="truncate sequence at position of first ambiguous base [default: "
             "off]")
    parser.add_argument('--version',
        action='version',
        version='%(prog)s ' + __version__)
    parser.add_argument('-t', '--threads',
        action=CheckThreads,
        type=int,
        default=1,
        help='number of threads to use for trimming [default: 1]')
    args = parser.parse_args()
    all_args = sys.argv[1:]

    seq_io.program_info('qtrim', all_args, __version__)

    # Fail if insufficient directive supplied
    if args.rhandle and not (args.out_r or args.out_interleaved):
        parser.error("one of -v/--out-reverse or --out-interleaved is required "
            "when the argument -r/--reverse is used")

    # Assign variables based on arguments supplied by the user
    fcrop, rcrop = parse_commas(args.crop, "crop") if args.crop else (0, 0)
    fheadcrop, rheadcrop = parse_commas(args.headcrop, "headcrop") if args.headcrop else (0, 0)
    fminlen, rminlen = parse_commas(args.minlen, "minlen") if args.minlen else (0, 0)
    out_f = args.out_f.write
    logger = args.log.write if args.log else do_nothing
    paired = True if (args.interleaved or args.rhandle) else False

    # Prepare the iterator based on dataset type
    print(args.fhandle, args.rhandle)
    iterator = seq_io.read_iterator(args.fhandle, args.rhandle, args.interleaved)

    # Populate list of trimming tasks to perform on reads
    trim_tasks = {'l': (trim.trim_leading, args.lead_score), 
        't': (trim.trim_trailing, args.trail_score), 
        'w': (trim.adaptive_trim, args.sw)}

    trim_steps = []
    for task in args.trim_order:
        value = trim_tasks[task][-1]
        if value:
            trim_steps.append(trim_tasks[task])
    if len(trim_steps) < 1 and not (args.crop or args.headcrop):
        seq_io.print_error("error: no trimming steps were specified")

    # Check dataset type (paired or single-end) 
    if paired:
        print("\nProcessing input as paired-end reads", file=sys.stderr)
        logger("Record\tForward length\tForward trimmed "
            "length\tReverse length\tReverse trimmed length\n")

        out_s = args.out_s.write if args.out_s else do_nothing
        out_r = out_f if ((args.interleaved or args.out_interleaved) and not \
            args.out_r) else args.out_r.write

        # Iterate over paired reads, populating queue for trimming
        pairs_passed = discarded_pairs = fsingles = rsingles = 0
        for i, record in enumerate(iterator):
            forward, reverse = record
            identifier = forward.id
            forig = len(forward.sequence)
            rorig = len(reverse.sequence)

            forward = apply_trimming(forward, trim_steps, args.qual_type, 
                fheadcrop, fcrop, args.trunc_n)
            ftrim = len(forward.sequence)

            reverse = apply_trimming(reverse, trim_steps, args.qual_type, 
                rheadcrop, rcrop, args.trunc_n)
            rtrim = len(reverse.sequence)

            # Both read pairs passed length threshold
            if ftrim >= fminlen and rtrim >= rminlen:
                pairs_passed += 1
                out_f(forward.write())
                out_r(reverse.write())
            # Forward reads orphaned, reverse reads failed length threshold
            elif ftrim >= fminlen and rtrim < rminlen:
                fsingles += 1
                out_s(forward.write())
            # Reverse reads orphaned, forward reads failed length threshold
            elif ftrim < fminlen and rtrim >= rminlen:
                rsingles += 1
                out_s(reverse.write())
            # Both read pairs failed length threshold and were discarded
            else:
                discarded_pairs += 1

            logger("{}\t{}\t{}\t{}\t{}\n".format(identifier, 
                forig, ftrim, rorig, rtrim))

        try:
            i += 1
        except UnboundLocalError:
            seq_io.print_error("error: no sequences were found to process")

        total = i * 2
        passed = pairs_passed * 2 + fsingles + rsingles
        print("\nRecords processed:\t{!s} ({!s} pairs)\nPassed filtering:\t"
            "{!s} ({:.2%})\n  Paired reads kept:\t{!s} ({:.2%})\n  Forward "
            "only kept:\t{!s} ({:.2%})\n  Reverse only kept:\t{!s} ({:.2%})"
            "\nRead pairs discarded:\t{!s} ({:.2%})\n".format(total, i,
            passed, passed / total, pairs_passed, pairs_passed / i,
            fsingles, fsingles / total, rsingles, rsingles / total,
            discarded_pairs, discarded_pairs / i), file=sys.stderr)

    else:
        # Iterate over single-end reads, populating queue for trimming
        print("\nProcessing input as single-end reads", file=sys.stderr)
        logger("Record\tLength\tTrimmed length\n")

        if args.out_s:
            print("\nwarning: argument --singles used with single-end reads"
                "... ignoring\n", file=sys.stderr)

        discarded = 0
        for i, record in enumerate(iterator):
            if i == 0:
                first_read = record.id
            elif i == 1:
                if first_read == record.id and not args.force:
                    seq_io.print_error("warning: the input fastq appears to "
                        "contain interleaved paired-end reads. Please run with "
                        "the --force flag to proceed with processing the data "
                        "as single-end reads")

            origlen = len(record.sequence)
            record = apply_trimming(record, trim_steps, args.qual_type,
                fheadcrop, fcrop, args.trunc_n)
            trimlen = len(record.sequence)
            
            # Record passed length threshold
            if trimlen >= fminlen:
                out_f(record.write())
            # Record failed length threshold and was discarded
            else:
                discarded += 1

            logger("{}\t{}\t{}\n".format(record.id,
                origlen, trimlen))

        try:
            i += 1
        except UnboundLocalError:
            seq_io.print_error("error: no sequences were found to process. "
                               "Please check formatting of the inputs")
 
        passed = i - discarded
        print("\nRecords processed:\t{!s}\nPassed filtering:\t{!s} "
        "({:.2%})\nRecords discarded:\t{!s} ({:.2%})\n".format(i, passed,
        passed / i, discarded, discarded / i), file=sys.stderr)

if __name__ == "__main__":
    main()
    sys.exit(0)
