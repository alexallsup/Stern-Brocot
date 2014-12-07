def mediant(frac1, frac2):
	"""Returns the mediant (n1+n2)/(d1+d2) of the two fractions, represented as a 2-tuple (n,d).
	frac1 and frac2 are given as 2-tuples (n,d)"""
	# print "%s m %s = %s" % (frac1, frac2, (frac1[0]+frac2[0], frac1[1]+frac2[1])
	return (frac1[0]+frac2[0], frac1[1]+frac2[1])

def compare_fracs(frac1, frac2):
	"""Return True if frac1 is greater than frac2."""
	return frac1[0]*frac2[1] > frac2[0]*frac1[1]

class SBNode():
	"""Represents one node in the Stern-Brocot tree"""
	def __init__(self, frac=(1,1), is_left_child=True, parent=None):
		self.parent = parent # the node this stems from. None if the top of the tree.
		self.frac = frac # the fraction at this node
		self.is_left_child = is_left_child # which side of the tree this is on

		self.left_child = None  # will be SBNode objects representing the object beneath this in the tree
		self.right_child = None

	def get_left_frac(self):
		"""returns the existing fraction immediately to the left of this one"""
		if self.parent == None:
			# if this is the root node
			return (0,1)
		elif self.is_left_child:
			# if the left side, run up the tree until we find a right child
			return self.parent.get_left_frac()
		else:
			# if right child, just return the fraction above it
			return self.parent.frac

	def get_right_frac(self):
		"""returns the fraction immediately to the right of this one"""
		if self.parent == None:
			# if this is the root node
			return (1,0)
		elif self.is_left_child:
			# if the left side, just return the fraction above it
			return self.parent.frac
		else:
			# if right child, run up the tree til we find a left child
			return self.parent.get_right_frac()

	def gen_children(self, max_denom=None, max_depth=None, current_depth=0):
		"""Populates self.left, self.right with the proper child nodes. 
		If max_denom is given, the children also generate their nodes until the maximum denominator is reached. While in max_denom mode, all created nodes will be <1, otherwise the tree blows up to infinity.
		If max_depth is given, it will generate that many layers of the tree. Depth is indexed from 0 s.t. the 1/1 node has depth 0. Externally this should be called as node.gen_children(max_depth=x).
		If neither are given, the children do not generate any further nodes.
		"""
		left_child_frac  = mediant(self.frac, self.get_left_frac() )
		right_child_frac = mediant(self.frac, self.get_right_frac())

		# print "%s generating children %s and %s" % (self.frac, left_child_frac, right_child_frac)

		if max_denom != None:
			if left_child_frac[1]  < max_denom and left_child_frac[0]  < left_child_frac[1]:
				self.left_child  = SBNode(frac=left_child_frac,  is_left_child=True,  parent=self)
				self.left_child.gen_children(max_denom=max_denom)

			if right_child_frac[1] < max_denom and right_child_frac[0] < right_child_frac[1]:
				self.right_child = SBNode(frac=right_child_frac, is_left_child=False, parent=self)
				self.right_child.gen_children(max_denom=max_denom)

		elif max_depth != None and current_depth < max_depth:
			self.left_child  = SBNode(frac=left_child_frac,  is_left_child=True,  parent=self)
			self.right_child = SBNode(frac=right_child_frac, is_left_child=False, parent=self)
			self.left_child.gen_children( max_depth=max_depth, current_depth=current_depth+1)
			self.right_child.gen_children(max_depth=max_depth, current_depth=current_depth+1)

	def get_tree_below(self, max_depth=None, current_depth=0):
		"""Can be called recursively. Will return a list, sorted L2G, of the 2-tuple fractions below in the tree.
		If max_depth and current_depth given, will return the row of the tree at a certain depth. Depth is indexed from 0; ie the 1/1 node has depth 0.
		Otherwise, will return the entire tree with no divisions.
		External calls should look like node.get_tree_below(max_depth)"""
		tree_list = []
		if max_depth == None:
			# if we are not returning a row.
			if self.left_child != None:
				# if this is not the base of the tree
				tree_list = self.left_child.get_tree_below()
				tree_list.append(self.frac)
				tree_list = tree_list + self.right_child.get_tree_below()
			else:
				# if this is the base of the tree
				tree_list = [self.frac]
		else:
			if current_depth == max_depth:
				# if this is the deepest level we want to go to
				tree_list = self.frac
			else:
				# WE NEED TO GO DEEPER
				left_side  = self.left_child.get_tree_below( max_depth, current_depth+1)
				right_side = self.right_child.get_tree_below(max_depth, current_depth+1)

				tree_list = left_side + right_side
		return tree_list

	def get_leftmost_child(self):
		"""Returns the node furthest down the tree to the left. This one if it doesn't have a left child."""
		if self.left_child == None:
			return self
		else:
			return self.left_child.get_leftmost_child()

	def get_rightmost_child(self):
		"""Returns the node furthest down the tree to the right. This one if it doesn't have a right child."""
		if self.right_child == None:
			return self
		else:
			return self.right_child.get_rightmost_child()

	def get_lowest_right_parent(self):
		"""returns the lowest parent up the tree from herethat is a right child."""
		if self.parent == None:
			# if we reached the top of the tree
			# just return this node bc the 1/1 node is technically a child of both the 1/0 and 0/1 nodes
			return self
		elif not self.parent.is_left_child:
			# the parent is a right child
			return self.parent
		else:
			# the parent is a left child
			return self.parent.get_lowest_right_parent()

	def get_lowest_left_parent(self):
		"""returns the lowest parent up the tree from herethat is a right child."""
		if self.parent == None:
			# if we reached the top of the tree
			# just return this node bc the 1/1 node is technically a child of both the 1/0 and 0/1 nodes
			return self
		elif not self.parent.is_left_child:
			# the parent is a right child
			return self.parent.get_lowest_left_parent()
		else:
			# the parent is a left child
			return self.parent

	def get_left_node(self):
		"""Returns the node immediately adjacent to this one on the left."""
		if self.left_child == None:
			# if we are at the end of a branch
			lowest_right_parent = self.get_lowest_right_parent()
			if lowest_right_parent.parent == None:
				# if this was called from left edge of the tree
				# the lowest right parent is the 1/1 node
				# return the 0/1 node on the left edge of the tree
				return SBNode(frac=(0,1))
			else:
				# if we had a lower right parent
				return lowest_right_parent.parent
		else:
			return self.left_child.get_rightmost_child()

	def get_right_node(self):
		"""Returns the node immediately adjacent to this one on the right."""
		if self.right_child == None:
			# if we are at the end of a branch
			lowest_left_parent = self.get_lowest_left_parent()
			if lowest_left_parent.parent == None:
				# if this was called from right edge of the tree
				# the lowest left parent is the 1/1 node
				# return the 1/0 (infinity) node on the right edge of the tree
				return SBNode(frac=(1,0))
			else:
				# if we had a lower left parent
				return lowest_left_parent.parent
		else:
			return self.right_child.get_leftmost_child()	

	def list_repr(self):
		"""Returns a list of the contents of this node and the tree below it.
		Format: [(n,d), left_list, right_list] if it has children, [(n,d)] otherwise.
		"""
		contents = [self.frac]
		if self.left_child  != None:
			contents.append( self.left_child.list_repr())
		if self.right_child != None:
			contents.append(self.right_child.list_repr())
		return contents

	def search_tree(self, tgt_frac):
		"""Search through the tree and return the SBNode with the target fraction."""
		if self.frac == tgt_frac:
			return self
		elif compare_fracs(self.frac, tgt_frac):
			# tgt is less than self and to left
			return self.left_child.search_tree(tgt_frac)
		else:
			# tgt is greater than self and to right
			return self.right_child.search_tree(tgt_frac)

	def __str__(self):
		return "%s/%s" % (self.frac[0], self.frac[1])

def print_nested_list(nest_list, indent_depth=0):
	for i in xrange(len(nest_list)):
		s = ""
		for j in xrange(indent_depth):
			s += "	"
		if i == 0:
			s += str(nest_list[i])
			indent_depth += 1
			print s
		else:
			print_nested_list(nest_list[i], indent_depth=indent_depth)


if __name__ == '__main__':
	root = SBNode()
	try:
		root.gen_children(max_depth=4)
	except RuntimeError, e:
		print "Stack overflowed."
	print root.list_repr()
	print_nested_list(root.list_repr())