"""
    Wiki core
    ~~~~~~~~~
"""
from collections import OrderedDict
from io import open
import os
import re

from flask import abort
from flask import url_for
import markdown

import smtplib
from string import Template
from tempfile import mkstemp
from shutil import move
from os import remove

def clean_url(url):
    """
        Cleans the url and corrects various errors. Removes multiple
        spaces and all leading and trailing spaces. Changes spaces
        to underscores and makes all characters lowercase. Also
        takes care of Windows style folders use.

        :param str url: the url to clean


        :returns: the cleaned url
        :rtype: str
    """
    url = re.sub('[ ]{2,}', ' ', url).strip()
    url = url.lower().replace(' ', '_')
    url = url.replace('\\\\', '/').replace('\\', '/')
    return url


def wikilink(text, url_formatter=None):
    """
        Processes Wikilink syntax "[[Link]]" within the html body.
        This is intended to be run after content has been processed
        by markdown and is already HTML.

        :param str text: the html to highlight wiki links in.
        :param function url_formatter: which URL formatter to use,
            will by default use the flask url formatter

        Syntax:
            This accepts Wikilink syntax in the form of [[WikiLink]] or
            [[url/location|LinkName]]. Everything is referenced from the
            base location "/", therefore sub-pages need to use the
            [[page/subpage|Subpage]].

        :returns: the processed html
        :rtype: str
    """
    if url_formatter is None:
        url_formatter = url_for
    link_regex = re.compile(
        r"((?<!\<code\>)\[\[([^<].+?) \s*([|] \s* (.+?) \s*)?]])",
        re.X | re.U
    )
    for i in link_regex.findall(text):
        title = [i[-1] if i[-1] else i[1]][0]
        url = clean_url(i[1])
        html_url = u"<a href='{0}'>{1}</a>".format(
            url_formatter('display', url=url),
            title
        )
        text = re.sub(link_regex, html_url, text, count=1)
    return text

def email(page, current_user):
    #get the contacts to send email to
    names = []
    emails = []
    with open("content/subscriptions.txt", mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            if(a_contact.split()[0] == page):
                names.append(a_contact.split()[1])
                emails.append(current_user.get('email'))

    #get the message ready to send to the contacts
    with open("content/message.txt", 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    message_template = Template(template_file_content)

    try:
        # set up the SMTP server
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login('megatroniki2017@gmail.com', 'megatron1234')

        #send the email
        sender = 'megatroniki2017@gmail.com'
        receivers = emails

        message = message_template.substitute(PAGE=page)


        #smtpObj = smtplib.SMTP('localhost')
        s.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"


class Processor(object):
    """
        The processor handles the processing of file content into
        metadata and markdown and takes care of the rendering.

        It also offers some helper methods that can be used for various
        cases.
    """

    preprocessors = []
    postprocessors = [wikilink]

    def __init__(self, text):
        """
            Initialization of the processor.

            :param str text: the text to process
        """
        self.md = markdown.Markdown([
            'codehilite',
            'fenced_code',
            'meta',
            'tables'
        ])
        self.input = text
        self.markdown = None
        self.meta_raw = None

        self.pre = None
        self.html = None
        self.final = None
        self.meta = None

    def process_pre(self):
        """
            Content preprocessor.
        """
        current = self.input
        for processor in self.preprocessors:
            current = processor(current)
        self.pre = current

    def process_markdown(self):
        """
            Convert to HTML.
        """
        self.html = self.md.convert(self.pre)


    def split_raw(self):
        """
            Split text into raw meta and content.
        """
        self.meta_raw, self.markdown = self.pre.split('\n\n', 1)

    def process_meta(self):
        """
            Get metadata.

            .. warning:: Can only be called after :meth:`html` was
                called.
        """
        # the markdown meta plugin does not retain the order of the
        # entries, so we have to loop over the meta values a second
        # time to put them into a dictionary in the correct order
        self.meta = OrderedDict()
        for line in self.meta_raw.split('\n'):
            key = line.split(':', 1)[0]
            # markdown metadata always returns a list of lines, we will
            # reverse that here
            self.meta[key.lower()] = \
                '\n'.join(self.md.Meta[key.lower()])

    def process_post(self):
        """
            Content postprocessor.
        """
        current = self.html
        for processor in self.postprocessors:
            current = processor(current)
        self.final = current

    def process(self):
        """
            Runs the full suite of processing on the given text, all
            pre and post processing, markdown rendering and meta data
            handling.
        """
        self.process_pre()
        self.process_markdown()
        self.split_raw()
        self.process_meta()
        self.process_post()

        return self.final, self.markdown, self.meta


class Page(object):
    def __init__(self, path, url, new=False):
        self.path = path
        self.url = url
        self._meta = OrderedDict()
        if not new:
            self.load()
            self.render()

    def __repr__(self):
        return u"<Page: {}@{}>".format(self.url, self.path)

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def render(self):
        processor = Processor(self.content)
        self._html, self.body, self._meta = processor.process()

    def save(self, update=True):
        folder = os.path.dirname(self.path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self.path, 'w', encoding='utf-8') as f:
            for key, value in self._meta.items():
                line = u'%s: %s\n' % (key, value)
                f.write(line)
            f.write(u'\n')
            f.write(self.body.replace(u'\r\n', u'\n'))
        if update:
            self.load()
            self.render()


    @property
    def meta(self):
        return self._meta

    def __getitem__(self, name):
        return self._meta[name]

    def __setitem__(self, name, value):
        self._meta[name] = value

    @property
    def html(self):
        return self._html

    def __html__(self):
        return self.html

    @property
    def title(self):
        try:
            return self['title']
        except KeyError:
            return self.url

    @title.setter
    def title(self, value):
        self['title'] = value

    @property
    def tags(self):
        try:
            return self['tags']
        except KeyError:
            return ""

    @tags.setter
    def tags(self, value):
        self['tags'] = value


class Wiki(object):
    def __init__(self, root):
        self.root = root

    def path(self, url):
        if url[-3:] == '.md':
            return os.path.join(self.root, url)
        else:
            return os.path.join(self.root, url + '.md')

    def exists(self, url):
        path = self.path(url)
        return os.path.exists(path)

    def get(self, url):
        path = self.path(url)
        if self.exists(url):
            return Page(path, url)
        return None

    def get_or_404(self, url):
        page = self.get(url)
        if page:
            return page
        abort(404)

    def get_bare(self, url):
        path = self.path(url)
        if self.exists(url):
            return False
        return Page(path, url, new=True)

    def move(self, url, newurl):
        if url[-3:] == '.md':
            source = os.path.join(self.root, url)
        else:
            source = os.path.join(self.root, url) + '.md'
        if newurl[-3:] == '.md':
            target = os.path.join(self.root, newurl)
        else:
            target = os.path.join(self.root, newurl) + '.md'
        # normalize root path (just in case somebody defined it absolute,
        # having some '../' inside) to correctly compare it to the target
        root = os.path.normpath(self.root)
        # get root path longest common prefix with normalized target path
        common = os.path.commonprefix((root, os.path.normpath(target)))
        # common prefix length must be at least as root length is
        # otherwise there are probably some '..' links in target path leading
        # us outside defined root directory
        if len(common) < len(root):
            raise RuntimeError(
                'Possible write attempt outside content directory: '
                '%s' % newurl)
        # create folder if it does not exists yet
        folder = os.path.dirname(target)
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.rename(source, target)

    def delete(self, url):
        path = self.path(url)
        if not self.exists(url):
            return False
        os.remove(path)
        return True

    def index(self):
        """
            Builds up a list of all the available pages.

            :returns: a list of all the wiki pages
            :rtype: list
        """
        # make sure we always have the absolute path for fixing the
        # walk path
        pages = []
        root = os.path.abspath(self.root)
        for cur_dir, _, files in os.walk(root):
            # get the url of the current directory
            cur_dir_url = cur_dir[len(root)+1:]
            for cur_file in files:
                path = os.path.join(cur_dir, cur_file)
                if cur_file.endswith('.md'):
                    url = clean_url(os.path.join(cur_dir_url, cur_file[:-3]))
                    page = Page(path, url)
                    pages.append(page)
        return sorted(pages, key=lambda x: x.title.lower())

    def index_by(self, key):
        """
            Get an index based on the given key.

            Will use the metadata value of the given key to group
            the existing pages.

            :param str key: the attribute to group the index on.

            :returns: Will return a dictionary where each entry holds
                a list of pages that share the given attribute.
            :rtype: dict
        """
        pages = {}
        for page in self.index():
            value = getattr(page, key)
            pre = pages.get(value, [])
            pages[value] = pre.append(page)
        return pages

    def get_by_title(self, title):
        pages = self.index(attr='title')
        return pages.get(title)

    def get_tags(self):
        pages = self.index()
        tags = {}
        for page in pages:
            pagetags = page.tags.split(',')
            for tag in pagetags:
                tag = tag.strip()
                if tag == '':
                    continue
                elif tags.get(tag):
                    tags[tag].append(page)
                else:
                    tags[tag] = [page]
        return tags

    def index_by_tag(self, tag):
        pages = self.index()
        tagged = []
        for page in pages:
            if tag in page.tags:
                tagged.append(page)
        return sorted(tagged, key=lambda x: x.title.lower())

    def search(self, term, ignore_case=True, attrs=['title', 'tags', 'body']):
        pages = self.index()
        regex = re.compile(term, re.IGNORECASE if ignore_case else 0)
        matched = []
        for page in pages:
            for attr in attrs:
                if regex.search(getattr(page, attr)):
                    matched.append(page)
                    break
        return matched


    def source_files_by_search(self, term, ignore_case=True, attr_type=['title']):
        '''
        Returns all the source files by either title, type, or by a search of the body
        Uses the search function, so it admits regex
        Returns a list of paths to md files
        :param term:
        :param ignore_case:
        :param attr_type:
        :return:
        '''
        retList = list()
        if term is None or term == []:
            return "source_files_by_search: Invalid term, None or empty list"
        pages = self.search(term, ignore_case, attr_type)
        for page in pages:
            retList.append(page.path)
        return retList

    def attr_by_url(self, attr, url):
        '''
        Returns given attr from the url of a page
        Valid attrs include: "path" ( to source file ), "title", "tags", "url" etc.
        Will return None if url is invalid

        :param attr:
        :param url:
        :return:
        '''
        pages = self.index()
        for page in pages:
            if url == page.url:
                return eval('page.' + attr)
        return None

    def parse_request(self, req):
        '''
        Parses an ebook request, made in the ebook spec language
        :param req: ebook request
        :return: a map in this specification { N : { attr : term } ... }
        where N is the ordering of this search, attr is the attr that will be searched and term is the term to search for
        '''
        def strip_n_check(brack, token):
            brack_map = {'(': {'left': '{[', 'right': '}]', 'check': ')'},
                         '{': {'left': '([', 'right': ')]', 'check': '}'},
                         '[': {'left': '{(', 'right': '})', 'check': ']'}}
            token = token.rstrip(brack_map[brack]['right']).lstrip(brack_map[brack]['left'])
            if token[-1:] == brack_map[brack]['check'] and token[:1] == brack:
                return True, token.rstrip(')}]').lstrip('({[')
            return False, token
        top_split = req.split('~')
        attrMap = {'body': '{', 'title': '(', 'tags': '['}
        token_counter = 0
        token_map = {}
        for token in top_split:
            type_map = {key: value for (key, value) in
                       [(attr, strip_n_check(brack, token)) for (attr, brack) in attrMap.iteritems()]
                       }
            for type in ('title', 'tags', 'body'):
                if type_map[type][0] == True:
                    token_map[token_counter] = {type: type_map[type][1].split('&')}
                    token_counter += 1
        return token_map

    def assemble_source_list(self, search_dict):
        '''
        Assembles a list of source files for use in building ebook
        :param search_dict: a map in this specification { N : { attr : term } ... }
        where N is the ordering of this search, attr is the attr that will be searched and term is the term to search for
        :return: A list of source files for wiki pages
        '''
        source_list = []
        for x in range(0, len( search_dict.keys() )):
            search_listlet = []
            cur_dict = search_dict[x]
            attr = cur_dict.keys()[0] ##can only ever have one
            terms = cur_dict[attr]
            for term in terms:
                search_listlet.extend( self.search( term, attrs=[ attr ] ) )
            source_list.extend( search_listlet )
        return map( lambda x : x.path, source_list) ##map from pages to their source

    def chapterfy_and_build(self, source_list):
        '''
        modifies source files so that they display properly when built into a pdf
        :param source_list: A list of source files
        :return: A list of source files 
        '''
        def replace(source_file_path, pattern, substring):
            fh, target_file_path = mkstemp()
            with open(target_file_path, 'w') as target_file:
                with open(source_file_path, 'r') as source_file:
                    for line in source_file:
                        target_file.write(line.replace(pattern, substring))
            return target_file_path
        source_list = map( lambda x: replace(x, 'title:', '#'), source_list)
        source_list = map( lambda x: replace(x, 'tags:', '\n* tags:'), source_list)
        os.system( "pandoc -N " + reduce( lambda x, y : x + "gap.md " + y, map( lambda x: x + ' ', source_list) ) + "-o out.pdf")
        map( lambda x : remove(x), source_list)
