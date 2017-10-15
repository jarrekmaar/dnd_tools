import math
import sqlite3
from sqlite3 import Error
def get_modifier( abScore ):
	if not isinstance( abScore, int ):
		raise ValueError('Not an integer.')
	if abScore < 0:
		raise ValueError('Must be a value >= 0.')
	modifier = int(math.floor((abScore-10)/2))
	return modifier

def get_proficiency_bonus( level ):
	if not isinstance( level, int ):
		raise ValueError('Not an integer.')
	if level <= 0:
		raise ValueError('Must be a value > 0.')
	bonus = math.floor((level/4.1)+2)
	return bonus

def get_spell_attack_mod( level, casting_modifier ):
	if not (isinstance( level, int ) or isinstance( casting_modifier, int)):
		raise ValueError('Not an integer.')
	if level <= 0:
		raise ValueError('Level be a value > 0.')
	spell_attack_mod = get_proficiency_bonus(level)+casting_modifier
	return spell_attack_mod

def get_spell_save_dc( level, casting_modifier ):
	save_dc = get_spell_attack_mod( level, casting_modifier )+8
	return save_dc