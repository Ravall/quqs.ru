$('document').ready(function() {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
});

function getDocumentHeight(){
    return (document.body.scrollHeight > document.body.offsetHeight) ? document.body.scrollHeight: document.body.offsetHeight;
}

function check_show(x) {
    return ($(document).height() - $(window).height() <= $(window).scrollTop() + x)
}

function pad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}

function print_card(val) {
    if (my_cards_attrs.indexOf(val['art']) == -1) {
        link_text = TEXT_ADD;
        action = 'add';
    } else {
        link_text = TEXT_DEL;
        action = 'del';
    }

    if (window.mode == 'my_cards') {
        count = array_count[val['art']];
        if (typeof count == 'undefined') {
            count = 1;
        }
        card_count = '<a href="#"  art_id='+  val['art'] + ' class="card_count_change">-</a> ' +
            '<span class="attr' + val['art'] + '">' + count + '</span> ' +
            '<a art_id='+  val['art'] + ' class="card_count_change" href="#">+</a>&nbsp;|&nbsp;';
    } else {
        card_count = '';
    }

    return "<div class='card'>" +
        "<img src='" + STATIC_URL + val['img'] + "'>" +
        "<div class='card_link'> " +  card_count +
            "<a class='change_list' action = '" + action + "' " +
            " href='#' art_id=" + val['art'] + ">" + link_text + "</a> | " +
            "<a href='" + url_author_b + val['author_id'] + "'>" + val['author'] + "</a>&nbsp;" +
            pad(val['art'], 4) +
        "</div>"
    "</div>";
}
function loader()
{
    if (! ready_query)
    {
        return;
    }
    ready_query = false;
    $('div#img_loader').html("<img src='"+ STATIC_URL + 'img/loader.gif' + "'>");
    ajaxPost(
        url_somecards,
        {
            'count': count,
            'art_numbers': art_numbers,
            'order': order,
            'author_id':author,
            'mode': get_mode,
            'my_cards': my_cards,

        },
        function(content)
        {
            if (!content['status'])
            {
                $(this).unbind("scroll");
                $('div#img_loader').html("");
                return
            }
            body_height = $( 'body' ).height();
            jQuery.each(content['left'], function(k, val) {
                $('#cards-left').append(print_card(val));
            });
            jQuery.each(content['right'], function(k, val) {
                $('#cards-right').append(print_card(val));
            });
            art_numbers += ','+content['art_numbers'];
            ready_query = true;
            $('a.card_count_change').click(function() {
                now = new Date().getTime()
                if (now - window.time_click < 100) {
                    return false
                }
                window.time_click = now ;

                attr_id = $(this).attr('art_id')
                ajaxPost(
                    url_card_count_change,
                    {
                        'mode': $(this).html(),
                        'attr_id': attr_id,
                        'count': $('span.attr'+attr_id).html(),
                    },
                    function(content) {
                        array_count = content['count']
                        count = array_count[attr_id];
                        $('span.attr'+attr_id).html(count);
                        $('span#card_price').html(content['price']);

                    }
                );
                return false;

            })

            $('a.change_list').click(function() {
                now = new Date().getTime()
                if (now - window.time_click < 100) {
                    return false
                }
                window.time_click = now ;


                my_action = $(this).attr('action');
                ajaxPost(
                    url_add_card,
                    {
                        'cards': my_cards,
                        'add': $(this).attr('art_id'),
                        'action': my_action,
                    },
                    function(content) {
                        var my_url = url_my_cards_b + content['hash'];
                        $('a#my_cards').attr('href', my_url);
                        $('span#count_my_cards').html('('+content['count']+')');
                        my_cards = content['arts'];

                        if (mode == 'my_cards') {
                            $(location).attr('href', my_url);
                        }

                    }
                );
                if (my_action == 'add') {
                    my_action = 'del'
                    link_text = TEXT_DEL;
                } else {
                    my_action = 'add'
                    link_text = TEXT_ADD;
                }

                $(this).attr('action', my_action)
                $(this).html(link_text);

                return false;
            });

            if (check_show(0)) {
               loader();
            } else {
                $('div#img_loader').html("");
            }
        }
    );

}
loader();
function scroll_check() {
   if (check_show(57)) {
        loader();
    }
}

$(window).scroll(scroll_check);