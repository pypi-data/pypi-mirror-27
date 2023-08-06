import argparse
import re
import sys

from platypush import get_backends, get_default_pusher_backend, parse_config_file

def print_usage():
    print ('''Usage: {} [-h|--help] <-t|--target <target name>> <-a|--action <action name>> payload
    -h, --help:\t\tShow this help and exit
    -b, --backend:\tBackend to deliver the message [pushbullet|kafka] (default: whatever specified in your config with pusher=True)
    -t, --target:\tName of the target device/host
    -a, --action\tAction to run, it includes both the package name and the method (e.g. shell.exec or music.mpd.play)
    payload:\t\tArguments to the action
'''.format(sys.argv[0]))


def pusher(target, action, backend=None, **kwargs):
    config = parse_config_file()

    msg = {
        'target': target,
        'action': action,
        **kwargs,
    }

    if target == 'localhost':
        backend = 'local'
    elif not backend:
        backend = get_default_pusher_backend(config)

    backends = get_backends(config)
    if backend not in backends:
        raise RuntimeError('No such backend configured: {}'.format(backend))

    b = backends[backend]
    b.send_msg(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', '-t', dest='target', required=True,
                        help="Destination of the command")

    parser.add_argument('--action', '-a', dest='action', required=True,
                        help="Action to execute, as package.method")

    parser.add_argument('--backend', '-b', dest='backend', required=False,
                        help="Backend to deliver the message " +
                        "[pushbullet|kafka|local] (default: whatever " +
                        "specified in your config with pusher=True)")

    opts, args = parser.parse_known_args(sys.argv[1:])

    if len(args) % 2 != 0:
        raise RuntimeError('Odd number of key-value options passed: {}'.
                           format(args))

    payload = {}
    for i in range(0, len(args), 2):
        payload[re.sub('^-+', '', args[i])] = args[i+1]

    pusher(target=opts.target, action=opts.action,
           backend=opts.backend if 'backend' in opts else None, **payload)


if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:

