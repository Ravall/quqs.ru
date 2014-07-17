# -*- coding: utf-8 -*-
from django import forms
from models import Autor, Postcard, Order, OrderCards, CARD_PRICE
from django.contrib import admin
from django.db.models import Max
from datetime import datetime


class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'public_name', 'comments')

class PostcardAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostcardAdminForm, self).__init__(*args, **kwargs)
        max_art = Postcard.objects.all().aggregate(Max('art_number'))
        if not max_art['art_number__max']:
            max_art['art_number__max'] = 1000
        self.fields['art_number'].initial = max_art['art_number__max']+1

    class Meta:
        model = Postcard

class PostcardAdmin(admin.ModelAdmin):
    readonly_fields = ('admin_image',)


    form = PostcardAdminForm
    list_display = ('art_number', 'autor', 'admin_image')


class OrderCardsInline(admin.TabularInline):
    model = OrderCards
    readonly_fields = ('admin_image', 'count')
    fields = ('admin_image', 'count')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('email','created', 'updated')
    list_display = ('id', 'status', 'email', 'created', 'updated', 'count', 'summ')

    inlines = [
        OrderCardsInline,
    ]

    def count(self, obj):
        order_cards = OrderCards.objects.filter(order=obj.id)
        count = 0
        for order_card in order_cards:
            count += order_card.count
        return count

    def summ(self, obj):
        return self.count(obj) * CARD_PRICE

    def save_model(self, request, obj, form, change):
        updated = False
        if Order.objects.get(pk=obj.id).status != obj.status:
            updated = True
        super(OrderAdmin, self).save_model(request, obj, form, change)
        if updated:
            obj.updated = datetime.now()
            obj.save()



admin.site.register(Autor, AutorAdmin)
admin.site.register(Postcard, PostcardAdmin)
admin.site.register(Order, OrderAdmin)

