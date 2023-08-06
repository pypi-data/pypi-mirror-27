from .biofiles.vcf import VCF
from .biofiles.bed import BED

import sys
import os

def vcf_peek(args):

    filepath = os.path.abspath(args.vcf)
    lines = args.lines
    pretty = args.pretty

    vcf = VCF(filepath)

    if all([args.head, args.tail]) is False:
        vcf.head(lines, pretty)
        vcf.tail(lines, pretty)

    if args.head:
        vcf.head(lines, pretty)

    if args.tail:
        vcf.tail(lines, pretty)


def bed_sort(args):
    filepath = os.path.abspath(args.bed)

    bed = BED(filepath)

    bed.sort()


def transpose_lines(args):
    filepath = os.path.abspath(args.input)
    nlines = args.lines
    n = 0

    infhand = open(filepath, 'r')

    from collections import OrderedDict

    values = OrderedDict()
    lines = False

    for line in infhand:
        line = line.strip('\n').split('\t')

        if lines is False:
            for key in line:
                values[key] = []
            lines = True
            continue

        for key, value in zip(values.keys(), line):
            values[key].append(value)

        n += 1

        if n >= nlines:
            break

    c = 0
    for key, value in values.items():
        value = " || ".join(value)
        print(f"{c: <2} <> \033[95m{key}\033[0m <> {value: <8}")
        c += 1
