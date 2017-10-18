import html, site_config, bottle.ext.sqlite
from bottle import Bottle, run, route, template, request, install
from string import ascii_uppercase
install(bottle.ext.sqlite.Plugin(dbfile=site_config.database_file))
header="<h1><a href='/'>" + html.escape("{{site_name}} - SRD v. 5.1 Tool Kit") + "</a></h1><br /><hr />"
nav_bar="<a href='/'>Home</a> - <a href='/spellbook'>Spellbook</a> - <a href='/charactergenerator'>Character Generator</a> - <a href='/about'>About</a> - <a href='/admin'>Admin</a><br />"
source_books="Player's Handbook","Elemental Evil Companion","Unearthed Arcana"
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
spell_search_bar="""
<form action='/spellbook/search' method='POST'>
	<label>Search:</label>
	<br />
	<label for="spell_name">Name:</label>
	<input type='text' name="spell_name">
	<label for="spell_level">Level:</label>
	<select name="spell_level">
		<option value="\0">0</option>
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
		<option value="6">6</option>
		<option value="7">7</option>
		<option value="8">8</option>
		<option value="9">9</option>
	</select>
	<label for="spell_school">School: </label>
	<select name="spell_school" id="school">
		<option value="">-</option>
		<option value="Abjuration">Abjuration</option>
		<option value="Conjuration">Conjuration</option>
		<option value="Divination">Divination</option>
		<option value="Enchantment">Enchantment</option>
		<option value="Evocation">Evocation</option>
		<option value="Illusion">Illusion</option>
		<option value="Necromancy">Necromancy</option>
		<option value="Transmutation">Transmutation</option>
	</select>
	<label for="spell_casting_time">Casting Time:</label>
	<select name="spell_casting_time">
		<option value="">-</option>
	    <option value="1 action">1 Action</option>
	    <option value="1 bonus action">1 Bonus Action</option>
	    <option value="1 reaction">1 Reaction</option>
	    <option value="1 minute">1 Minute</option>
	    <option value="10 minutes">10 Minutes</option>
	    <option value="1 hour">1 Hour</option>
	    <option value="8 hours">8 Hours</option>
	    <option value="24 hours">24 Hours</option>
	</select>
	<label for="spell_range">Range:</label>
	<select name="spell_range">
		<option value="">-</option>
		<option value="Self">Self</option>
		<option value="Touch">Touch</option>
		<option value="Sight">Sight</option>
		<option value="5 feet">5 feet</option>
		<option value="10 feet">10 feet</option>
		<option value="30 feet">30 feet</option>
		<option value="60 feet">60 feet</option>
		<option value="90 feet">90 feet</option>
		<option value="100 feet">100 feet</option>
		<option value="120 feet">120 feet</option>
		<option value="150 feet">150 feet</option>
		<option value="300 feet">300 feet</option>
		<option value="500 feet">500 feet</option>
		<option value="1 mile">1 mile</option>
		<option value="500 miles">500 miles</option>
		<option value="Unlimited">Unlimited</option>
		<option value="Special">Special</option>
	</select>
	<br />
	<input type='submit' value='Submit'>
	</form>
"""
spell_templ=base_templ+spell_nav_bar
spell_schools="Abjuration","Conjuration","Divination","Enchantment","Evocation","Illusion","Necromancy","Transmutation"
spell_casting_times="1 action","1 bonus action","1 reaction","1 minute","10 minutes","1 hour","8 hours","24 hours"
spell_ranges="Self","Touch","Sight","5 feet","10 feet","30 feet","60 feet","90 feet","100 feet","120 feet","150 feet","300 feet","500 feet","1 mile","500 miles","Unlimited","Special"
spell_durations="Instantaneous","1 round","1 minute","10 minutes","1 hour","8 hours","24 hours","Concentration, up to 6 rounds","Concentration, up to 1 minute","Concentration, up to 10 minutes","Concentration, up to 1 hour","Concentration, up to 2 hours","Concentration, up to 8 hours","Concentration, up to 24 hours","7 days","10 days","30 days","Until dispelled","Until dispelled or triggered","Special"
# Homepage
# Displays a list of all spells in the database
@route('/spellbook')
@route('/spellbook/index')
def spellbook(db, site_name=site_config.site_name):
	templ=spell_templ
	"""
	----------------------------------------
	Generate Spell List
	----------------------------------------
	The spellbook homepage displays an 
	alphabetical list of all spells in the
	database, to make it quick to find a 
	spell by name when needed.

	This method tries to hit the database as
	little as possible.
	----------------------------------------
	"""
	all_spells=db.execute('SELECT * FROM spells ORDER BY name')
	row=all_spells.fetchone()
	alpha_index=0
	while row:
		letter=ascii_uppercase[alpha_index]
		templ+="<p>"+letter+"<br />"
		if row[0][0].upper() == letter:
			templ+=row[0]+"<br />"
			row=all_spells.fetchone()
		else:
			alpha_index+=1
			templ+="</p>"
	while alpha_index < 26:
		letter=ascii_uppercase[alpha_index]
		templ+="<p>"+letter+"<br /></p>"
		alpha_index+=1
	return template(templ, site_name=site_name)

# Spell Display Page
# Displays the details of a single spell
@route('/spellbook/<spell_name>')
def get_spell(db, spell_name, site_name=site_config.site_name):
	templ=spell_templ
	result=db.execute('''SELECT * FROM spells WHERE UPPER(name)=?''', (spell_name.upper(),))
	spell=result.fetchone()
	spell_name=spell[0]
	spell_level=spell[1]
	spell_school=spell[2]
	spell_is_ritual=spell[3]
	spell_casting_time=spell[4]
	spell_range=spell[5]
	spell_component_is_verbal=spell[6]
	spell_component_is_somatic=spell[7]
	spell_component_is_material=spell[8]
	spell_material_components=spell[9]
	spell_mats_are_consumed=spell[10]
	spell_duration=spell[11]
	spell_description=spell[12]
	spell_source_book=spell[13]
	templ+="Name: "+spell_name+"<br />"
	templ+="Level: "+str(spell_level)+"<br />"
	templ+="School: "+spell_school+"<br />"
	if spell_is_ritual == 1:
		templ+="<i>(Ritual)</i>"
	templ+="Casting Time: "+spell_casting_time+"<br />"
	templ+="Range: "+spell_range+"<br />"
	if spell_component_is_verbal == 1:
		templ+="V"
	if spell_component_is_somatic == 1:
		templ+="S"
	if spell_component_is_material == 1:
		templ+="M"
	templ+="<br />"
	templ+="Mats: "+spell_material_components+"<br />"
	if spell_mats_are_consumed == 1:
		templ+="Mats are consumed<br />"
	templ+="Duration: "+spell_duration+"<br />"
	templ+="Description: "+spell_description+"<br />"
	templ+="Source Book: "+spell_source_book+"<br />"
	return template(templ, spell_name=spell_name, site_name=site_name)

# Spell Edit Page
# For adding new spells or editing existing ones
@route('/spellbook/addedit')
def addedit_spell(site_name=site_config.site_name):
	spell_edit_form='<form action="" method="POST"><label for="spell_name">Name:</label><input name="spell_name" type="text"><br /><label for="spell_level">Level:</label><select name="spell_level">'
	for level in range(10):
		spell_edit_form+='<option value="\\'+str(level)+'>'+str(level)+'</option>'
	spell_edit_form+='</select><label for="spell_school">School:</label><select name="spell_school">'
	for school in spell_schools:
		spell_edit_form+='<option value="'+school+'">'+school+'</option>'
	spell_edit_form+='</select><label for="spell_is_ritual">Is the Spell a Ritual?</label><input type="checkbox" name="spell_is_ritual"><br /><label for="spell_casting_time">Casting Time:</label><select name="spell_casting_time">'
	for time in spell_casting_times:
		spell_edit_form+='<option value="'+time+'">'+time+'</option>'
	spell_edit_form+='</select><br /><label for="spell_range">Range:</label><select name="spell_range">'
	for rng in spell_ranges:
		spell_edit_form+='<option value="'+rng+'">'+rng+'</option>'
	spell_edit_form+='</select><br /><label>Components:</label><br /><label for="spell_component_is_verbal">Verbal:</label><input type="checkbox" name="spell_component_is_verbal"><br /><label for="spell_component_is_somatic">Somatic:</label><input type="checkbox" name="spell_component_is_somatic"><br /><label for="spell_component_is_material">Material:</label><input type="checkbox" name="spell_component_is_material"><br /><label for="spell_material_components">Material Components:</label><input type="text" name="spell_material_components" value="None"><br /><label for="spell_mats_are_consumed">Are the Materials Consumed?</label><input type="checkbox" name="spell_mats_are_consumed"><br /><label for="spell_duration">Duration:</label><select name="spell_duration">'
	for duration in spell_durations:
		spell_edit_form+='<option value="'+duration+'">'+duration+'</option>'
	spell_edit_form+='</select><br /><label for="spell_description">Description:</label><br /><textarea rows="10" cols="80" name="spell_description"></textarea><br /><label for="spell_source_book">Source Book:</label><select name="spell_source_book">'
	for book in source_books:
		spell_edit_form+='<option value="'+book+'>'+book+'</option>'
	spell_edit_form+='</select><br /><input type="submit" name="Submit"></form>'
	templ=spell_templ+spell_edit_form
	return template(templ, site_name=site_name)
@route('/spellbook/addedit/<spell_name>')
def addedit_spell_db(db, spell_name, site_name=site_config.site_name):
	templ=spell_templ
	result=db.execute('''SELECT * FROM spells WHERE UPPER(name)=?''', (spell_name.upper(),))
	spell=result.fetchone()
	if spell:
		spell_name=spell[0]
		spell_level=spell[1]
		spell_school=spell[2]
		spell_is_ritual=spell[3]
		spell_casting_time=spell[4]
		spell_range=spell[5]
		spell_component_is_verbal=spell[6]
		spell_component_is_somatic=spell[7]
		spell_component_is_material=spell[8]
		spell_material_components=spell[9]
		spell_mats_are_consumed=spell[10]
		spell_duration=spell[11]
		spell_description=spell[12]
		spell_source_book=spell[13]
		spell_edit_form='<form action="" method="POST"><label for="spell_name">Name:</label>'
		spell_edit_form+='<input name="spell_name" type="text" value="'+spell_name+'"><br />'
		spell_edit_form+='<label for="spell_level">Level:</label><select name="spell_level">'
		for i in range(10):
			spell_edit_form+='<option value="\\'+str(i)+'"'
			if spell_level == i:
				spell_edit_form+=' selected'
			spell_edit_form+='>'+str(i)+'</option>'
		spell_edit_form+='<label for="spell_school">School:</label><select name="spell_school">'
		for school in spell_schools:
			spell_edit_form+='<option value="'+school+'"'
			if spell_school == school:
				spell_edit_form+=' selected'
			spell_edit_form+='>'+school+'</option>'
		spell_edit_form+='</select><label for="spell_is_ritual">Is the Spell a Ritual?</label><input type="checkbox" name="spell_is_ritual"'
		if spell_is_ritual == 1:
			spell_edit_form+=' checked'
		spell_edit_form+='><br /><label for="spell_casting_time">Casting Time:</label><select name="spell_casting_time">'
		for time in spell_casting_times:
			spell_edit_form+='<option value="'+time+'"'
			if spell_casting_time == time:
				spell_edit_form+=' selected'
			spell_edit_form+='>'+time+'</option>'
		spell_edit_form+='</select><br /><label for="spell_range">Range:</label><select name="spell_range">'
		for rng in spell_ranges:
			spell_edit_form+='<option value="'+rng
			if spell_range == rng:
				spell_edit_form+=' selected'
			spell_edit_form+='">'+rng+'</option>'
		spell_edit_form+='</select><br /><label>Components:</label><br /><label for="spell_component_is_verbal">Verbal:</label><input type="checkbox" name="spell_component_is_verbal"'
		if spell_component_is_verbal == 1:
			spell_edit_form+=' checked'
		spell_edit_form+='><br /><label for="spell_component_is_somatic">Somatic:</label><input type="checkbox" name="spell_component_is_somatic"'
		if spell_component_is_somatic == 1:
			spell_edit_form+=' checked'
		spell_edit_form+='><br /><label for="spell_component_is_material">Material:</label><input type="checkbox" name="spell_component_is_material"'
		if spell_component_is_material == 1:
			spell_edit_form+=' checked'
		spell_edit_form+='><br /><label for="spell_material_components">Material Components:</label>'
		if spell_material_components != "None":
			spell_edit_form+='<input type="text" name="spell_material_components" value="'+spell_material_components+'">'
		else:
			spell_edit_form+='<input type="text" name="spell_material_components" value="None">'
		spell_edit_form+='<br /><label for="spell_mats_are_consumed">Are the Materials Consumed?</label><input type="checkbox" name="spell_mats_are_consumed"'
		if spell_mats_are_consumed == 1:
			spell_edit_form+=' checked'
		spell_edit_form+='><br /><label for="spell_duration">Duration:</label><select name="spell_duration">'
		for duration in spell_durations:
			spell_edit_form+='<option value="'+duration+'"'
			if spell_duration == duration:
				spell_edit_form+=' selected'
			spell_edit_form+='>'+duration+'</option>'
		spell_edit_form+='</select><br /><label for="spell_description">Description:</label><br /><textarea rows="10" cols="80" name="spell_description">'+spell_description+'</textarea><br /><label for="spell_source_book">Source Book:</label><select name="spell_source_book">'
		for book in source_books:
			spell_edit_form+='<option value="'+book+'"'
			if spell_source_book == book:
				spell_edit_form+=' selected'
			spell_edit_form+='>'+book+'</option>'
		spell_edit_form+='</select><br /><input type="submit" name="Submit"></form>'
		templ+=spell_edit_form
	else:
		templ+="<p>Spell "+spell_name+" not found.</p>"
	return template(templ, site_name=site_name)

# Spell Search Page
@route('/spellbook/search')
def spell_search(site_name=site_config.site_name):
	templ=spell_templ+spell_search_bar
	return template(templ, site_name=site_name)
@route('/spellbook/search', method='POST')
def spell_search_result(db, site_name=site_config.site_name):
	templ=spell_templ
	spell_name=request.forms.get('spell_name')
	#'SELECT * from spells WHERE LOWER(name)=?', (spell_name.lower(),)).fetchall()
	if search_results:
		for row in search_results:
			templ+="<p>"+row[0]+"</p>"
	else:
		templ+="<p>No results found</p>"
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
	templ=base_templ+"Character Generator"
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
------------------------------------------------------------
Admin
------------------------------------------------------------
------------------------------------------------------------
"""
@route('/admin')
def admin(site_name=site_config.site_name):
	templ=base_templ+"Admin"
	return template(templ, site_name=site_name)
"""
RUN
"""
run(host='localhost', port=8080)