from kooki.steps import Content, Extension, Metadata, Document, Template, Export
from kooki.utensils import Empy, FrontMatter

def recipe(document, config):
    extensions = Extension(config, filters=['.md'])
    metadata = Metadata(config, document.metadata)

    front_matter = FrontMatter()
    template = Empy({**extensions, **metadata})
    utensils = [front_matter, template]
    content = Content(config, document.content, utensils)

    document_content = Document(config, document.template, extensions, {**extensions, **metadata, 'content': content})
    name = Template(document.name, metadata)

    Export(name, document_content, 'md')
