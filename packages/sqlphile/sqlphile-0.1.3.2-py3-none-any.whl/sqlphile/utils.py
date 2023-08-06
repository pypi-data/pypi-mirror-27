import datetime

class F:
	def __init__ (self, val):
		self.val = val
		
	def __str__ (self):
		return self.val
	
	def add_percent (self, pos = 0):
		if pos == 0:
			self.val = "'%' || " + str (self.val) + " || '%'"
		elif pos == 1:	
			self.val = "'%' || " + str (self.val)
		else:
			self.val = str (self.val) + " || '%'"	

class D:
	def __init__ (self, **data):
		self._feed = data
		self._columns = list (self._feed.keys ())
		self._encoded = False
	
	def encode (self, engine):
		if self._encoded:
			return
		_data = {}
		for k, v in self._feed.items ():
			_data [k] = toval (v, engine)
		self._feed = _data
		self._encoded = True
		
	@property
	def columns (self):	
		return ", ".join (self._columns)
	
	@property
	def values (self):		
		return ", ".join ([self._feed [c] for c in self._columns])
	
	@property
	def pairs (self):		
		return ", ".join (["{} = {}".format (c, self._feed [c]) for c in self._columns])
		

def toval (s, engine = "postgresql"):
	if isinstance (s, datetime.date):
		return "timestamp '" + s.strftime ("%Y%m%d %H:%M:%S") + "'"
	if isinstance (s, (float, int, F)):
		return str (s)
	if s is None:
		return "NULL"	
	return "'" + s.replace ("'", "''") + "'"

def toD (dict, engine):	
	d = D (**dict)
	d.encode (engine)
	return d
		
def make_update_statement (engine, tbl, dict):
	return "UPDATE {} SET {}".format (
		tbl,
		toD (dict, engine).pairs
	)
	
def make_insert_statement (engine, tbl, dict):	
	_d = toD (dict, engine)	
	return "INSERT INTO {} ({}) VALUES ({})".format (
		tbl,
		_d.columns,
		_d.values
	)

def make_select_statement (engine, tbl, fields):
	return "SELECT {} FROM {}".format (",".join (fields), tbl)

def make_delete_statement (engine, tbl):
	return "DELETE FROM {}".format (tbl)

def make_orders (order_by, keyword = "ORDER"):
	if isinstance (order_by, str):
		order_by = [order_by]
	orders = []
	for f in order_by:
		if f[0] == "-":
			orders.append (f[1:] + " DESC")
		else:
			orders.append (f)	
	return "{} BY {}".format (keyword, ", ".join (orders))
	