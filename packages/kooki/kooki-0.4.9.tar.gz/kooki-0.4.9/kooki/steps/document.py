from kooki import DocumentException
from kooki.tools.output import Output

def Document(config, template, extensions, metadata):

    Output.start_step('document')
    Output.info(template)

    if template in extensions:
        kooki = extensions[template]
    else:
        raise DocumentException('bad template')

    document = kooki(**metadata)

    return document
