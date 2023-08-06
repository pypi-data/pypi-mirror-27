==========
SQLPhile
==========


Introduce
=============

SQLPhile is a Python styled SQL generator. It looks like Django ORM but it hasn't any relationship with Django or ORM.

But it is inspired by Django ORM and IBATIS SQL Maps.

SQLPhile might be useful for keeping clean look of your app script.

SQLPhile can make hide SQL statements for your script by using Python functions or/and writing SQL templates to seperated files.

For Example,

.. code:: python
  
  conn = psycopg2.connect (...)
	cursor = conn.cursor ()
	
	cursor.execute ("""
		SELECT type, org, count(*) cnt FROM rc_file
		WHERE org = 1 AND filename LIKE '%OCD'
		GROUP BY type		
		ORDER BY org, cnt DESC
		LIMIT 10
		OFFSET 10
	""")

This codes can be written with SQLPhile:

.. code:: python

  sp = SQLPhile ()
	
  conn = psycopg2.connect (...)
	cursor = conn.cursor ()
	
	q = sp.ops.select ("type", "count(*) cnt")
	q.filter (org = 1, name__endswith = 'OCD')
	q.group_by ("type").order_by ("org", "-cnt")[10:20]
	cursor.execute (q.as_sql ())

Or you can use SQL template file: sqlmaps/file.sql:

.. code:: sql

  <sql name="get_stat">
		SELECT type, org, count(*) cnt FROM rc_file
		WHERE {filters}
		GROUP BY type		
		ORDER BY org, cnt DESC
		{limit} {offset}
	</sql>

Your app code is,
	
.. code:: python
	
  sp = SQLPhile ("sqlmaps")
	
  conn = psycopg2.connect (...)
	cursor = conn.cursor ()
	
	q = sp.file.get_stat.filter (org = 1, name__endswith = 'OCD')[10:20]
	cursor.execute (q.as_sql ())


SQLPhile
===========

SQLPhile is main class of this package.

.. code:: python
  
	from sqlphile import SQLPhile
	
  sp = SQLPhile (dir = None, auto_reload = False, engine = "postgresql")
	
Once SQLPhile is created, you can reuse it through entire your app.

SQLPhile provide *ops* object for generic SQL operation.

.. code:: python
	
	q = sp.ops.insert (tbl, name = "Hans", created = datetime.date.today ())	
	cursor.execute (q.as_sql ())
	
	q = sp.ops.update (tbl, name = "Jenny", modified = datetime.date.today ())
	q.filter (...)
	cursor.execute (q.as_sql ())
	
	q = sp.ops.select (tbl, "id", "name", "create", "modified")
	q.filter (...)
	cursor.execute (q.as_sql ())
	
	q = sp.ops.delete (tbl)
	q.filter (...)
	cursor.execute (q.as_sql ())

If you create SQL templates in specific directory,

.. code:: python

  from sqlphile import SQLPhile
	
  sp = SQLPhile (dir = "./sqlmaps", auto_reload = True)

SQLPhile will load all of your templates in ./sqlmaps.

Assume there is a template file named 'file.sql':

.. code:: sql

  <sqlmap version="1.0">
	
  <sql name="get_stat">
		SELECT type, org, count(*) cnt FROM rc_file
		WHERE {filters}
		GROUP BY type		
		ORDER BY org, cnt DESC
		{limit} {offset}
	</sql>

It looks like XML file, BUT IT'S NOT. All tags - <sqlmap>, <sql></sql> should be started at first of line. But SQL of inside is at your own mind but I recommend give some indentation.

Now you can access each sql temnplate via filename without extension and query name attribute:
	
.. code:: python

  # filename.query name
	q = sp.file.get_stat	
	q.filter (...).order_by (...)

Note: filename is *default.sql*, you can ommit filename.

.. code:: python

	q = sp.get_stat
	q.filter (...).order_by (...)

Note 2: SHOULD NOt use "ops.*" as filename.


Filtering & Excluding
======================

filter function is very simailar with Djnago ORM.

.. code:: python

  q = sp.get_stat
	
	q.filter (id = 1)
	>> id = 1
	
	q.filter (id_exact = 1)
	>> id = 1
	
	q.filter (id_eq = 1)
	>> id = 1
	
	q.exclude (id = 1)
	>> NOT (id = 1)
	
	q.filter (id__neq = 1)
	>> id <> 1
	
	q.filter (id__gte = 1)
	>> id >= 1
	
	q.filter (id__lt = 1)
	>> id < 1

	q.filter (id__between = (10, 20))
	>> id BETWEEN 10 AND 20
	
	q.filter (name__contains = "fire")
	>> name LIKE '%fire%'
	
	q.exclude (name__contains = "fire")
	>> NOT name LIKE '%fire%'
	
	q.filter (name__startswith = "fire")
	>> name LIKE 'fire%'
	
	# escaping %
	q.filter (name__startswith = "fire%20ice")
	>> name LIKE 'fire\%20ice%'
	
	q.filter (name__endswith = "fire")
	>> name LIKE '%fire'
	
	q.filter (name = None)
	>> name IS NULL
	
	q.exclude (name = None)
	>> NOT name IS NULL
	
	q.filter (name__isnull = True)
	>> name IS NULL
	
	q.filter (name__isnull = False)
	>> name IS NOT NULL
	
Also you can add multiple filters:

.. code:: python

  q.filter (name__isnull = False, id = 4)
	>> name IS NOT NULL AND id = 4

All filters will be joined with "AND" operator.
	
How can add OR operator?

.. code:: python

	from sqlphile import Q
	
	q.filter (Q (id = 4) | Q (email__contains = "org"), name__isnull = False)
	>> name IS NOT NULL AND (id = 4 OR email LIKE '%org%')
	
Note that Q objects are first, keywords arguments late. Also you can add seperatly.

.. code:: python

	q.filter (name__isnull = False)
	q.filter (Q (id = 4) | Q (email__contains = "org"))
	>> (id = 4 OR email LIKE '%org%') AND name IS NOT NULL

All value will be escaped or automatically add single qutes, but for comparing with other fileds use *F*.

.. code:: python

  from sqlphile import F
	
	Q (email__contains = F ("org"))
	>> email LIKE 
	





