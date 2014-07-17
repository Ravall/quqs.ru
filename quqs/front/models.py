# -*- coding: utf-8 -*-
import uuid
import os
import trans
import re
import hashlib
from django.conf import settings
from django.db import models
from django.utils import timezone
from django import forms
from datetime import datetime


CARD_PRICE = 70

class SubscibeForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'invalid': 'Введите корректный email',
            'required':'Введите email'
        })

class OrderForm(SubscibeForm):
    pass


def translite(string):
    '''
    транслитерация. подходит для seo
    '''
    def eu8(string):
        return string.encode('utf-8')
    if string[-1] == '.':
        string = string[0:-1]
    return re.sub(
        '[^0-9a-z_]', '_',
        eu8(unicode(string.lower()).encode('trans'))
    )


class UserSubscribe(models.Model):
    email = models.EmailField(
        'email', db_index=True, unique=True,
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Autor(models.Model):
    public_name = models.CharField('имя на сайте', max_length=256)
    comments = models.TextField('заметки (для админа)', blank=True)

    def __unicode__(self):
        return "{0}".format(self.public_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


def get_file_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = "postcard-{0}-{1}.{2}" .format(
        translite(instance.autor.public_name),
        instance.art_number,
        ext
    )
    return os.path.join('upload/', filename)


class Postcard(models.Model):
    art_number = models.IntegerField('номер', db_index=True, unique=True)
    autor = models.ForeignKey(Autor, verbose_name='Автор')
    pc_image = models.FileField(
        'сама открытка',
        upload_to=get_file_path
    )


    def admin_image(self):
        if self.pc_image:
            img = '<img src="{0}/{1}"/>'.format(settings.STATIC_URL, self.pc_image)
        else:
            img = 'не загружено изображение'
        return img
    admin_image.short_description = 'Изображение открытки'
    admin_image.allow_tags = True

    class Meta:
        verbose_name = 'Открытка'
        verbose_name_plural = 'Открытки'


class ShortLinkCardsUrl(models.Model):
    url_part = models.TextField()
    url_short = models.CharField(max_length=33, db_index=True, unique=True)
    time_usage = models.DateField(auto_now=True)

    @classmethod
    def save_str(cls, full_str):
        obj, created = cls.objects.get_or_create(url_part=full_str)
        if created:
            short_str = hashlib.md5(full_str).hexdigest()
            obj.url_short = short_str
        else:
            short_str = obj.url_short
        obj.save()
        return short_str


OPEN = 'open'
DONE = 'done'
ORDER_STATUSES = (
    (OPEN, 'открыт'),
    (DONE, 'выполнен'),
)


class Order(models.Model):
    email = models.EmailField(
        'email', db_index=True, unique=False,
    )
    created = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUSES,
        default=OPEN
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def create_order(self, request):
        my_cards_attrs = request.session.get('my_cards_attrs', {})
        my_cards_count_array = request.session.get('my_cards_count_array', {})

        for attr in my_cards_attrs.split(','):
            card = Postcard.objects.get(art_number=attr)
            OrderCards(
                order=self,
                card=card,
                count=my_cards_count_array.get(str(attr), 1)
            ).save()



class OrderCards(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ')
    card = models.ForeignKey(Postcard, verbose_name='открытка')
    count = models.IntegerField('количество')

    def admin_image(self):
        return self.card.admin_image()
    admin_image.short_description = 'Изображение открытки'
    admin_image.allow_tags = True


