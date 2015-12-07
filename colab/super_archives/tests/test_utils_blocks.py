from django.test import TestCase

from ..utils.blocks import EmailBlock


class TestEmailBlock(TestCase):

    def setUp(self):
        self.email_block = EmailBlock()

    def test_html2text_without_br_tag(self):
        html = '<a>Hello, world!</a>'
        text = self.email_block._html2text(html)

        self.assertEquals(text, 'Hello, world!')

    def test_html2text_with_br_tag(self):
        html = '<a>Hello, world</a>!<br><p>Test with br tag</p>!'
        text = self.email_block._html2text(html)

        self.assertEquals(text, 'Hello, world!\nTest with br tag!')

    def test_mark_links(self):
        html = 'http://test.org/'
        text = self.email_block._mark_links(html)

        self.assertEquals(text, '<a target="_blank" href=' +
                                '"http://test.org/">http://test.org/</a>')
