import inspect

def func_name():
	res = inspect.stack()
	return res[1][0].f_locals['self'].__class__.__name__ + '.' + res[1][3]

class A(object):
	b = 10

	def test(self, c = b):
		print func_name()

a = A()
a.test()
