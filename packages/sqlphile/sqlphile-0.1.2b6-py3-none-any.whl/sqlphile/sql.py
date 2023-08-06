from . import utils
from .q import Q, batch

class SQL:
	def __init__ (self, template, engine = "postgresql"):	
		self._template = template		
		self._engine = engine
		self._filters = []
		self._limit = 0
		self._offset = 0
		self._order_by = None
		self._group_by = None
		self._having = None
		self._returning = None
		self._feed = {}
		self._data = {}
		
	@property
	def query (self):
		return self.as_sql ()
	
	def exclude (self, *Qs, **filters):
		for q in Qs + tuple (batch (**filters)):
			self._filters.append ("NOT (" + str (q) + ")")		
		return self
	
	def returning	(self, *args):
		self._returning = "RETURNING " + ", ".join (args)
		return self
	
	def filter (self, *Qs, **filters):
		for q in Qs + tuple (batch (**filters)):
			self._filters.append (str (q))		
		return self
	
	def having (self, cond):
		self._having = "HAVING " + cond
		return self
		
	def order_by (self, *by):
		self._order_by = utils.make_orders (by)
		return self
	
	def group_by (self, *by):
		self._group_by = utils.make_orders (by, "GROUP")
		return self
		
	def limit (self, val):
		self._limit = "LIMIT {}".format (val)
		return self
	
	def offset (self, val):
		self._offset = "OFFSET {}".format (val)
		return self
	
	def __getitem__(self, key):
		key.start and self.offset (key.start)
		if key.stop:
			self.limit (key.stop - (key.start or 0))
		return self
		
	def as_sql (self):
		raise NotImplementedError
		

class SQLInjector (SQL):
	def __call__ (self, **karg):
		return self.feed (**karg)
	
	def encode (self, **karg):
		_data = {}
		for k, v in karg.items ():
			_data [k] = utils.toval (v, self._engine)
		return utils.D (**_data)
			
	def data (self, **karg):
		for k, v in karg.items ():
			self._data [k] = utils.toval (v, self._engine)
		return self
		
	def feed (self, **karg):		
		for k, v in karg.items ():
			self._feed [k] = v
		return self
	
	def as_sql (self):
		data = utils.D (**self._data)		
		self._feed.update (self._data)
		
		return self._template.format (
			_filters = " AND ".join (self._filters),
			_limit = self._limit,
			_offset = self._offset,
			_order_by = self._order_by,
			_group_by = self._group_by,
			_having = self._having,
			_columns = data.columns,
			_values = data.values,
			_pairs = data.pairs,
			_returning = self._returning,
			**self._feed
		)

class SQLMerger (SQL):	
	def as_sql (self):
		sql = [self._template]
		self._filters and sql.append ("WHERE " + " AND ".join (self._filters))
		if self._group_by:
			sql.append (self._group_by)
			self._having and sql.append (self._having)
		self._order_by and sql.append (self._order_by)
		self._limit and sql.append (self._limit)
		self._offset and sql.append (self._offset)
		self._returning and sql.append (self._returning)
		return "\n".join (sql)
