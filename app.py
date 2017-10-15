import html, site_config
from bottle import Bottle, run, route, template
header="<h1><a href='/'>" + html.escape("{{site_name}} - SRD v. 5.1 Tool Kit") + "</a></h1><br />"
nav_bar="<a href='/'>Home</a> - <a href='/spellbook'>Spellbook</a> - <a href='/charactergenerator'>Character Generator</a>"
@route('/')
@route('/index')
def index(site_name=site_config.site_name):
	templ=header+nav_bar
	return template(templ, site_name=site_name)
@route('/spellbook')
def spellbook(site_name=site_config.site_name):
	templ=header+nav_bar+"<p>Spellbook</p>"
	return template(templ, site_name=site_name)
@route('/charactergenerator')
def charactergen(site_name=site_config.site_name):
	templ=header+nav_bar+"<p>Character Generator</p>"
	return template(templ, site_name=site_name)
run(host='localhost', port=8080)