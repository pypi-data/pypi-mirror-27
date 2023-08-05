from xmlrpc.client import ServerProxy

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop

from openslides.core.config import config

from .models import Keypad


VOTECOLLECTOR_ERROR_MESSAGES = {
    -1: ugettext_noop('Unknown voting mode.'),
    -2: ugettext_noop('Invalid keypad range.'),
    -3: ugettext_noop('Invalid keypad list.'),
    -4: ugettext_noop('No keypads authorized for voting.'),
    -5: ugettext_noop('License not sufficient.'),
    -6: ugettext_noop('No voting device connected.'),
    -7: ugettext_noop('Failed to set up voting device.'),
    -8: ugettext_noop('Voting device not ready.'),
}

# For cert authentification see:
# http://mail.python.org/pipermail/python-list/2010-January/1231391.html


class VoteCollectorError(Exception):
    """
    Error class for the VoteCollector Plugin
    """
    def __init__(self, value=None, nr=None):
        if nr is not None:
            self.value = _(VOTECOLLECTOR_ERROR_MESSAGES[nr])
        elif value is not None:
            self.value = value
        else:
            self.value = ''

    def __str__(self):
        return repr("VoteCollector Exception: %s" % self.value)


def get_server():
    """
    Gets a server proxy object.
    """
    try:
        server = ServerProxy(config['votecollector_uri'])
    except TypeError:
        raise VoteCollectorError(_('Server not found.'))
    return server


def get_keypads():
    keypads = Keypad.objects.exclude(user__is_present=False).values_list(
        'keypad_id', flat=True).order_by('keypad_id')

    if config['votecollector_method'] == 'anonym':
        keypads = keypads.filter(user=None)
    elif config['votecollector_method'] == 'person':
        keypads = keypads.exclude(user=None)

    if not keypads.exists():
        raise VoteCollectorError(_('No keypads selected.'))

    return keypads


def get_device_status():
    server = get_server()
    try:
        status = server.voteCollector.getDeviceStatus()
    except:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    return status


def start_voting(mode, options, callback_url):
    server = get_server()
    keypads = get_keypads()

    ext_mode = options + ';' + callback_url if options else callback_url
    try:
        count = server.voteCollector.prepareVoting(mode + '-' + ext_mode, 0, 0, list(keypads))
    except Exception as e:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    if count < 0:
        raise VoteCollectorError(nr=count)

    try:
        count = server.voteCollector.startVoting()
    except:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    if count < 0:
        raise VoteCollectorError(nr=count)

    return count


def stop_voting():
    server = get_server()
    try:
        result = server.voteCollector.stopVoting()
    except:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    return result


def get_voting_status():
    """
    Returns voting status as a list: [elapsed_seconds, votes_received]
    """
    server = get_server()
    try:
        status = server.voteCollector.getVotingStatus()
    except:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    return status


def get_voting_result():
    """
    Returns the voting result as a list.
    """
    server = get_server()
    try:
        result = server.voteCollector.getVotingResult()
    except:
        raise VoteCollectorError(_('No connection to VoteCollector.'))
    return result
