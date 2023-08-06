import argparse
import re
from sys import stdout

if __name__ == "__main__":
    #
    # Define an argument parser for commit-msg.py
    parser = argparse.ArgumentParser(description='Check commit message for tag flag.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('prev-msg', metavar='ppp', type=str, help='the previous message')
    #
    # Get args as dict
    args_dict = vars(parser.parse_args())
    msg = args_dict['prev-msg']
    #
    # Parse the msg
    flag_regex = re.compile(".*(-[tT]).*")
    flag_found = flag_regex.search(msg)
    if flag_found:
        with open("__version__", "r") as ff:
            post_commit_msg = ff.read().strip()
    else:
        post_commit_msg = "NO"
    #
    # Write output 
    stdout.write(post_commit_msg)
