import logging
import os
import sys
from logging import FileHandler
from optparse import OptionParser

from fish_webapp import settings
from fish_webapp.views.dashboard import dashboard
from fish_webapp.views.scrapyd import scrapyd, fetch_scrapyd_agent
from fish_webapp.views.user import user
from flask import Flask, session, redirect, url_for, request, send_from_directory, render_template
from werkzeug.contrib.cache import SimpleCache


def parse_opts(config):
    parser = OptionParser(usage='usage: %prog [options] args',
                          description='Command line param for FishFishJump webapp.')
    parser.add_option('--host',
                      help='host address, default: %s' % config.get('HOST'),
                      dest='HOST',
                      type='string',
                      default=config.get('HOST'))
    parser.add_option('--port',
                      help='port, default: %s' % config.get('PORT'),
                      dest='PORT',
                      type='int',
                      default=config.get('PORT'))
    parser.add_option('--username',
                      help='administrator username for login, default: %s' % config.get('ADMIN_USERNAME'),
                      type='string',
                      dest='ADMIN_USERNAME',
                      default=config.get('ADMIN_USERNAME'))
    parser.add_option('--password',
                      help='administrator password for login, default: %s' % config.get('ADMIN_PASSWORD'),
                      dest='ADMIN_PASSWORD',
                      default=config.get('ADMIN_PASSWORD'))
    parser.add_option('-d',
                      '--debug',
                      help='enable debug pattern of the flask, default: %s' % config.get('DEBUG'),
                      action='store_true',
                      dest='DEBUG',
                      default=config.get('DEBUG'))
    parser.add_option('-t',
                      '--test',
                      help='enable test pattern of the flask, default: %s' % config.get('TESTING'),
                      action='store_true',
                      dest='TESTING',
                      default=config.get('TESTING'))
    parser.add_option('--uncached',
                      help='disable cache of the flask, default: %s' % config.get('ENABLE_CACHE'),
                      action='store_false',
                      dest='ENABLE_CACHE',
                      default=config.get('ENABLE_CACHE'))
    parser.add_option('--cached-expire',
                      help='expire of the flask cache, default: %s' % config.get('CACHE_EXPIRE'),
                      type='int',
                      dest='CACHE_EXPIRE',
                      default=config.get('CACHE_EXPIRE'))
    parser.add_option('--scrapyd-url',
                      help='url of the scrapyd for connect scrapyd service, default: %s' % config.get('SCRAPYD_URL'),
                      type='string',
                      dest='SCRAPYD_URL',
                      default=config.get('SCRAPYD_URL'))
    parser.add_option('-v',
                      '--verbose',
                      help='verbose that log info, default: %s' % config.get('VERBOSE'),
                      action='store_true',
                      dest='VERBOSE',
                      default=config.get('VERBOSE'))
    return parser.parse_args()


def enable_opts(config):
    opts, args = parse_opts(config)
    config.update(
        DEBUG=opts.DEBUG,
        TESTING=opts.TESTING,
        HOST=opts.HOST,
        PORT=opts.PORT,
        SCRAPYD_URL=opts.SCRAPYD_URL,
        ADMIN_USERNAME=opts.ADMIN_USERNAME,
        ADMIN_PASSWORD=opts.ADMIN_PASSWORD,
        ENABLE_CACHE=opts.ENABLE_CACHE,
        CACHE_EXPIRE=opts.CACHE_EXPIRE,
        VERBOSE=opts.VERBOSE
    )


def setting_logger(app, out_file_name='ffj_web.log'):
    handler = FileHandler(out_file_name)
    root = logging.getLogger()
    if app.config.get('VERBOSE') is True:
        app.logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        root.setLevel(logging.DEBUG)
    root.addHandler(logging.StreamHandler(sys.stdout))
    root.addHandler(handler)
    app.logger.addHandler(handler)


app = Flask(__name__)
app.config.from_object(settings.DevelopmentConfig)
enable_opts(app.config)
setting_logger(app)
app.logger.info('FishFishJump(webapp) started on %s:%s username=%s password=%s'
                % (app.config['HOST'], str(app.config['PORT']), app.config['ADMIN_USERNAME'],
                   app.config['ADMIN_PASSWORD']))

app.secret_key = os.urandom(24)

# init global cache
if app.config['ENABLE_CACHE']:
    app.config['GLOBAL_CACHE'] = SimpleCache()

# register scrapyd agent
fetch_scrapyd_agent(app.config['SCRAPYD_URL'])

# register blueprint
app.register_blueprint(dashboard, url_prefix='/supervisor/dashboard')
app.register_blueprint(user, url_prefix='/supervisor/user')
app.register_blueprint(scrapyd, url_prefix='/supervisor/scrapyd')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500), 500


@app.before_request
def login_interceptor():
    path = request.path
    if path.startswith('/supervisor'):
        if path == '/supervisor/user/login.html' or path == '/supervisor/user/login':
            return
        if not 'is_login' in session or not session['is_login']:
            return redirect(url_for('user.login'))


def main():
    app.run(host=app.config['HOST'], port=int(app.config['PORT']))


if __name__ == '__main__':
    main()
