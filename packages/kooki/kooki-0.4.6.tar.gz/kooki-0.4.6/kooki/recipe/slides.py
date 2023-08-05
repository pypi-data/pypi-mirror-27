from kooki.steps import Extension, Metadata, Document, Sass, Font, Js, Css, Slides, DocumentName, Export

def recipe(document, config):
    extensions = Extension(config, filters=['.html'])
    metadata = Metadata(config, document.metadata)
    fonts = Font(config)
    js = Js(config)
    css = Css(config)
    sass = Sass(config)

    content = Slides(config, document.contents, {**extensions, **metadata})

    document_content = Document(config, document.template, extensions, metadata={
        **extensions,
        **metadata,
        'js': js,
        'css': css,
        'sass': sass,
        'fonts': fonts,
        'content': content})

    name = DocumentName(document, metadata)

    Export(name, document_content, 'html')
