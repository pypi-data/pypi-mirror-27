import functools
import importlib
import logging
import signal
import time

from platypush.config import Config
from platypush.message import Message

modules = {}

def get_or_load_plugin(plugin_name, reload=False):
    global modules

    if plugin_name in modules and not reload:
        return modules[plugin_name]

    try:
        module = importlib.import_module('platypush.plugins.' + plugin_name)
    except ModuleNotFoundError as e:
        logging.warning('No such plugin: {}'.format(plugin_name))
        raise RuntimeError(e)

    # e.g. plugins.music.mpd main class: MusicMpdPlugin
    cls_name = functools.reduce(
        lambda a,b: a.title() + b.title(),
        (plugin_name.title().split('.'))
    ) + 'Plugin'

    plugin_conf = Config.get_plugins()[plugin_name] \
        if plugin_name in Config.get_plugins() else {}

    try:
        plugin_class = getattr(module, cls_name)
        plugin = plugin_class(**plugin_conf)
        modules[plugin_name] = plugin
    except AttributeError as e:
        logging.warning('No such class in {}: {}'.format(
            plugin_name, cls_name))
        raise RuntimeError(e)

    return plugin


def init_backends(bus=None, **kwargs):
    """ Initialize the backend objects based on the configuration and returns
        a name -> backend_instance map.
    Params:
        bus -- If specific (it usually should), the messages processed by the
            backends will be posted on this bus.

        kwargs -- Any additional key-value parameters required to initialize the backends
        """

    backends = {}

    for k in Config.get_backends().keys():
        module = importlib.import_module('platypush.backend.' + k)
        cfg = Config.get_backends()[k]

        # e.g. backend.pushbullet main class: PushbulletBackend
        cls_name = functools.reduce(
            lambda a,b: a.title() + b.title(),
            (module.__name__.title().split('.')[2:])
        ) + 'Backend'

        try:
            b = getattr(module, cls_name)(bus=bus, **cfg, **kwargs)
            backends[k] = b
        except AttributeError as e:
            logging.warning('No such class in {}: {}'.format(
                module.__name__, cls_name))
            raise RuntimeError(e)

    return backends

def get_module_and_name_from_action(action):
    """ Input  : action=music.mpd.play
        Output : ('music.mpd', 'play') """

    tokens = action.split('.')
    module_name = str.join('.', tokens[:-1])
    method_name = tokens[-1:][0]
    return (module_name, method_name)


def get_message_class_by_type(msgtype):
    """ Gets the class of a message type given as string """

    try:
        module = importlib.import_module('platypush.message.' + msgtype)
    except ModuleNotFoundError as e:
        logging.warning('Unsupported message type {}'.format(msgtype))
        raise RuntimeError(e)

    cls_name = msgtype[0].upper() + msgtype[1:]

    try:
        msgclass = getattr(module, cls_name)
    except AttributeError as e:
        logging.warning('No such class in {}: {}'.format(
            module.__name__, cls_name))
        raise RuntimeError(e)

    return msgclass


def set_timeout(seconds, on_timeout):
    """
    Set a function to be called if timeout expires without being cleared.
    It only works on the main thread.

    Params:
        seconds    -- Timeout in seconds
        on_timeout -- Function invoked on timeout unless clear_timeout is called before
    """

    def _sighandler(signum, frame):
        on_timeout()

    signal.signal(signal.SIGALRM, _sighandler)
    signal.alarm(seconds)


def clear_timeout():
    """ Clear any previously set timeout """
    signal.alarm(0)


# vim:sw=4:ts=4:et:

