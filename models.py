from django.db import models
from django.utils.translation import ugettext_lazy as _


class SMS(models.Model):

    class STATUS:
        not_deliver = 'not_deliver'
        deliver = 'deliver'
        expired = 'expired'
        send = 'send'

        CHOICES = (
            (not_deliver, _('Не доставлено')),
            (deliver, _('Доставлено')),
            (expired, _('Просрочено')),
            (send, _('Отправлено')),
        )

    phone = models.CharField(verbose_name=_('Телефон'), max_length=20)
    sms_id = models.CharField(verbose_name='ID SMS', editable=False, max_length=255)
    status = models.CharField('Статус', max_length=128, choices=STATUS.CHOICES, default=STATUS.send)
    created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True)

    def __str__(self):
        return '{phone} ({status})'.format(
            phone=self.phone,
            status=self.get_status_display()
        )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('SMS сообщение')
        verbose_name_plural = _('SMS сообщения')
