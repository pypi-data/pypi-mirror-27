from kooki.tools.output import Output
from kooki.tools import read_file
from kooki import DocumentException

def Read(files):
    Output.start_step('read')
    result = ''
    infos = []
    error = False
    for source in files:
        try:
            result += read_file(source)
            infos.append({'name': source, 'status': '[found]', 'info': ''})

        except DocumentException as e:
            infos.append({'name': source, 'status': ('[error]', 'red'), 'info': (str(e), 'red')})
            error = True

        except NameError as e:
            infos.append({'name': source, 'status': ('[error]', 'red'), 'info': (str(e), 'red')})
            error = True

        except Exception as e:
            raise Exception(type(e))

    if len(files) > 0:
        Output.infos(infos, [('name', 'cyan'), ('status', 'green'), ('info', 'cyan')])

    if error:
        raise DocumentException('Something went wrong... :(')

    return result
