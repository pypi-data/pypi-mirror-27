from kooki.steps import Extension, Metadata, Document, Sass, Font, Js, Css, Template, Export, Split, Read
from kooki.steps.content2 import Content
from kooki.steps.merge import Merge
from kooki.steps.custom import Custom
from kooki.utensils import MarkdownToHTML, Empy

def custom(content, index):
    slide_number = index + 1
    classes = ''
    html_id = ''
    others = ''
    slide_content = content
    result = ''

    if content.startswith('<p>{:'):
        end = content.find('}</p>')
        attrs = content[5:end].split()
        slide_content = content[end + 5:]
        for attr in attrs:
            if attr.startswith('.'):
                classes += attr[1:]
            elif attr.startswith('#'):
                html_id = attr[1:]
            else:
                others += attr

    result = '''
<section id="{0}" class="slide slide-{3} {1}" {2}>
    <div class="slide-number">{3}</div>
    <div class="slide-content">
        <div class="slide-content-child">
        {4}
        </div>
    </div>
</section>
'''.format(html_id, classes, others, slide_number, slide_content)

    return result

def recipe(document, config):
    extensions = Extension(config, filters=['.html'])
    metadata = Metadata(config, document.metadata)
    fonts = Font(config)
    js = Js(config)
    css = Css(config)
    sass = Sass(config)

    text = Read(document.content)
    parts = Split(text, '---\n')

    template = Empy({**extensions, **metadata})
    html = MarkdownToHTML()
    utensils = [template, html]

    result = Content(parts, utensils)
    result = Custom(result, custom)
    result = Merge(result)

    document_content = Document(config, document.template, extensions, metadata={
        **extensions,
        **metadata,
        'js': js,
        'css': css,
        'sass': sass,
        'fonts': fonts,
        'content': result})

    name = Template(document.name, metadata)

    Export(name, document_content, 'html')
