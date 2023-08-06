import markdown

def MarkdownToHTML(content):

    extensions = [
        'markdown.extensions.meta',
        'markdown.extensions.tables',
        'markdown.extensions.attr_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.def_list',
        'markdown.extensions.sane_lists',
        'markdown.extensions.codehilite']

    md = markdown.Markdown(extensions=extensions)

    html_content = md.convert(content)
    return html_content
