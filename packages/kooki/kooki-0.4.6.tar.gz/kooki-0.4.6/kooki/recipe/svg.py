from kooki.steps import Extension, Metadata, Document, DocumentName

def recipe(document, config):
    extensions = Extension(config, filters=['.svg'])
    metadata = Metadata(config, metadata=document.metadata)
    document_content = Document(config, template=document.template, extensions=extensions, metadata={**extensions, **metadata})
    name = DocumentName(document, metadata)

    Export(name, document_content, 'svg')
