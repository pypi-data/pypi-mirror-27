import pretty_output

def Split(text, separator):
    parts = text.split('---\n')
    pretty_output.info('text splitted {} times'.format(len(parts)))
    return parts
