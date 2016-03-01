# coding=utf-8
__author__ = 'Warlock'

from flask.ext.assets import Environment, Bundle


def bundle(app):
    assets = Environment(app)

    assets.debug = True

    theme_bundle(assets)
    base_bundle(assets)
    app_bundle(assets)

    return assets


def base_bundle(assets):

    js_vendor = Bundle('components/jquery/dist/jquery.js',
                        'js/vendor/jquery-ui.js',
                       'js/vendor/bootstrap/bootstrap-toggle.min.js',
                       'js/vendor/labjs/LAB.src.js' if assets.debug else 'js/vendor/labjs/LAB.js',
                       'components/knockout/dist/knockout.debug.js',
                       'components/select2/dist/js/select2.full.js',
                       'components/lodash/lodash.js',
                       'components/toastr/toastr.js',
                       'js/knockout.ext.js',
                       filters='jsmin', output='gen/vendor_pack.js')

    assets.register('js_vendor', js_vendor)

    css_vendor = Bundle('css/vendor/jquery/jquery-ui.css',
                        'css/vendor/jquery/jquery-ui.theme.css',
                        'css/vendor/bootstrap/bootstrap-toggle.min.css',
                        'components/toastr/toastr.css',
                        'components/select2/dist/css/select2.css',
                        'components/select2-bootstrap-theme/dist/select2-bootstrap.css',
                        filters='cssmin', output='gen/vendor_pack.css')

    assets.register('css_vendor', css_vendor)


def theme_bundle(assets):
    js_theme = Bundle('js/theme/wordeater/bootstrap.js',
                      'js/theme/wordeater/todo.js',
                      'js/theme/wordeater/app.plugin.js',
                      'theme_components/calendar/calendar.min.js',
                      output='gen/theme_packed.js')

    assets.register('js_theme', js_theme)

    css_theme = Bundle('css/themes/wordeater/bootstrap.css',
                       'css/themes/wordeater/animate.css',
                       'css/themes/wordeater/font-awesome.min.css',
                       'css/themes/wordeater/font.css',
                       'css/themes/wordeater/plugin.css',
                       'css/themes/wordeater/todo.css',
                       'theme_components/calendar/calendar.css',
                       filters='cssmin', output='gen/theme.css')

    assets.register('css_theme', css_theme)


def app_bundle(assets):
    js_app = Bundle('js/utils.js',
                    'js/rest.js',
                    'js/api.js',
                    'js/app.js',
                    filters='jsmin', output='gen/app.js')

    assets.register('js_app', js_app)

