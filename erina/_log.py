import logging
from fbchat import log

from _argument_parser import args

def setLogFile(logger, filename):
    """Sets log file to given log

    It also removes log output to stdout cuz erina (usually)
    its executed by cron (linux service) so we dont need
    to print anything to stdout just to log files.

    Args:
        logger (Logger): Instance of Logger
        filename (str): Path to log file
    """
    fileh = logging.FileHandler(filename, 'a+')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    fileh.setFormatter(formatter)

    # if --no-stdout is set we remove all old handlers
    # (cuz there is stdout handler)
    if args.no_stdout:
        for hdlr in log.handlers[:]:
            logger.removeHandler(hdlr)

    logger.addHandler(fileh)
    logger.setLevel(20)

chatlog = logging.getLogger('messenger')

if __name__ == '__main__':
    setLogFile(log, "./_data/logs/fbchat.log")
    setLogFile(chatlog, "./_data/logs/messenger.log")
