# encoding=utf-8

import time
import functools


def timer(func):
	"""
	装饰器函数，用于计算func运行耗时，并将运行时间输出至屏幕上，结果保留小数点后3位

	类似的有timeit等
	:param func:
	:return:
	"""

	@functools.wraps(func)
	def _wrapper(*args, **kwargs):
		start = time.time()
		r = func(*args, **kwargs)
		end = time.time()
		cost = end - start
		print '耗时：%0.3f s' % cost
		return r

	return _wrapper
