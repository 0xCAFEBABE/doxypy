"""	@namespace Foo
	A fascinating and senseless module.
"""

class Foo(object):
    """ Foo is yet another random class. """
    
    def __init__(self):
        """ Constructs Foo. """
        pass
    
    def add(self, a, b):
        """ Makes $a say $b.
        
            @param a A persons name
            @param b Something to say
            
            @returns A string containing "$a says '$b!'".
        """
        return "%s says '%s!'" % (a, b)

class Bar(Foo):
	""" Bar """
	pass

class Fnord(Foo):
	"""Fnord"""
	pass

class Hans(Bar, Fnord):
	''' Hans '''
	pass

class Peter:
	'''Peter'''
