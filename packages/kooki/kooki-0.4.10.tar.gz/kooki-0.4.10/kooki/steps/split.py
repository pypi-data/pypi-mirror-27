from kooki.tools.output import Output

def Split(text, separator):
    Output.start_step('split')
    parts = text.split('---\n')
    Output.info('text splitted {} times'.format(len(parts)))
    return parts
