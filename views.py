import re
import logging
from urllib.request import urlopen
from urllib.parse import quote_plus

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.sms.models import SMS

logger = logging.getLogger('sms')


class SmsSender():
    PROTOCOL = 'http'
    HOST = 'gateway.api.sc'

    def send_request(self, params):
        logger.info('SmsSender - send_request', exc_info=True)
        url = '{protocol}://{host}/get/?user={user}&pwd={password}&{params}'.format(
            protocol=self.PROTOCOL,
            host=self.HOST,
            user=settings.SMS_USER,
            password=settings.SMS_PASSWORD,
            params='&'.join('%s=%s' % i for i in params.items()),
        )
        logger.info('SmsSender - url: %s' % url, exc_info=True)
        try:
            response = urlopen(url)
            response_read = response.read()
            logger.info('SmsSender - response_read: %s' % response_read, exc_info=True)
            return response_read
        except:
            logger.error('connection error', exc_info=True)
            return 'connection error'

    def parse_response(self, response):
        logger.info('SmsSender - parse_response', exc_info=True)
        logger.info('SmsSender - isinstance: %s' % isinstance(response, bytes), exc_info=True)
        if isinstance(response, bytes):
            value = response.decode()  # uses 'utf-8' for encoding
        else:
            value = response
        return value  # Instance of str


sender = SmsSender()


def send_sms(phone, text):
    logger.info('SmsSender - send_sms', exc_info=True)

    phone = phone.replace(' ', '')\
        .replace('-', '')\
        .replace('+', '')\
        .replace('(', '')\
        .replace(')', '')
    match = re.search('^\+?\d{11}$', phone)
    if not match:
        Exception(_('Недействительный телефон'))
        return
    logger.info('SmsSender - phone: %s' % phone, exc_info=True)

    params = {
        'dadr': phone,
        'text': quote_plus(text),
        'sadr': quote_plus(settings.SMS_NAME)
    }

    response = sender.send_request(params)
    sms_id = sender.parse_response(response)
    logger.info('SmsSender - sms_id: %s' % sms_id, exc_info=True)

    status = get_sms_status(sms_id)
    logger.info('SmsSender - status: %s' % status, exc_info=True)

    sms = SMS.objects.create(
        phone=phone,
        sms_id=sms_id,
        status=status
    )
    return sms


def get_sms_status(sms_id):
    response = sender.send_request({
        'smsid': sms_id
    })
    status = sender.parse_response(response)
    return status
