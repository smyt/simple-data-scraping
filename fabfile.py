"""This module help for deploy project and creating config files."""
import configparser
import os
from pathlib import Path

from fabric.api import env, run, cd, prefix, sudo

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    'host': 'XX.XX.XX.XX',
    'port': 'YY',
    'username': 'smyt',
    'project_name': 'viz_parser',
    'project_dir': PROJECT_DIR,
    'virtualenv_dir': '{}/.virtualenvs/viz_parser/'.format(str(Path.home())),
    'pid': '/tmp/viz_parser.pid',
    'socket': '/tmp/viz_parser.sock'
}

env.hosts = ['{0}@{1}:{2}'.format(
    CONFIG['username'],
    CONFIG['host'],
    CONFIG['port'])
]
env.forward_agent = True


def restart():
    """Restart project's systemd services."""
    run("{}bin/uwsgi --reload {}".format(
        CONFIG['virtualenv_dir'],
        CONFIG['pid']
    ))
    sudo("service v_parser_systemd_rq restart")


def deploy():
    """Deploy project to server."""
    with cd(CONFIG['project_dir']):
        run('git pull origin master')
        with prefix('source {}bin/activate'.format(CONFIG['virtualenv_dir'])):
            run('pip install -r requirements.pip')
        restart()


def generate_config_nginx():
    """Generate config file for nginx."""
    nginx_conf = '''server {
        listen {PORT};

        access_log /var/log/nginx/{PROJECT_NAME}.access.log;
        error_log /var/log/nginx/{PROJECT_NAME}.error.log;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:{SOCKET};
        }
    }'''
    with open('conf/nginx.conf', 'w') as nginx:
        nginx_conf = nginx_conf.replace('{PORT}', '80')
        nginx_conf = nginx_conf.replace('{PROJECT_NAME}', CONFIG['project_name'])
        nginx_conf = nginx_conf.replace('{SOCKET}', CONFIG['socket'])
        nginx.write(nginx_conf)


def generate_config_uwsgi():
    """Generate config file for uwsgi."""
    config = configparser.ConfigParser()
    config['uwsgi'] = {
        'module': 'app:app',
        'chdir': CONFIG['project_dir'],
        'virtualenv': CONFIG['virtualenv_dir'],
        'master': 'true',
        'processes': 2,
        'socket': CONFIG['socket'],
        'pidfile': CONFIG['pid'],
        'chmod-socket': '660',
        'vacuum': 'true',
        'die-on-term': 'true'
    }
    with open('conf/uwsgi.ini', 'w') as uwsgi_config:
        config.write(uwsgi_config)


def generate_config_systemd_uwsgi():
    """Generate config file for uwsgi as systemd service."""
    config = configparser.ConfigParser()
    # disable converts option names to lower case
    config.optionxform = str
    config['Unit'] = {
        'Description': '{} uwsgi daemon'.format(CONFIG['project_name'])
    }
    config['Service'] = {
        'WorkingDirectory': CONFIG['project_dir'],
        'ExecStart': '{}bin/uwsgi {}conf/uwsgi.ini'.format(
            CONFIG['virtualenv_dir'],
            CONFIG['project_dir']
        )
    }
    config['Install'] = {
        'WantedBy': 'multi-user.target'
    }

    with open('conf/systemd.conf', 'w') as file_config:
        config.write(file_config)


def generate_config_systemd_rq():
    """Generate config file for rq as systemd service."""
    config = configparser.ConfigParser()
    # disable converts option names to lower case
    config.optionxform = str
    config['Unit'] = {
        'Description': '{} rq daemon'.format(CONFIG['project_name'])
    }
    config['Service'] = {
        'WorkingDirectory': CONFIG['project_dir'],
        'ExecStart': '{}bin/uwsgi {}bin/rq worker default'.format(
            CONFIG['virtualenv_dir'],
            CONFIG['virtualenv_dir']
        )
    }
    config['Install'] = {
        'WantedBy': 'multi-user.target'
    }

    with open('conf/v_parser_systemd_rq.conf', 'w') as file_config:
        config.write(file_config)


def generate_configs():
    """Create all required configs."""
    if not os.path.exists('conf/'):
        os.makedirs('conf')
    generate_config_nginx()
    generate_config_uwsgi()
    generate_config_systemd_uwsgi()
    generate_config_systemd_rq()
