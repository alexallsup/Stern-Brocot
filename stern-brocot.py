def mediant(frac1, frac2):
	"""Returns the mediant (n1+n2)/(d1+d2) of the two fractions, represented as a 2-tuple (n,d).
	frac1 and frac2 are given as 2-tuples (n,d)"""
	# print "%s m %s = %s" % (frac1, frac2, (frac1[0]+frac2[0], frac1[1]+frac2[1])
	return (frac1[0]+frac2[0], frac1[1]+frac2[1])

class SBNode():
	"""Represents one node in the Stern-Brocot tree"""
	def __init__(self, frac=(1,1), is_left_child=True, parent=None):
		self.parent = parent # the node this stems from. None if the top of the tree.
		self.frac = frac # the fraction at this node
		self.is_left_child = is_left_child # which side of the tree this is on

		self.left_child = None  # will be SBNode objects representing the object beneath this in the tree
		self.right_child = None

	def get_left_frac(self):
		# returns the existing fraction immediately to the left of this one
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
		# returns the fraction immediately to the right of this one
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
				self.left_child.gen_children(max_denom)

			if right_child_frac[1] < max_denom and right_child_frac[0] < right_child_frac[1]:
				self.right_child.gen_children(max_denom)
				self.right_child = SBNode(frac=right_child_frac, is_left_child=False, parent=self)

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

	def list_repr(self):
		"""Returns a list of the contents of this node and the tree below it.
		Format: [(n,d), left_list, right_list] if it has children, [(n,d)] otherwise.
		"""
		contents = [self.frac]
		if left_child  != None:
			contents.append( left_child.list_repr())
		if right_child != None:
			contents.append(right_child.list_repr())
		return contents

	def __str__(self):
		return "%s/%s" % (self.frac[0], self.frac[1])

def gen_SB_tree(max_denom):
	"""Generate a Stern-Brocot tree with all denominators less than max_denom. Returns the root node."""
	root_node = SBNode()
	root_node.gen_children(max_denom)
	return root_node

if __name__ == '__main__':
	root = SBNode()
	try:
		root.gen_children(max_denom=4)
	except RuntimeError, e:
		print "Stack overflowed."
	print root.list_repr()