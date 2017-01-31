from json import dumps

from bottle import run, get, post, request

from errors import translate_error
from evaldontevil import execute_python


def explain_error(exc, code):
    msg = exc.get('exception_type', '') + ': ' + exc.get('exception_msg', '')
    line = code.split('\n')[exc['line'] - 1]
    try:
        translation = translate_error(msg, line)
    except:
        translation = ''
    exc['exception_translation'] = translation


@get('/execute')
def execute():
    print(request)
    user_script = request.query.user_script
    print(user_script)
    input_data = request.query.input_data
    print(input_data)
    explain = bool(request.query.explain)
    print(explain)
    res = execute_python(user_script, stdin=input_data, explain=explain).__dict__

    if explain:
        del res['stdout']  # exact the same information is present on the last frame - why should it be duplicated?
        del res['stderr']  # see ^

    if 'trace' in res:
        event = res['trace'][-1]
        if event['event'] == 'exception' or event['event'] == 'uncaught_exception':
            explain_error(event, user_script)

    if 'exception' in res and res['exception'] is not None:
        explain_error(res['exception'], user_script)

    return dumps(res)


run(host='localhost', port=8080)
