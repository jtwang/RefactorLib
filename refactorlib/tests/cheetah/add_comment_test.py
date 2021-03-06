from refactorlib.cheetah.parse import parse

def test_can_add_comments():
	"""
	It's often useful to simply add comment to code, automatically.
	"""
	example = parse('''
		#def foo
			$esc(
				$_('My translated string.')
			)
		#end def
	''')

	calls = example.find_calls('_')
	assert len(calls) == 1, calls

	calls[0].add_comment('1 _')
	calls[0].add_comment('2 _')
	calls[0].add_comment('3 _')
	
	calls = example.find_calls('esc')
	assert len(calls) == 1, calls

	calls[0].add_comment('1 esc')
	calls[0].add_comment('2 esc')
	calls[0].add_comment('3 esc')

	assert '''
		#def foo
			## 1 esc
			## 2 esc
			## 3 esc
			$esc(
				## 1 _
				## 2 _
				## 3 _
				$_('My translated string.')
			)
		#end def
	''' == example.totext()
