import argparse
import re

if __name__ == "__main__":
    #
    # Define an argument parser for commit-msg.py
    parser = argparse.ArgumentParser(description='Check commit message for flags.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('msg-path', metavar='mmm', type=str, help='the path to the commit message')
    #
    # Get args as dict
    args_dict = vars(parser.parse_args())
    msg_path = args_dict['msg-path']
    #
    # Grab message
    with open(msg_path, 'r') as f:
        msg = f.read().strip()
    #
    # Parse the msg for version number
    flag_regex = re.compile(".*(-[mM]).*")
    flag_found = flag_regex.search(msg)
    flag = None
    if flag_found:
        flag = re.sub('-', '', flag_found.group(1))
    try:
        #
        # Parse semantic version
        semver_regex = re.compile("(\d+\.\d+\.\d+)")
        with open("__version__", "r") as ff:
            version = ff.read().strip()
        semver_match = semver_regex.search(version)
        if semver_match:
            semver = [int(j) for j in version.split('.')]
        else:
            semver = [0, 0, 0]
        #
    except Exception:
        semver = [0, 0, 0]
    #
    # Parse the msg for skip command
    skip_flag_regex = re.compile(".*(-[sS]).*")
    skip_flag_found = skip_flag_regex.search(msg)
    if skip_flag_found:
        pass
        #
    else:
        #
        # Condition on flag
        if flag == 'M':
            semver[0] += 1
            semver[1] = 0
            semver[2] = 0
        elif flag == 'm':
            semver[1] += 1
            semver[2] = 0
        else:
            semver[2] += 1
        #
        # Concat
        semver = [str(i) for i in semver]
        version = '.'.join(semver)
        #
        # Write semantic version
        with open("__version__", "w") as f:
            f.write(version)
        #
    #
#
