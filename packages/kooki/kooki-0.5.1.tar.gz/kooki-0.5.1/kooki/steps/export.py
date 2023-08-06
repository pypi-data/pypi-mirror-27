from kooki.tools import write_file
from kooki.tools.output import Output

def Export(name, content, extension):
    Output.start_step('export')
    file_name = '{0}.{1}'.format(name, extension)
    write_file(file_name, content)
    infos = []
    infos.append({'name': file_name, 'status': '[created]', 'info': ''})
    Output.infos(infos, [('name', 'blue'), ('status', 'green'), ('info', 'cyan')])
