#Python 2.7
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import reactome_stats

class TestReactomeStats(unittest.TestCase):

	def setUp(self):
		self.hello_message = "Hello, ReactomeStats!"

	def test_prints_hello_reactome(self):
		output = reactome_stats.hello()
		assert(output == self.hello_message)
		

