from html.parser import HTMLParser

tags_opened = []
formats_opened = []
text_tags = ['p', 'span']
attrs_to_tags = {
    'font-weight': 'b',
    'font-style': 'i',
    'text-decoration': 'u',
}


class HtmlToShortTag(HTMLParser):

    def __init__(self):
        super().__init__()
        self.tagged_message = ''

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.tagged_message += '<{} {}="{}"/>'.format(tag, *attrs[0])
        elif tag in text_tags:
            tags_opened.append(tag)
            for attr in attrs:
                formats_opened.extend(
                    [attrs_to_tags.get(a.split(':')[0]) for a in attr[1].split() if a.split(':')[0] in attrs_to_tags.keys()])
                if formats_opened:
                    for f in formats_opened:
                        self.tagged_message += '<{}>'.format(f)

    def handle_endtag(self, tag):
        if tag in text_tags and formats_opened:
            while formats_opened:
                self.tagged_message += '</{}>'.format(formats_opened.pop())
        elif tag == 'style':
            self.tagged_message = ''
        elif tag == 'html':
            self.reset()

    def handle_data(self, data):
        if tags_opened and data.strip():
            self.tagged_message += data
