import os
import re
from . import utils
from . import sql
from .sql import SQL, SQLInjector, SQLMerger
from .q import Q
from .utils import F, D

__version__ = "0.1.2b5"

class SQLMap:
	def __init__ (self, map = None, auto_reload = False, engine = "postgresql"):
		self._map = map
		self._auto_reload = auto_reload
		self._engine = engine
		self._version = "1.0"
		self._sqls = {}
		self._last_modifed = 0
		if self._map:
			self._read_from_file ()
	
	def __getattr__ (self, name):		
		self._reloaderble () and self._read_from_file ()
		return sql.SQLInjector (self._sqls.get (name), self._engine)
		
	def _reloaderble (self):
		return self._map and self._auto_reload and self._last_modifed != os.path.getmtime (self._map)
		
	def _read_from_file (self):
		self._last_modifed = os.path.getmtime (self._map)
		with open (self._map) as f:
			self._read_from_string (f.read ())
	
	RX_NAME	= re.compile ("\sname\s*=\s*['\"](.+?)['\"]")
	RX_VERSION	= re.compile ("\sversion\s*=\s*['\"](.+?)['\"]")
	def _read_from_string (self, data):
		current_name = None
		current_data = []
		for line in data.split ("\n"):
			if not line.strip ():
				continue
			
			if line.startswith ("<sqlmap "):
				m = self.RX_VERSION.search (line)
				if m:					
					self._version = m.group (1)
				
			elif line.startswith ("</sql>"):
				if not current_name:
					raise ValueError ("unexpected end tag </sql>")
				self._sqls [current_name] = "\n".join (current_data)
				current_name, current_data = None, []				 
			
			elif line.startswith ("<sql "):
				m = self.RX_NAME.search (line)
				if not m:
					raise ValueError ("name attribute required")
				current_name = m.group (1)
			
			elif current_name:
				current_data.append (line.strip ())


class Operation:
	def __init__ (self, engine = 'postresql'):
		self.engine = engine
		
	def insert (self, tbl, **fields):		
		return sql.SQLMerger (utils.make_insert_statement (self.engine, tbl, fields), self.engine)
	
	def update (self, tbl, **fields):		
		return sql.SQLMerger (utils.make_update_statement (self.engine, tbl, fields), self.engine)		
	
	def select (self, tbl, *fields):		
		return sql.SQLMerger (utils.make_select_statement (self.engine, tbl, fields), self.engine)		
	
	def delete (self, tbl):
		return sql.SQLMerger (utils.make_delete_statement (self.engine, tbl), self.engine)


class SQLPhile:
	def __init__ (self, dir = None, auto_reload = False, engine = "postgresql"):
		self._dir = dir
		self._auto_reload = auto_reload
		self._engine = engine
		self.ops = Operation (self._engine)
		self._ns = {}
		self._dir and self._load_sqlmaps ()
		
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
