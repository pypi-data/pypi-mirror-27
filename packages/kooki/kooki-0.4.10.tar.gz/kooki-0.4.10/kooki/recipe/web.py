from kooki.steps import Extension, Metadata, Document, Content, Sass, Font, Css, Js, Template, Export
from kooki.utensils import MarkdownToHTML, HTMLToTeX, Empy, FrontMatter

def recipe(document, config):
    extensions = Extension(config, filters=['.html'])
    metadata = Metadata(config, document.metadata)
    fonts = Font(config)
    js = Js(config)
    css = Css(config)
    sass = Sass(config)

    front_matter = FrontMatter()
    template = Empy({**extensions, **metadata})
    html = MarkdownToHTML()
    utensils = [front_matter, template, html]
    content = Content(config, document.content, utensils)

    document_content = Document(config, document.template, extensions, metadata={
        **extensions,
        **metadata,
        'js': js,
        'css': css,
        'sass': sass,
        'fonts': fonts,
        'content': content})

    name = Template(document.name, metadata)

    Export(name, document_content, 'html')
