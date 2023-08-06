import datetime

def toval (s, engine = "postgresql"):
	if isinstance (s, datetime.date):
		return "timestamp '" + s.strftime ("%Y%m%d %H:%M:%S") + "'"
	if isinstance (s, (float, int)):
		return str (s)
	if s is None:
		return "NULL"
	return "'" + s.replace ("'", "''") + "'"

def make_update_statement (engine, tbl, dict):
	sets = []
	for k, v in dict.items ():
		sets.append ("{}={}".format (k, toval (v, engine)))		
	return "UPDATE {} SET {}".format (
		tbl,
		",".join (sets)		
	)
	
def make_insert_statement (engine, tbl, dict):	
	cols = []
	values = []
	for k, v in dict.items ():
		cols.append (k)
		values.append (toval (v, engine))		
	return "INSERT INTO {} ({}) VALUES ({})".format (
		tbl,
		",".join (cols),
		",".join (values),
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
	