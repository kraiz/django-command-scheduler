from collections import defaultdict

from django.core.management import get_commands


def build_command_choices():
    command_by_app = defaultdict(list)
    for k, v in get_commands().iteritems():
        command_by_app[v.rpartition('.')[-1]].append(k)
    return tuple(sorted([
        (app, tuple(sorted(((cmd, cmd) for cmd in commands))))
        for app, commands in command_by_app.iteritems()
    ]))