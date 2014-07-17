# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404
from models import (
    Postcard, Autor, ShortLinkCardsUrl, SubscibeForm, OrderForm, UserSubscribe, Order, CARD_PRICE
)
from django_ajax.decorators import ajax
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.shortcuts import redirect



def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ int(x) for x in seq if (not (x in seen or seen_add(x))) and x and int(x)]


@ensure_csrf_cookie
def index(request, author_id=0):

    my_cards_count = request.session.get('my_cards_count', 0)
    my_cards_hash = request.session.get('my_cards_hash', 'my')
    my_cards_attrs = request.session.get('my_cards_attrs', [])
    order = request.GET.get('order', False)
    order = '?' if order != 'art' else '-art_number'

    my_cards_count_array = request.session.get('my_cards_count_array', {})

    author = False
    if author_id:
        author = get_object_or_404(Autor, pk=author_id)

    return render(
        request,
        'front/index.html',
        {
            'art_numbers': '0',
            'mode': 'new_cards',
            'order':order,
            'author_id': author_id,
            'author': author,
            'my_cards_count': my_cards_count,
            'my_cards_hash': my_cards_hash,
            'my_cards_attrs':simplejson.dumps(my_cards_attrs),
            'my_cards_attrs_str': str(my_cards_attrs) if len(my_cards_attrs) else '0',
            'my_cards_count_array': simplejson.dumps(my_cards_count_array)
        }
    )

def get_mycards_price(my_cards_attrs, my_cards_count_array):
    count = 0
    for attr in my_cards_attrs.split(','):
        count += my_cards_count_array.get(str(attr), 1)
    return count, count * CARD_PRICE


@ensure_csrf_cookie
def my_cards(request, cards_hash):

    order = request.GET.get('order', False)
    order = '?' if order != 'art' else '-art_number'

    author = False
    author_id = False


    my_cards_hash = cards_hash

    short_url = ShortLinkCardsUrl.objects.get(url_short=cards_hash)



    my_cards_attrs = sorted(f7(short_url.url_part.split(',')))
    attrs_str = ','.join(str(x) for x in my_cards_attrs)
    my_cards_count = len(my_cards_attrs)

    my_cards_count_array = request.session.get('my_cards_count_array', {})

    my_cards_attrs = request.session.get('my_cards_attrs', {})
    count, price = get_mycards_price(my_cards_attrs, my_cards_count_array)


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(email=form.cleaned_data['email'])
            print order
            order.save()
            order.create_order(request)
            to_redirect = redirect('my_cards', cards_hash=cards_hash)
            to_redirect['Location'] += '?ok={0}'.format(order.id)
            return to_redirect
    else:
        form = OrderForm()

    return render(
        request,
        'front/my_cards.html',
        {
            'action':'my_cards',
            'art_numbers': short_url.url_part,
            'mode': 'my_cards',
            'order':order,
            'author_id': author_id,
            'author': author,
            'my_cards_count': my_cards_count,
            'my_cards_hash': my_cards_hash,
            'my_cards_attrs':simplejson.dumps(attrs_str),
            'my_cards_attrs_str': attrs_str if len(my_cards_attrs) else '0',
            'my_cards_count_array': simplejson.dumps(my_cards_count_array),
            'count': count,
            'price': price,
            'form': form,
            'ok_id': request.GET.get('ok'),
        }
    )


@ajax
def get_some_cards(request):

    if not request.method == 'POST':
        pass

    count = int(request.POST.get('count', 4))


    order = request.POST.get('order', False)
    order = '?' if order != '-art_number' else '-art_number'

    author_id = int(request.POST.get('author_id', 0))


    art_numbers = request.POST.get('art_numbers', '').split(',')

    cards = Postcard.objects

    if author_id != False and author_id > 0:
        cards = cards.filter(autor=author_id)

    get_mode = request.POST.get('mode')
    if get_mode == 'new_cards':
        cards = cards.exclude(art_number__in=art_numbers).order_by(order).all()[:count]
    elif get_mode == 'my_cards':
        my_cards = request.POST.get('my_cards')
        cards = cards.filter(
            art_number__in=my_cards.split(',')
        ).exclude(
            art_number__in=art_numbers
        ).order_by(order).all()[:count]


    is_first = False
    art_numbers = []
    cards_json = {
        'params': {
            'count':count,
         },

        'is_last': '0' if len(cards) else '1',
    }
    if cards:
        cards_json['left'] = [];
        cards_json['right'] = [];
        cards_json['status'] = True;
    else:
        cards_json['status'] = False;
    for card in cards:
        is_first = not is_first
        key = 'left' if is_first else 'right'
        art_numbers.append(card.art_number)

        cards_json[key].append({
            'img': unicode(card.pc_image),
            'art': card.art_number,
            'author': card.autor,
            'author_id': card.autor.id,
            'card_id': card.id
        })


    cards_json['art_numbers'] = art_numbers

    return cards_json


@ajax
def my_card_count_change(request):
    my_cards_count_array = request.session.get('my_cards_count_array', {})

    my_cards_attrs = request.session.get('my_cards_attrs', {})
    mode = request.POST.get('mode')
    attr_id = str(request.POST.get('attr_id'))
    count = int(my_cards_count_array.get(attr_id, 1))
    if mode == '+':
        my_cards_count_array[attr_id] = count + 1
    if mode == '-' and count > 1:
        my_cards_count_array[attr_id] = count - 1
    request.session['my_cards_count_array'] = my_cards_count_array

    card_count, price = get_mycards_price(my_cards_attrs, my_cards_count_array)

    return {
        'price': price,
        'card_count': card_count,
        'count': my_cards_count_array
    }



@ajax
def add_card(request):

    action = request.POST.get('action')
    cards = request.POST.get('cards', '0')
    add = request.POST.get('add')


    if action == 'add':
        cards += ',' + add


    attrs = sorted(f7(cards.split(',')))
    print add

    if action == 'del':
        try:
            attrs.remove(int(add))
        except ValueError:
            pass

    attrs_str = ','.join(str(x) for x in attrs)

    hash_str = ShortLinkCardsUrl.save_str(attrs_str)
    my_cards_count = len(attrs)
    request.session['my_cards_count'] = my_cards_count
    request.session['my_cards_hash'] = hash_str
    request.session['my_cards_attrs'] = attrs_str
    return {
        'hash': hash_str,
        'count': my_cards_count,
        'arts': attrs_str
    }

def shops(request):
    my_cards_count = request.session.get('my_cards_count', 0)
    my_cards_hash = request.session.get('my_cards_hash', 'my')
    my_cards_attrs = request.session.get('my_cards_attrs', [])

    return render(
        request,
        "front/shops.html",
        {
            'action': 'shops',
            'my_cards_count': my_cards_count,
            'my_cards_hash': my_cards_hash,
            'my_cards_attrs':simplejson.dumps(my_cards_attrs),
            'my_cards_attrs_str': str(my_cards_attrs) if len(my_cards_attrs) else '0'
        }
    )


def about(request):


    my_cards_count = request.session.get('my_cards_count', 0)
    my_cards_hash = request.session.get('my_cards_hash', 'my')
    my_cards_attrs = request.session.get('my_cards_attrs', [])
    if request.method == 'POST':
        form = SubscibeForm(request.POST)
        if form.is_valid():
            UserSubscribe.objects.get_or_create(email = form.cleaned_data['email'])[0].save()
            to_redirect = redirect('about')
            to_redirect['Location'] += '?ok=1'
            return to_redirect
    else:
        form = SubscibeForm()

    return render(
        request,
        "front/about.html",
        {
            'action': 'about',
            'ok': bool(request.GET.get('ok', 0)),
            'form':form,
            'my_cards_count': my_cards_count,
            'my_cards_hash': my_cards_hash,
            'my_cards_attrs':simplejson.dumps(my_cards_attrs),
            'my_cards_attrs_str': str(my_cards_attrs) if len(my_cards_attrs) else '0'
        }
    )

