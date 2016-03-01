/**
 * Created by Warlock on 21.02.2016.
 */

var default_rest_options = {
    is_show_error_message: true,
    cbFinally: undefined
};

function Delete(url, success, fail, options) {

    var data = {
        'justification': ''
    };

    var contentType = '';
    if(options.justification){
        data.justification = options.justification;
        contentType = 'application/json';
    }

    $.ajax({
        url: url,
        type: 'Delete',
        dataType: 'json',
        contentType: contentType,
        data: JSON.stringify(data)
    }).done(function (data) {
        _Success(success, data, options);
    }).fail(function (error) {
        _Fail(fail, error, options);
    });
}

function Get(url, success, fail, options) {

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json'
    }).done(function (data) {
        _Success(success, data, options);

    }).fail(function (error) {
        _Fail(fail, error, options);
    });
}

function Post(url, data, success, fail, options) {

    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data)
    }).done(function (data) {
        _Success(success, data, options);

    }).fail(function (error) {
        _Fail(fail, error, options);
    });
}

function Patch(url, data, success, fail, options) {
    $.ajax({
        url: url,
        type: 'PATCH',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(data)
    }).done(function (data) {
        _Success(success, data, options);
    }).fail(function (error) {
        _Fail(fail, error, options);
    });
}

function _Success(cb, data, options) {
    options = _.defaults({}, default_rest_options, options);

    if (cb) {
        cb(data);
    }

    if (options.cbFinally)
        options.cbFinally();
}

function _Fail(cb, error, options) {
    options = _.defaults({}, default_rest_options, options);

    if (cb) {
        cb(error);
    }
    else {
        if (error.responseJSON && error.responseJSON.message && (typeof error.responseJSON.message) == 'string' && options.is_show_error_message) {
            if (error.responseJSON.status) {
                if (error.responseJSON.status == 401) {
                    toastr.error('Необходима авторизация <a href="/logout/" style="color: yellow">Сменить пользователя<i class="icon sign out"></i> </a>');
                }
                if (error.responseJSON.status == 403) {
                    toastr.error('Не хватает прав для выполнения действия <a href="/logout/" style="color: yellow">Сменить пользователя<i class="icon sign out"></i> </a>');
                }
            }
            else {
                toastr.error(error.responseJSON.message);
            }
        }
        else {
            if (options.is_show_error_message) {
                toastr.error('При обращении к API произошла ошибка');
            }
        }
    }


    if (options.cbFinally)
        options.cbFinally();
}