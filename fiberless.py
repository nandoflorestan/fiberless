#!/usr/bin/env python3

"""**Fiberless** monitors your network connection and logs downtime
    to a CSV file.
    """

import atexit
from datetime import datetime
from subprocess import call
from time import sleep

PING_HOSTS = [
    'vivatudo.com.br',
    'www.microsoft.com',
    'uol.com.br',
]


class Fiberless(object):
    def __init__(self, sleep=30, ping_hosts=PING_HOSTS,
                 log_path='downtime.utf8.csv'):
        self.sleep = sleep
        self.ping_hosts = ping_hosts
        self.log_path = log_path
        self.bad_since = None
        atexit.register(self.close)

    @property
    def network_has_been_up(self):
        return not self.bad_since

    def network_is_ok_now(self):
        """If all ``ping_hosts`` fail, network must be down."""
        for host in self.ping_hosts:
            ret = call(['ping', '-q', '-c', '1', host])
            if ret == 0:
                return True
        return False

    def write_downtime(self, now):
        print('Adding a downtime line to the CSV log file: ', self.log_path)
        with open(self.log_path, mode='a', encoding='utf-8') as fil:
            fil.write(','.join([
                'Downtime',
                str(now - self.bad_since),
                str(self.bad_since),
                str(now),
            ]))

    def monitor_forever(self):
        while True:
            self.monitor()
            sleep(self.sleep)

    def monitor(self):
        now = datetime.now()
        now_ok = self.network_is_ok_now()
        if self.network_has_been_up and not now_ok:
            self.bad_since = now
        elif not self.network_has_been_up and now_ok:
            self.write_downtime(now)
            self.bad_since = None

        if not now_ok:
            print('Connection is bad since {}\n'.format(self.bad_since))

    def close(self):
        """On program termination, write downtime up to now."""
        if not self.network_has_been_up:
            self.write_downtime(datetime.now())


if __name__ == '__main__':
    f = Fiberless(sleep=15)
    f.monitor_forever()
