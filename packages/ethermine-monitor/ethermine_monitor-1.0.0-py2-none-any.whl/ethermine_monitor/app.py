""" entry point for app """
import os
import requests

from ethermine_monitor.email import send_email


MAX_TIME_DIFF = 30 * 60  # 30 minutes
ID = os.environ.get('WORKER_ID')
SEND_EMAIL = os.environ.get('SEND_EMAIL', True)
URL = 'https://api.ethermine.org/miner/{}/workers'.format(ID)


def worker_monitor():
    """
    Check all workers have positive hashrate and have been seen recently.
    Returns a list of booleans representing if worker is active.
    """
    workers = request_worker_data()
    for worker in workers:
        timeDiff = worker['time'] - worker['lastSeen']
        activeHashing = worker['reportedHashrate'] > 0
        if timeDiff > MAX_TIME_DIFF or not activeHashing:
            name = worker['worker']
            print('Worker {} not active!'.format(name))
            if SEND_EMAIL:
                send_email(name)
            yield False
        else:
            yield True


def request_worker_data():
    """ Make network request for worker data """
    return requests.get(URL).json()['data']
