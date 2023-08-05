from kooki.steps import Content, Extension, Metadata, Document, Xelatex, DocumentName
from kooki.utensils import MarkdownToHTML, HTMLToTeX, Empy, FrontMatter

def recipe(document, config):
    extensions = Extension(config, filters=['.tex'])
    metadata = Metadata(config, document.metadata)

    front_matter = FrontMatter()
    template = Empy({**extensions, **metadata})
    html = MarkdownToHTML()
    tex = HTMLToTeX()
    utensils = [front_matter, template, html, tex]
    content = Content(config, document.contents, utensils)

    document_content = Document(config, document.template, extensions, {**extensions, **metadata, 'content': content})
    name = DocumentName(document, metadata)

    Xelatex(config, name, document_content)
