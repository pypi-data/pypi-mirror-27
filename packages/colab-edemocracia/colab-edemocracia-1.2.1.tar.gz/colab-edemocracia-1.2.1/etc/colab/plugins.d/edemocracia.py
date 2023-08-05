from decouple import config

name = 'colab_edemocracia'
verbose_name = 'Colab eDemocracia Plugin'

urls = {
    'include': 'colab_edemocracia.urls',
    'prefix': '',
    'namespace': 'colab_edemocracia',
    'login': '/home'
}

middlewares = ['colab_edemocracia.middlewares.ForceLangMiddleware']

dependencies = ['djangobower', 'compressor', 'easy_thumbnails',
                'image_cropping', 'widget_tweaks', 'macros', 'rest_framework', 'compressor_toolkit']

context_processors = ['colab_edemocracia.processors.recaptcha_site_key',
                      'colab_edemocracia.processors.home_customization']

settings_variables = {
    'STATICFILES_FINDERS': (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'djangobower.finders.BowerFinder',
        'compressor.finders.CompressorFinder',
    ),
    'BOWER_COMPONENTS_ROOT':
        '/colab-plugins/edemocracia/src/colab_edemocracia/static',
    'BOWER_INSTALLED_APPS': (
        'foundation-sites#6.2.3',
        'jquery-mask-plugin',
        'https://github.com/labhackercd/fontastic-labhacker.git',
    ),
    'COMPRESS_PRECOMPILERS': (
        ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    ),
    'LIBSASS_SOURCEMAPS': 'DEBUG',
    'COMPRESS_ROOT': "/colab-plugins/edemocracia/src/colab_edemocracia/static",
    'COMPRESS_NODE_MODULES': "/colab-plugins/edemocracia/src/colab_edemocracia/node_modules",
    "COMPRESS_NODE_SASS_BIN": "/colab-plugins/edemocracia/src/colab_edemocracia/node_modules/.bin/node-sass",
    "COMPRESS_POSTCSS_BIN": "/colab-plugins/edemocracia/src/colab_edemocracia/node_modules/.bin/postcss",
    'COLAB_TEMPLATES': (
        "/colab-plugins/edemocracia/src/colab_edemocracia/templates",
    ),
    'COLAB_STATICS': [
        '/colab-plugins/edemocracia/src/colab_edemocracia/static',
        '/colab-plugins/edemocracia/src/colab_edemocracia/templates'
        '/components/edem-navigation/static',
    ],
    'RECAPTCHA_SITE_KEY': config('RECAPTCHA_SITE_KEY', default=''),
    'RECAPTCHA_PRIVATE_KEY': config('RECAPTCHA_PRIVATE_KEY', default=''),
    'SITE_NAME': config('SITE_NAME', default='Nome do site'),
    'SITE_LOGO': config('SITE_LOGO', default='https://exemple.com/img.png'),
    'REST_FRAMEWORK': {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'PAGE_SIZE': 20
    }
}
