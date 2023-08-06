""" Main runnable script for the package. """
import argparse
import logging
import shlex
import time


def main(cmdline=None):
    """ main entry point of script. """

    parser = argparse.ArgumentParser(
        description='Package Examples / Demonstrator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--simulate', action='store_true',
                        help='Enable simulation mode')
    parser.add_argument('-c', '--config', type=str,
                        help='The configuration file to load.')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='Increase output verbosity')

    if cmdline:
        cmdline = shlex.split(cmdline)

    opts = parser.parse_args(cmdline)
    log_format = '%(asctime)s %(levelname)-7s %(name)-30s %(thread)-8d %(message)s'
    log_level = [logging.ERROR, logging.INFO, logging.DEBUG][min(opts.verbosity, 2)]
    logging.basicConfig(level=log_level, format=log_format)

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print('Caught Ctrl+C. Exiting...')


if __name__ == '__main__':
    _CMDLINE = None
    main(_CMDLINE)
