def parse(filename, filetype=None, encoding=None):
	from filetypes import FILETYPES
	filetype = FILETYPES.detect_filetype(filename, filetype)

	source = open(filename).read()

	# If no encoding was explicitly specified, see if we can parse
	# it out from the contents of the file.
	if encoding is None:
		encoding = filetype.encoding_detector(source)

	if encoding:
		source = unicode(source, encoding)
	else:
		# I don't see why encoding=None is different from not specifying the encoding.
		source = unicode(source)

	return filetype.parser(source)

def dictnode_to_lxml(tree, element_factory=None):
	"""
	Input: A dictionary-based representation of a node tree.
	Output: An lxml representation of the same.

	Each dictionary has three attributes:
	    name -- The type of node, a string. In html, this would be the tag name.
		text -- The content of the node: <b>text</b>
		tail -- Any content after the end of this node, but before the start of the next: <br/>tail
		attrs -- A dictionary of any extra attributes.
		children -- An ordered list of more node-dictionaries.
	"""
	if element_factory:
		Element = element_factory
	else:
		from node import RefactorLibNode as Element

	root = None
	stack = [ (tree,root) ]

	while stack:
		node, parent = stack.pop()

		lxmlnode = Element(node['name'], attrib=node['attrs'])
		lxmlnode.text = node['text']
		lxmlnode.tail = node['tail']

		if parent is None:
			root = lxmlnode
		else:
			parent.append(lxmlnode)

		for child in reversed(node['children']):
			stack.append((child, lxmlnode))

	return root
