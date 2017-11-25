"""."""
from bottle import route, run, request
from uuid import uuid4


@route('/submit_image', method='POST')
def submit_image():
    """."""
    # TODO: hardcoded path? (yep)
    request.files.get('update').save('./uploads/' + uuid4())
    # call ML process with a path to the files
    return 'OK'


def resolve_config(path):
    """."""
    with open(path) as cf:
        config = {}
        for line in cf:
            keyval = line.strip().split('=')
            if len(keyval) != 2:
                raise Exception("Bad configuration file entry: %s" % line)
            else:
                config[keyval[0]] = keyval[1]
        return config


if __name__ == '__main__':
    config = resolve_config('./config.cfg')
    # TODO: exceptions handiling? (nope, hackathon)
    run(host='0.0.0.0', port=config['bottle_port'])
