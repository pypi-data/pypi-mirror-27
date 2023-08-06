import os
import re
from . import utils
from . import sql
from .ops import Operation
from .sql import SQL, SQLTemplateRederer, SQLComposer
from .sqlmap import SQLMap
from .q import Q, IN, B
from .d import D
from .f import F

__version__ = "0.1.4b6"

class SQLPhile:
	def __init__ (self, dir = None, auto_reload = False, engine = "postgresql"):
		self._dir = dir
		self._auto_reload = auto_reload
		self._engine = engine
		self._ns = {}
		self._dir and self._load_sqlmaps ()
	
	@property
	def ops (self):
		return Operation (self._engine)
		
	def template (self, template):
		q = sql.SQLTemplateRederer (template, self._engine)
		return q
		
	def __getattr__ (self, name):
		try:
			return self._ns [name]
		except KeyError:
			return getattr (self._ns ["default"], name)
	
	def _load_sqlmaps (self):	
		for fn in os.listdir (self._dir):
			if fn[0] == "#":
				continue			
			ns = fn.split (".") [0]
			if ns == "ops":
				raise NameError ('ops cannot be used SQL map file name')
			self._ns [ns] = SQLMap (os.path.join (self._dir, fn), self._auto_reload, self._engine)
