#!/usr/bin/python
#
# Script to send email notifications when a change in Galera cluster membership
# occurs.
#
# Complies with http://www.codership.com/wiki/doku.php?id=notification_command
#
# Author: Gabe Guillen <gguillen@gesa.com>
# Version: 1.3
# Release: 10/03/2013
# Use at your own risk.  No warranties expressed or implied.
#

import os
import sys
import getopt
import smtplib
import ConfigParser
import argparse

try: from email.mime.text import MIMEText
except ImportError:
    # Python 2.4 (CentOS 5.x)
    from email.MIMEText import MIMEText

import socket

configfile = '/etc/galeranotify.conf'

# Edit below at your own risk
################################################################################
# Change this to some value if you don't want your server hostname to show in
# the notification emails
hostname = socket.gethostname()

config = ConfigParser.ConfigParser()
if os.path.exists(configfile):
    config.read(configfile)
else:
    print "Missing %s. Exiting." % (configfile)
    sys.exit(1)

config = config._sections['galeranotify']

def main(argv):
    parser = argparse.ArgumentParser(
        description=(
            'Notify by Email from config file of changes in the Galera Cluster'
        )
    )
    parser.add_argument(
        '--status',
        action='store',
        required=True,
        type=str,
        help='<status str>'
    )
    parser.add_argument(
        '--uuid',
        action='store',
        required=True,
        type=str,
        help='<state UUID>'
    )
    parser.add_argument(
        '--primary',
        action='store',
        required=True,
        type=str,
        help='<yes/no>'
    ),
    parser.add_argument(
        '--members',
        action='store',
        required=True,
        type=str,
        help='<comma-seperated list of the component member UUIDs>'
    )
    parser.add_argument(
        '--index',
        action='store',
        required=True,
        type=str,
        help='<n>'
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args_obj = parser.parse_args()
    args = vars(args_obj)
    # if args['']
    try:
        send_notification(
            config, 
            'Galera Notification: ' + hostname,
            str(GaleraStatus(hostname)),
        )
    except Exception, e:
        print "Unable to send notification: %s" % e
        sys.exit(1)
    sys.exit(0)

def send_notification(config, subject, message):
    msg = MIMEText(message)

    msg['From'] = config['from']
    msg['To'] = ', '.join(config['to'])
    msg['Subject'] =  subject

    if(config['ssl']):
        mailer = smtplib.SMTP_SSL(config['host'], config['port'])
    else:
        mailer = smtplib.SMTP(config['port'], config['port'])

    if(config['auth']):
        mailer.login(config['username'], config['password'])

    mailer.sendmail(config['from'], config['to'], msg.as_string())
    mailer.close()

class GaleraStatus:
    def __init__(self, server):
        self._server = server
        self._status = ""
        self._uuid = ""
        self._primary = ""
        self._members = ""
        self._index = ""
        self._count = 0

    def set_status(self, status):
        self._status = status
        self._count += 1

    def set_uuid(self, uuid):
        self._uuid = uuid
        self._count += 1

    def set_primary(self, primary):
        self._primary = primary.capitalize()
        self._count += 1

    def set_members(self, members):
        self._members = members.split(',')
        self._count += 1

    def set_index(self, index):
        self._index = index
        self._count += 1

    def __str__(self):
        message = "Galera running on " + self._server + " has reported the following"
        message += " cluster membership change"

        if(self._count > 1):
            message += "s"

        message += ":\n\n"

        if(self._status):
            message += "Status of this node: " + self._status + "\n\n"

        if(self._uuid):
            message += "Cluster state UUID: " + self._uuid + "\n\n"

        if(self._primary):
            message += "Current cluster component is primary: " + self._primary + "\n\n"

        if(self._members):
            message += "Current members of the component:\n"

            if(self._index):
                for i in range(len(self._members)):
                    if(i == int(self._index)):
                        message += "-> "
                    else:
                        message += "-- "

                    message += self._members[i] + "\n"
            else:
                message += "\n".join(("  " + str(x)) for x in self._members)

            message += "\n"

        if(self._index):
            message += "Index of this node in the member list: " + self._index + "\n"

        return message

if __name__ == "__main__":
    main(sys.argv[1:])
