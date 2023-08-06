from .messages import *
from .tools import *
from .utils import *
from .main_process import *

from .biofiles import *
from .processes import *

__version__ = '0.0.2'

import argparse
import os
import io
import actg


def vcf_peek_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--vcf", help='Location to tf state file',
                       required=True)
    add_arg.add_argument("-f", "--head", action='store_true', help='First Variants in VCF')
    add_arg.add_argument("-t", "--tail", action='store_true', help='Lasts Variants in VCF')
    add_arg.add_argument("-p", "--pretty", action='store_true', help='Pretty print VCF')
    add_arg.add_argument("-l", "--lines", type=int, default=5, help='Print this N lines')

    return add_arg

def bed_sort_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--bed", help='Location to tf state file', required=True)

    return add_arg


def parse_options():
    parser = argparse.ArgumentParser(description='Any description to be displayed for the program.')
    # Create a subcommand
    subparsers = parser.add_subparsers(help='Add sub commands', dest='command')
    # Define a primary command apply & set child/sub commands for apply
    add_vcf_peek = subparsers.add_parser('vcf_peek', help='Tools to apply to VCF files')
    vcf_peek_sub_commands(add_vcf_peek)
    add_bed_sort = subparsers.add_parser('bed_sort', help='Tool to sort bed file')
    bed_sort_sub_commands(add_bed_sort)

    # add_p = subparsers.add_parser('destroy', help='Destroy the infra from system')
    # sub_commands(add_p)
    # add_p = subparsers.add_parser('plan', help='Verify your changes before apply')
    # sub_commands(add_p)
    args = parser.parse_args()
    return args


def main():

    args = parse_options()

    if args.command == 'vcf_peek':
        vcf_peek(args)
    elif args.command == 'bed_sort':
        bed_sort(args)

if __name__ == "__main__":

    main()
