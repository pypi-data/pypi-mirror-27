from . import utils
from .f import F
from . import d

OPS = {
	"gt": ">",
	"gte": ">=",
	"lt": "<",
	"lte": "<=",
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
		
		elif self.v is None:
			return ""
			
		else:
			k, v = self.k, self.v
			ll = k.split ("__")
			if len (ll) == 1:
				fd, op = k, "eq"
			else:
				if ll [-1] in (OPS):
					fd, op = ".".join (ll [:-1]), ll [-1]
				else:
					fd, op = ".".join (ll), "eq"
					
			if v is None:
				if op == "eq":
					op = "is"
					
			try:
				_op = OPS [op]
			except KeyError:
				raise TypeError ('Unknown Operator: {}'.format (op))
				
			_val = v
			_escape = True
			if op.endswith ("all"):
				fd, _val = "1", int (_val)			
			elif op == "in":
				_val = "({})".format (",".join ([d.toval (each) for each in _val]))
				_escape = False
			elif op.endswith ("contains"):				
				_val = self.add_percent (_val, 0)
			elif op.endswith ("endswith"):
				_val = self.add_percent (_val, 1)
			elif op.endswith ("startswith"):
				_val = self.add_percent (_val, 2)
			elif op == "between":
				_val = "{} AND {}".format (d.toval (_val [0], d.toval (_val [1])))		
				_escape = False				
			elif op == "isnull":
				if not _val: # False
					_op = "IS NOT"
				_val = None
			
			retval = "{} {} {}".format (fd, _op, _escape and d.toval (_val) or _val)
		
		if self._exclude:
			return "NOT (" + retval + ")"
		return retval	
	
	def _joinwith (self, op, b):
		_a = str (self)
		_b = str (b)
		if _a and _b:
			return Q ("({} {} {})".format (self, op, b))
		return _a and self or b
		
	def __str__ (self):
		return self.render ()
	
	def __or__ (self, b):
		return self._joinwith ("OR", b)
		
	def __and__ (self, b):
		return self._joinwith ("AND", b)
	
	def __invert__ (self):
		self._exclude = True
		return self


def batch (**filters):
	Qs = []
	for k, v in filters.items ():
		if v is None:
			continue
		Qs.append (Q (k, v))
	return Qs
	