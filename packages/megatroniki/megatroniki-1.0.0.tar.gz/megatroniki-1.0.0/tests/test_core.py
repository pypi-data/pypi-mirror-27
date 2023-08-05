# -*- coding: utf-8 -*-
from io import open
from mock import patch
import os
from unittest import TestCase

from wiki.core import clean_url, email
from wiki.core import wikilink
from wiki.core import Page
from wiki.core import Processor
from wiki.web.user import UserManager

from . import WikiBaseTestCase


PAGE_CONTENT = u"""\
title: Test
tags: one, two, 3, jö

Hello, how are you guys?

**Is it not _magnificent_**?
"""


CONTENT_HTML = u"""\
<p>Hello, how are you guys?</p>
<p><strong>Is it not <em>magnificent</em></strong>?</p>"""


WIKILINK_PAGE_CONTENT = u"""\
title: link

[[target]]
"""

WIKILINK_CONTENT_HTML = u"""\
<p><a href='/target'>target</a></p>"""


def simple_url_formatter(endpoint, url):
    """
        A simple URL formatter to use when no application context
        is available.

        :param str endpoint: the endpoint to use.
        :param str url: the URL to format
    """
    return u"/{}".format(url)


def wikilink_simple_url_formatter(text):
    """
        A wikilink function that uses the simple URL formatter.

        :param str text: the text to format.
    """
    return wikilink(text, simple_url_formatter)


class SimpleWikilinkProcessor(Processor):
    """
        As the processor can currently not take arguments for
        preprocessors we need to temporarily subclass it to
        overwrite it with the simple URL formatter.
    """
    postprocessors = [wikilink_simple_url_formatter]


class URLCleanerTestCase(TestCase):
    """
        Contains various tests for the url cleaner.
    """

    def test_clean_simple_url(self):
        """
            Assert a simple URL remains unchanged.
        """
        simple_url = '/test'

        assert clean_url(simple_url) == simple_url

    def test_clean_deep_url(self):
        """
            Assert a deep URL remains unchanged.
        """
        deep_url = '/test/two/three/yo'

        assert clean_url(deep_url) == deep_url

    def test_handle_spaces(self):
        """
            Assert that unnecessary spaces will be removed and all
            other spaces correctly substituted.
        """
        assert (clean_url('   /hello you/wonderful/person ')
                    == '/hello_you/wonderful/person')

    def test_handle_uppercase(self):
        """
            Assert that uppercase characters will be substituted.
        """
        assert clean_url("HELLo") == "hello"


class WikilinkTestCase(TestCase):
    """
        Contains various tests for the wikilink parser.
    """

    def test_simple_wikilink(self):
        """
            Assert a simple wikilink is converted correctly.
        """
        formatted = wikilink(u'[[target]]', simple_url_formatter)
        assert formatted == "<a href='/target'>target</a>"

    def test_titled_wikilink(self):
        """
            Assert a wikilink with a title will be converted correctly.
        """
        formatted = wikilink(u'[[target|Target]]', simple_url_formatter)
        assert formatted == "<a href='/target'>Target</a>"

    def test_multiple_wikilinks(self):
        """
            Assert a text with multiple wikilinks will be converted
            correctly.
        """
        formatted = wikilink(
            u'[[target|Target]] is better than [[alternative]]',
            simple_url_formatter
        )
        assert formatted == (
            "<a href='/target'>Target</a> is better than"
            " <a href='/alternative'>alternative</a>"
        )


class ProcessorTestCase(WikiBaseTestCase):
    """
        Contains various tests for the :class:`~wiki.core.Processors`
        class.
    """

    page_content = PAGE_CONTENT

    def setUp(self):
        super(ProcessorTestCase, self).setUp()
        self.processor = Processor(self.page_content)

    def test_process(self):
        """
            Assert processing works correctly.
        """
        html, original, meta = self.processor.process()

        assert html == CONTENT_HTML
        assert original == PAGE_CONTENT.split(u'\n\n', 1)[1]
        assert meta == {
            'title': u'Test',
            'tags': u'one, two, 3, jö'
        }

    def test_process_wikilinks(self):
        """
            Assert that wikilinks are processed correctly.
        """
        self.processor = SimpleWikilinkProcessor(WIKILINK_PAGE_CONTENT)
        html, _, _ = self.processor.process()
        assert html == WIKILINK_CONTENT_HTML


class PageTestCase(WikiBaseTestCase):
    """
        Contains various tests for the :class:`~wiki.core.Page`
        class.
    """

    page_content = PAGE_CONTENT

    def setUp(self):
        super(PageTestCase, self).setUp()

        self.page_path = self.create_file('test.md', self.page_content)
        self.page = Page(self.page_path, 'test')

    def test_page_loading(self):
        """
            Assert that content is loaded correctly from disk.
        """
        assert self.page.content == PAGE_CONTENT

    def test_page_meta(self):
        """
            Assert meta data is interpreted correctly.
        """
        assert self.page.title == u'Test'
        assert self.page.tags == u'one, two, 3, jö'

    def test_page_saving(self):
        """
            Assert that saving a page back to disk persists it
            correctly.
        """
        self.page.save()
        with open(self.page_path, 'r', encoding='utf-8') as fhd:
            saved = fhd.read()
        assert saved == self.page_content


class WikiTestCase(WikiBaseTestCase):
    """
        Contains various tests for the :class:`~wiki.core.Wiki`
        class.
    """

    def test_simple_file_detection(self):
        """
            Assert a test markdown file is correctly detected.
        """
        self.create_file('test.md')
        assert self.wiki.exists('test') is True

    def test_wrong_extension_detection(self):
        """
            Assert a non markdown file is ingored.
        """
        self.create_file('test.txt')
        assert self.wiki.exists('test') is False

    def test_config_is_unreadable(self):
        """
            Assert that the content file cannot be loaded as a page.
        """
        # the config file is automatically created, so we can just run
        # tests without having to worry about anything
        assert self.wiki.exists('config') is False
        assert self.wiki.exists('config.py') is False

    def test_delete(self):
        """
            Assert deleting a URL will delete the file.
        """
        self.create_file('test.md')
        self.wiki.delete("test")
        assert not os.path.exists(os.path.join(self.rootdir, 'test.md'))

    def test_index(self):
        """
            Assert index correctly lists all the files.
        """
        self.create_file('test.md', PAGE_CONTENT)
        self.create_file('one/two/three.md', WIKILINK_PAGE_CONTENT)
        with patch('wiki.core.Processor', new=SimpleWikilinkProcessor):
            pages = self.wiki.index()
        assert len(pages) == 2

        # as the index return should be sorted by the title
        # the first page should always be the link one and the other
        # one the second
        deeptestpage = pages[0]
        assert deeptestpage.url == 'one/two/three'

        testpage = pages[1]
        assert testpage.url == 'test'

    def test_move(self):
        """
        Assert that move correctly moves a page
        :return:
        """
        self.create_file('move.md', PAGE_CONTENT)
        self.wiki.move( 'move.md', self.rootdir + '/movetest/move.md')
        self.wiki.move( self.rootdir + '/movetest/move.md', self.rootdir + "/move.md")
        assert os.path.exists( self.rootdir + '/movetest/move.md') is False
        assert os.path.exists( self.rootdir + '/move.md')

    def test_tags(self):
        """
        Test tags
        :return:
        """
        self.create_file( "tags.md", PAGE_CONTENT )
        tags = self.wiki.get_tags()
        test_tags = [ u'one', u'two', u'3', u'jö' ]
        for tag in tags.keys():
            assert tag in test_tags

    def test_index_by_tag(self):
        """
        Test indexing by tags
        :return:
        """
        self.create_file("tag_index.md", PAGE_CONTENT)
        pages = self.wiki.index_by_tag(u'two')
        assert pages[0].path == self.rootdir + "/tag_index.md"

    def test_search(self):
        """
        Test search function
        :return:
        """
        self.create_file("search.md", PAGE_CONTENT)
        pages = self.wiki.search("guys")
        assert pages[0].path == self.rootdir + "/search.md"

    def test_gets(self):
        """
        Test all three get functions
        :return:
        """
        self.create_file("gets.md", PAGE_CONTENT)
        caught = False
        page1 = self.wiki.get(self.rootdir + "/gets.md")
        page2 = self.wiki.get_bare(self.rootdir + "/gets.md")
        page3 = self.wiki.get_or_404(self.rootdir + "/gets.md")
        try:
            page4 = self.wiki.get_or_404(self.rootdir + "/derp.md")
        except( Exception ):
            caught = True
        assert caught == True
        assert page2 == False
        for page in [page1, page3]:
            assert page.path == self.rootdir + "/gets.md"

    def test_index_by(self):
        """
        Test the index_by function
        :return:
        """
        self.create_file("index_by.md", PAGE_CONTENT)
        tags = self.wiki.index_by(u'tags')
        assert tags.keys()[0] == u'one, two, 3, jö'

    def test_request(self):
        '''
        Test the eBook request function
        :return:
        '''

class EmailTestCase(TestCase):
    """
        Tests that email is sent when page is edited
    """

    def test_email_sent(self):
        name = 'user'
        password = '1234'
        active = True
        roles = ['Admin']
        authentication_method = 'hash'
        os.remove("users.json")
        user_manager = UserManager('')
        hash_user = user_manager.add_user(name, password, active, roles, authentication_method)
        hash_user.set('authenticated', True)
        hash_user.set('email', 'cmschwegman@gmail.com')
        url = "test"
        alreadySub = False
        with open("content/subscriptions.txt", mode='r') as contacts_file:
            for a_contact in contacts_file:
                if (a_contact.split()[1] == str(hash_user.get_id())):
                    if (a_contact.split()[0] == str(url)):
                        alreadySub = True
        if (not alreadySub):
            f = open('content/subscriptions.txt', 'a+')
            f.write(u'' + url + ' ' + str(hash_user.get_id()) + '\n')
            f.close()
        is_caught = False
        try:
            email(url, hash_user)
        except:
            is_caught = True
        assert is_caught is False


