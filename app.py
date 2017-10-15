import html, site_config, bottle.ext.sqlite
from bottle import Bottle, run, route, template, request, install
install(bottle.ext.sqlite.Plugin(dbfile=site_config.database_file))
header="<h1><a href='/'>" + html.escape("{{site_name}} - SRD v. 5.1 Tool Kit") + "</a></h1><br /><hr />"
nav_bar="<a href='/'>Home</a> - <a href='/spellbook'>Spellbook</a> - <a href='/charactergenerator'>Character Generator</a> - <a href='/about'>About</a><br />"
base_templ=header+nav_bar
"""
------------------------------------------------------------
Generic Functions
------------------------------------------------------------
These functions are to be called by pages but are not pages
------------------------------------------------------------
"""

"""
------------------------------------------------------------
Homepage
------------------------------------------------------------
------------------------------------------------------------
"""
@route('/')
@route('/index')
def index(site_name=site_config.site_name):
	templ=base_templ
	return template(templ, site_name=site_name)
"""
------------------------------------------------------------
Spellbook
------------------------------------------------------------
------------------------------------------------------------
"""
spell_nav_bar="<a href='/spellbook'>Spellbook Home</a> - <a href='/spellbook/addedit'>Add/Edit Spells</a> - <a href='/spellbook/search'>Search</a><br /><hr />"
spell_search_bar="<form action='/spellbook/search' method='POST'>Search: <input type='text' name='spell_name'> <input type='submit' value='Submit'></form>"
spell_templ=base_templ+spell_nav_bar
@route('/spellbook')
@route('/spellbook/index')
def spellbook(db, site_name=site_config.site_name):
	list_of_all_spells=db.execute('SELECT * from spells').fetchall()
	templ=spell_templ
	for i in list_of_all_spells:
		templ+=i[0]
	return template(templ, site_name=site_name)
@route('/spellbook/<spell_name>')
def get_spell(spell_name, site_name=site_config.site_name):
	templ=spell_templ+"<p>{{spell_name}}</p>"
	return template(templ, spell_name=spell_name, site_name=site_name)
@route('/spellbook/addedit')
def addedit_spell(site_name=site_config.site_name):
	templ=spell_templ
	return template(templ, site_name=site_name)
@route('/spellbook/search')
def spell_search(site_name=site_config.site_name):
	templ=spell_templ+spell_search_bar
	return template(templ, site_name=site_name)
@route('/spellbook/search', method='POST')
def spell_search_result(site_name=site_config.site_name):
	spell_name=request.forms.get('spell_name')
	templ=spell_templ+"<p>{{spell_name}}</p>"
	return template(templ, spell_name=spell_name, site_name=site_name)
"""
------------------------------------------------------------
Character Generator
------------------------------------------------------------
------------------------------------------------------------
"""
@route('/charactergenerator')
@route('/charactergenerator/index')
def charactergen(site_name=site_config.site_name):
	templ=base_templ+"<p>Character Generator</p>"
	return template(templ, site_name=site_name)
"""
------------------------------------------------------------
About
------------------------------------------------------------
------------------------------------------------------------
"""
@route('/about')
def about_page(site_name=site_config.site_name):
	templ=base_templ+"This is a great site"
	return template(templ, site_name=site_name)

"""
RUN
"""
run(host='localhost', port=8080)