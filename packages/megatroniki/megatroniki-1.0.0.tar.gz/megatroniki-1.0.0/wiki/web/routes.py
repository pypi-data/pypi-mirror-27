"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import send_file
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor, email
from wiki.web.forms import EditorForm
from wiki.web.forms import SettingsForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
# from wiki.web import base_addr  ##for use in to_pdf etc
from wiki.web.user import protect
from wiki.web.user import User
from wiki.web.user import UserManager


import pypandoc
from os import system

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/<path:url>/topdf/')
@protect  # this just wraps the function to make sure the user is authenticated
def toPdf(url):
    pypandoc.convert('content/' + url + '.md', 'pdf', outputfile='content/pandocTemp/' + url + '.pdf',
                     extra_args=['-V geometry:margin=1.5cm'])
    return send_file('../../content/pandocTemp/' + url + '.pdf', conditional=True)


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        email(url, current_user)
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


@bp.route('/settings/', methods=['GET', 'POST'])
@protect
def settings( ):
    email = current_user.get('email')
    editor = current_user.get('editor')
    settingsUrl = "settings"
    if email == "":
        email = "Enter your email"
    if editor == "":
        editor = "Enter the path to your preferred text editor"
    form = SettingsForm()
    if form.validate_on_submit():
        return render_template('settings.html', form=form, email=email, editor=editor, settingsUrl=settingsUrl )
    return render_template('settings.html', form=form, email=email, editor=editor, settingsUrl=settingsUrl )

@bp.route('/admin/', methods=['GET','POST'])
@protect
def admin( ):
    print current_user.is_admin()
    adminUrl = "admin"
    form = SettingsForm()
    default="username, password"
    if form.validate_on_submit():
        return render_template('admin.html', form=form, default=default, adminUrl=adminUrl )
    return render_template('admin.html', form=form, default=default, adminUrl=adminUrl )

@bp.route('/newUser/<path:url>', methods=['POST'])
@protect
def newUser(url):
    val = request.form['value']
    vals = val.split(",")
    name = vals[0].lstrip().rstrip()
    password = vals[1].lstrip().rstrip()
    new = UserManager('user')
    new.add_user(name, password)
    return redirect(url)

@bp.route('/setEditor/<path:url>/', methods=['POST'])
@protect
def setEditor(url):
    editor = request.form['value']
    current_user.set('editor', editor)
    return redirect(url)


@bp.route('/setEmail/<path:url>/', methods=['POST'])
@protect
def setEmail(url):
    email = request.form['value']
    current_user.set('email', email)
    return redirect(url)


@bp.route('/googleScholar/<path:url>/', methods=['GET'])
@protect
def googleScholar(url):
    title = current_wiki.attr_by_url('title', url)
    title = title.replace(' ', '+')
    googleURL = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C18&q=' + title + '&btnG='
    return redirect(googleURL)


@bp.route("/customEditor/<path:url>", methods=['GET'])
@protect
def customEditor(url):
    source_path = current_wiki.attr_by_url( "path", url )
    editor_path = current_user.get("editor")
    system(editor_path + " " + source_path)
    return redirect(url)


@bp.route("/testRoute/<path:url>")
@protect
def testRoute(url):
    temp = current_user.is_anonymous()
    return redirect(url)


@bp.route("/ebook/", methods=['GET', 'POST'])
@protect
def ebook():
    ebookUrl = "ebook"
    form = SettingsForm()
    if form.validate_on_submit():
        return render_template('ebook.html', form=form, ebookUrl=ebookUrl)
    return render_template('ebook.html', form=form, ebookUrl=ebookUrl)


@bp.route("/ebookGen/<path:url>", methods=['POST'])
@protect
def ebookGen(url):
    ebook_req = request.form['value']
    current_wiki.chapterfy_and_build( current_wiki.assemble_source_list ( current_wiki.parse_request( ebook_req )))
    return redirect(url)


@bp.route('/subscribe/<path:url>')
@protect #this just wraps the function to make sure the user is authenticated
def subscribe(url):
    alreadySub = False
    with open("content/subscriptions.txt", mode='r') as contacts_file:
        for a_contact in contacts_file:
            if(a_contact.split()[1] == str(current_user.get_id())):
                if(a_contact.split()[0] == str(url)):
                    alreadySub = True
    if(not alreadySub):
        f = open('content/subscriptions.txt', 'a+')
        f.write(str(url) + ' ' + str(current_user.get_id()) + '\n')
        f.close()
    return redirect(request.referrer)  ##don't navigate away from the page


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
