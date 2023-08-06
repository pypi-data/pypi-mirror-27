import requests_unixsocket
import json
import os

socket_file = '/opt/data/platform/api.socket'.replace('/', '%2F')
socket = 'http+unix://{0}'.format(socket_file)


def get_app_dir(app):
    if 'SNAP' in os.environ:
        return '/snap/{0}/current'.format(app)
    else:
        return '/opt/app/{0}'.format(app)


def get_data_dir(app):
    if 'SNAP' in os.environ:
        return '/var/snap/{0}/common'.format(app)
    else:
        return '/opt/data/{0}'.format(app)


def _temp():
    session = requests_unixsocket.Session()
    try:
        response = session.get('{0}/app/install_path?name={1}'.format(socket, app))
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if 'success' in response_json and response_json['success']:
                return response_json['data']
            else:
                raise Exception('service error: {0}'.format(response_json['message']))
            
        else:
            raise Exception('unablento connect to {0} with error code: {1}'.format(socket, response.stats_code))
    except Exception, e:
        raise Exception('unable to connect to {0}'.format(socket), e)