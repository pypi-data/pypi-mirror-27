from . import utils
from .f import F
from . import d

OPS = {
	"gt": ">",
	"gte": ">=",
	"lt": "<",
	"lte": "<=",
	"is": "IS",
	"isnot": "IS NOT",
	"neq": "<>",
	"eq": "=",
	"exact": "=",
	"in": "IN",
	"notin": "NOT IN",
	"isnull": "IS",
	"exists": "EXISTS",
	"nexists": "NOT EXISTS",
	"between": "BETWEEN",
	"contains": "LIKE",
	"startswith": "LIKE",
	"endswith": "LIKE",
	"ncontains": "NOT LIKE",
	"nstartswith": "NOT LIKE",
	"nendswith": "NOT LIKE",	
	"all": "=",	
}

class Q:
	def __init__ (self, *args, **kargs):
		self._str = None		
		if kargs:
			assert len (kargs) == 1
			self.k, self.v = kargs.popitem ()
		elif len (args) == 2:
			self.k, self.v = args
		else:	
			self._str = args [0]
		self._exclude = False
	
	def add_percent (self, val, pos = 0):
		if isinstance (val, F):
			val.add_percent (pos)
			return val
		val = val.replace ("%", "\\%")
		if pos == 0:
			return "%" + val + "%"
		elif pos == 1:	
			return "%" + val
		return val + "%"
			
	def render (self):
		if self._str:
			retval = "({})".format (self._str)
		
		else:
			k, v = self.k, self.v
			
			try:
				fd, op = k.split ("__", 1)
			except ValueError:
				fd, op = k, "eq"
			
			if v is None:
				if op == "eq":
					op = "is"
					
			try:
				_op = OPS [op]
			except KeyError:
				raise TypeError ('Unknown Operator: {}'.format (op))
				
			_val = v
			if op.endswith ("all"):
				fd, _val = "1", int (_val)
			elif op.endswith ("contains"):				
				_val = self.add_percent (_val, 0)
			elif op.endswith ("endswith"):
				_val = self.add_percent (_val, 1)
			elif op.endswith ("startswith"):
				_val = self.add_percent (_val, 2)
			elif op == "between":
				_val = "{} AND {}".format (d.toval (_val [0], d.toval (_val [1])))		
			elif op == "isnull":
				if not _val: # False
					_op = "IS NOT"
				_val = None
			
			retval = "{} {} {}".format (fd, _op, d.toval (_val))
		
		if self._exclude:
			return "NOT (" + retval + ")"
		return retval	
		
	def __str__ (self):
		return self.render ()
	
	def __or__ (self, b):
		return Q ("({} OR {})".format (self, b))
	
	def __and__ (self, b):
		return Q ("({} AND {})".format (self, b))	
	
	def __invert__ (self):
		self._exclude = True
		return self


def batch (**filters):
	Qs = []
	for k, v in filters.items ():
		Qs.append (Q (k, v))
	return Qs
	