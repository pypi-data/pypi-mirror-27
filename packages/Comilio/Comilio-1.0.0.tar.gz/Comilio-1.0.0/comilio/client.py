import re
import requests
from . import exceptions


__all__ = [
    'Client',
    'API_URL',

    'CLASSIC',
    'SMART',
    'SMARTPRO',
]


_NUMBER_FORMAT_REGEX = re.compile(r'^\+?[0-9]{4,14}$')

API_URL = 'https://api.comilio.it/rest/v1'

CLASSIC = 'Classic'
SMART = 'Smart'
SMARTPRO = 'SmartPro'


class Client(object):

    def __init__(self, username, password):

        self._auth = (username, password, )

        self.default_type = CLASSIC
        self.default_sender = None
        self.default_recipients = None
        self.raise_insufficient_credit = False

    def set_default_type(self, type):
        if self._check_type(type):
            self.default_type = type

    def set_default_sender(self, sender):
        if self._check_sender(sender):
            self.default_sender = sender
        else:
            raise exceptions.ComilioException('Sender "%s" is not valid' % sender)

    def set_default_recipients(self, recipients, ignore_invalid=False):
        recipients, invalid = self._check_recipients(recipients, ignore_invalid)
        self.default_recipients = recipients
        return invalid

    def send(self, message, recipients=None, type=None, sender=None):
        if not message:
            raise exceptions.ComilioException('SMS message text cannot be empty')

        if recipients:
            recipients = self._check_recipients(recipients)[0]
        else:
            if not self.default_recipients:
                raise exceptions.ComilioException('No recipient provided')
            recipients = self.default_recipients


        if type and self._check_type(type):
            sms_type = type
        else:
            sms_type = self.default_type

        payload = {
           'message_type':  sms_type,
           'phone_numbers': recipients,
           'text':          message,
        }

        if sender:
            if self._check_sender(sender):
                payload['sender_string'] = sender
            else:
                raise exceptions.ComilioException('Sender "%s" is not valid' % sender)
        elif self.default_sender:
            payload['sender_string'] = self.default_sender

        req = self.post('/message', payload)

        if req.status_code != 200:
            exc = exceptions.ComilioException('Unable to send SMS')
            exc.payload = req.text
            raise exc

        data = req.json()
        return data

    def status(self, message_id):
        req = self.get('/message/%s' % message_id)

        if req.status_code != 200:
            exc = exceptions.ComilioException('Unable to get SMS status')
            exc.payload = req.text
            raise exc

        data = req.json()
        return data

    @staticmethod
    def is_valid_number(number):
        if _NUMBER_FORMAT_REGEX.match(number):
            return True
        return False

    def _check_sender(self, sender):
        try:
            sender.encode('ascii')
            if self.is_valid_number(sender) or len(sender) <= 11:
                return True
            return False
        except UnicodeEncodeError:
            return False

    def _check_type(self, sms_type):
        if sms_type in [CLASSIC, SMART, SMARTPRO]:
            self.default_type = sms_type
        else:
            raise exceptions.ComilioException('Invalid message type')

    def _check_recipients(self, recipients, ignore_invalid=False):
        if not isinstance(recipients, list):
            recipients = [recipients]

        invalid = []

        for recipient in recipients:
            if not self.is_valid_number(recipient):
                invalid.append(recipient)
                recipients.remove(recipient)

        if invalid:
            if not ignore_invalid:
                exc = exceptions.ComilioException('Some (%d) recipients were invalid' % len(invalid))
                exc.payload = invalid
                raise exc

        return recipients, invalid

    def get(self, url):
        return self._send_request(url, None, 'get')

    def post(self, url, data):
        return self._send_request(url, data, 'post')

    def _send_request(self, url, data, method):
        headers = {
            'Content-Type': 'application/json',
        }

        method = getattr(requests, method)
        target_url = API_URL + url

        req = method(target_url, json=data, auth=self._auth, headers=headers)

        if req.status_code == 401:
            raise exceptions.InvalidCredentials

        if self.raise_insufficient_credit:
            try:
                data = req.json()
                if data['error'] == 'Insufficient+credit':
                    raise exceptions.InsufficientCredit
            except:
                pass

        return req
