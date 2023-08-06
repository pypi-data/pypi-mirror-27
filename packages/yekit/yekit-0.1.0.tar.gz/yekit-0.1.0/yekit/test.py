# encoding=utf-8

from kit import timer


@timer
def test():
	m = 0
	for i in range(100):
		m += 1
		print m

if __name__ == '__main__':
	test()