import requests_unixsocket
import json

socket_file = '/opt/data/platform/config/uwsgi/socket/api.wsgi.sock'.replace('/', '%2F')
socket = 'http+unix://{0}'.format(socket_file)

def get_install_path(app):
    session = requests_unixsocket.Session()
    try:
        response = session.get('{0}/app/install_path?name='.format(socket, app))
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