
# Jenkins Job Manager 'deploy' command

import sys


def parse(parser, parents):
    deploy = parser.add_parser('deploy', parents=parents)
    deploy.add_argument('module_path',
                        help='colon-separated list of paths to Python'
                             ' modules.',
                        nargs='?', default=sys.stdin)
    deploy.add_argument('--delete-old', help='delete obsolete jobs.',
                        action='store_true', dest='delete_old', default=False)
