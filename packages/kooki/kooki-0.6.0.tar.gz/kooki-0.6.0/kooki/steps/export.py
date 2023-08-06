from kooki.tools import write_file
import pretty_output

def Export(name, content, extension):
    pretty_output.start_step('export')
    file_name = '{0}.{1}'.format(name, extension)
    write_file(file_name, content)
    infos = []
    infos.append({'name': file_name, 'status': '[created]', 'info': ''})
    pretty_output.infos(infos, [('name', 'blue'), ('status', 'green'), ('info', 'cyan')])
