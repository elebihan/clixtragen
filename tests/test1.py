import argparse

def parse_cmd_securize(args):
    value = 1
    print(value)

def parse_cmd_customize(args):
    print(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', '-n',
                        action='store_true',
                        help='do not commit changes')
    parser.add_argument('user',
                        help='name of the user')
    subs = parser.add_subparsers(dest='command',
                                 help='command to execute')
    p_a = subs.add_parser('securize',
                          help='securize the device')
    p_a.set_defaults(func=parse_cmd_securize)
    p_a.add_argument('--full', '-f',
                     action='store_true',
                     default=False,
                     help='fully lock the device')
    p_b = subs.add_parser('customize',
                          help='customize the device')
    p_b.set_defaults(func=parse_cmd_customize)
    p_b.add_argument('parameter',
                     choices=('mac', 'serial', 'config'),
                     help='name of the parameter to set')
    p_b.add_argument('value',
                     help='value of the parameter')
    parser.add_argument('address',
                        help='address of the device')
    p_i = subs.add_parser('inspect',
                          help='inspect the device')
    p_i.add_argument('-o', '--output',
                     metavar='FILE',
                     help='set output file')

    args = parser.parse_args()
    args.func(args)
