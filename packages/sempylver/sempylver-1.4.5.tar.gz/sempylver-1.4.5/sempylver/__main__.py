import argparse
from sempylver.actions import actions


def main():
    #
    # Define an argument parser for commit-msg.py
    parser = argparse.ArgumentParser(description='Tool for simple semantic versioning.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(
        help="""Possible actions:
- config""",
        dest='action'
    )
    #
    # Config parser
    parser_config = subparsers.add_parser('config', help='Set values in the global config file')
    parser_config.add_argument('--working-directory', metavar='d', type=str, help='specify the root git directory that contains your repos')
    parser_config.add_argument('--author', metavar='a', type=str, help='specify the author to use in setup')
    parser_config.add_argument('--email', metavar='e', type=str, help='specify the email to use in setup')
    parser_config.add_argument('--ssh-key', metavar='s', type=str, help='specify the ssh key file to use when pushing to git')
    #
    # Track parser
    parser_config = subparsers.add_parser('track', help='Track a Python git repository')
    parser_config.add_argument('project_directory', metavar='p', type=str, help='the repository to track')
    parser_config.add_argument('-s', action='store_true', help='create or modify the setup file')
    #
    # Get args
    args_dict = vars(parser.parse_args())
    #
    # Determine action
    action_str = args_dict.pop('action')
    if action_str is not None:
        #
        action = actions[action_str]
        #
        # Perform action
        action(**args_dict)


if __name__ == "__main__":
    main()
