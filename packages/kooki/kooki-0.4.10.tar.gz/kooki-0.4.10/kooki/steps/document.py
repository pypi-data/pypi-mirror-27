from kooki import DocumentException
from kooki.tools.output import Output

def Document(config, template, extensions, metadata):

    Output.start_step('document')

    if template in extensions:
        kooki = extensions[template]
        infos = []
        infos.append({'name': template, 'status': '[found]', 'info': ''})
        Output.infos(infos, [('name', 'blue'), ('status', 'green'), ('info', 'cyan')])
    else:
        raise DocumentException('the template provided (\'{}\') was not found'.format(template))

    document = kooki(**metadata)

    return document
