import time
import argparse
import os
from esbmc_wr.csvwr import csvwr
from esbmc_wr.log import log
from esbmc_wr.bar import Bar
from esbmc_wr.utils import utils
from esbmc_wr.utils import shell

def arguments():
    parser = argparse.ArgumentParser("Input Options")
    parser.add_argument("-e", "--esbmc-parameter", help="Use ESBMC parameter")
    parser.add_argument("-i", "--libraries", help="Path to the file that describe the libraries dependecies", default=False)
    parser.add_argument("-f", "--functions", help="Enable Functions Verification", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", help="Enable Verbose Output", action="store_true", default=False)
    parser.add_argument("-r", "--recursive", help="Enable Recursive Verification", action="store_true", default=False)
    parser.add_argument("-d", "--directory", help="Set the directory to be verified", default=False)
    parser.add_argument("-fl", "--file", help="File to be verified", default=False)
    parser.add_argument("-rp", "--retest-pointer", help="Retest Invalid Pointer", action="store_true", default=False)
    args = parser.parse_args()

    return(args)

def main():
    utils.is_esbmc_installed()

    args = arguments()

    log.configure(args.verbose)

    print("ESBMC Running...")

    # Format ESBMC arguments
    cmd_line = utils.get_command_line(args)

    # Read Libraries Dependencies File
    if args.libraries:
        log.info("Dependecies File: %s" % args.libraries)
        dep_list = utils.read_dep_file(args.libraries)
    else:
        dep_list = []

    # Get c files on the folder
    if args.file:
        all_c_files = [args.file]
    else:
        all_c_files = utils.list_c_files(args.recursive, args.directory)


    start_all = time.time()

    pbar = Bar(all_c_files, verbose=args.verbose)
    # Run ESBMC on each file found
    for c_file in pbar:
        pbar.set_description("Processing %s" % c_file)
        start = time.time()

        shell.run_esbmc(c_file, cmd_line, dep_list, args)

        elapsed = (time.time() - start)
        log.finish_time(c_file, elapsed)


    elapsed_all = (time.time() - start_all)
    log.overall_time(elapsed_all)

    # Run csvwr to export output to a spreadsheet
    csvwr.export_cex()
    print("Done!")

if __name__ == "__main__":
    main()