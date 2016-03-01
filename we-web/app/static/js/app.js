/**
 * Created by Warlock on 21.02.2016.
 */

function loader_show() {
    $('body').append('<div class="ui active dimmer"><div class="ui loader"></div></div>');
}

function loader_close() {
    $('.ui.active.dimmer').removeClass('active');
}