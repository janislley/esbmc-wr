from src.utils import utils

def run(cmd):
    invalid_pointer = 0
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    while True:
        out = proc.stdout.readline()

        if out == ''and proc.poll() is not None:
            break
        if out:
            log.info(out.strip())
            if POINTER_FAIL in out.strip():
                invalid_pointer = 1

    return invalid_pointer

def run_esbmc(c_file, cmd_line, dep_list, args):
    esbmc_args = []

    if not args.functions:
        func_list = ["main"]
    else:
        func_list = utils.list_functions(c_file)

    esbmc_args = shlex.split(cmd_line);

    pbar = Bar(func_list, leave=False, verbose=args.verbose)
    for item in pbar:
        pbar.set_description("Processing %s" % item)
        log.header(c_file, esbmc_args, item)

        cmd = ([ESBMC, c_file] +
                ([] if not args.functions else [FUNCTION, item]) +
                dep_list +
                esbmc_args)

        fail = run(cmd)

        if args.retest_pointer:
            if fail:
                cmd.append(NO_POINTER)
                log.header_retest(c_file, esbmc_args, item)
                run(cmd)

        log.info("")
