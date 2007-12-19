"""foo
bar"""
import re ''' ford '''

def multiline1(v1,
		v2,
		v3):
	"""comment"""
	pass

def multiline2  (  
		v1,
		v2,
		v3):
	"""comment \\brief yay"""
	pass

class MyClass:
	def __init__(self, arg=Null):
		""" Class constructor
		
		Example of how you should do if you override
		the constructor in a subclass.
		
		@code
		class MySubClass(MyClass):
			TOTO = "something"	# some comment
			
			def __init__(self, arg):
				MyClass.__init__(self, param1)
				# your own code follows here
		@endcode
		"""
		pass

def test0():
	"""not
	brief"""
	pass

def test1():
	""""""
	pass 

def test2():
	"""
	"""
	pass 

def test3():
	"""
"""
	pass 

def test4():
	"""foo
	bar
foobar
	fnord
		asdf
			lalalla"""

class Foo:
	"""class doc"""
	def test5(self):
		"""AASDF"""
	
	@staticmethod
	def test6():
		"""FOOBAR"""

##
# doxy string
def test7():
	"""doc string"""
	"""more doc string"""
	
	"""even much more"""

def test8():
	"""	my doc
		string
	and mine alone
	"""
	
def test9():
	''' Shalalalala """ a comment '''
	
def test10():
	""" Blub ''' and the same reverse """
	
