/**
 * Created by warlock on 30.07.15.
 */

//
// Post model on server (Ajax). Invoke callback function after.
executeOnServer = function (model, url, callback) {

    return $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(model),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            if (callback)
                callback(data);
            else {
                if (data.redirect) {
                    location.href = resolveUrl(data.url);
                }
            }
        },
        error: function (error) {
            alert("There was an error posting the data to the server: " + (error.responseText || error.statusText));
        }
    });

};

//
// Функции по работе с cookie

// возвращает cookie с именем name, если есть, если нет, то undefined
function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options) {
    options = options || {};

    var expires = options.expires;

    if (typeof expires == "number" && expires) {
        var d = new Date();
        d.setTime(d.getTime() + expires * 1000);
        expires = options.expires = d;
    }
    if (expires && expires.toUTCString) {
        options.expires = expires.toUTCString();
    }

    value = encodeURIComponent(value);

    var updatedCookie = name + "=" + value;

    for (var propName in options) {
        updatedCookie += "; " + propName;
        var propValue = options[propName];
        if (propValue !== true) {
            updatedCookie += "=" + propValue;
        }
    }

    document.cookie = updatedCookie;
}

function bakeCookie(name, value) {
    var cookie = [name, '=', JSON.stringify(value), '; domain=.', window.location.host.toString(), '; path=/;'].join('');
    setCookie(name, cookie);
}

function readCookie(name) {
    var cookie = getCookie(name);
    if(!cookie)
        return undefined;

    var result = cookie.match(new RegExp(name + '=([^;]+)'));
    result && (result = JSON.parse(result[1]));
    return result;
}

function deleteCookie(name) {
    document.cookie = [name, '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; path=/; domain=.', window.location.host.toString()].join('');
}


//
// Querystring functions

// Функция разбирает параметры строки и извлекает значние запрошенного параметра
function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
}


// Popovers
function InitPopovers() {
    $('[data-toggle="tooltip"]').popover();
}
