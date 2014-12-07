def mediant(frac1, frac2):
	"""Returns the mediant (n1+n2)/(d1+d2) of the two fractions, represented as a 2-tuple (n,d).
	frac1 and frac2 are given as 2-tuples (n,d)"""
	return (frac1[0]+frac2[0], frac1[1]+frac2[1])

def compare_fracs(frac1, frac2):
	"""Return frac1 > frac2"""
	return frac1[0]*frac2[1] > frac2[0]*frac1[1]

def create_node(frac):
	"""Returns an ProcSBNode with a parent chain all the way up from the desired fraction."""
	root_node = ProcSBNode()
	while root_node.frac != frac:
		if compare_fracs(root_node.frac, frac):
			# frac is to the left
			child_frac = mediant(root_node.left_frac, root_node.frac)
			root_node = ProcSBNode(frac=child_frac, is_left_child=True, parent=root_node, left=root_node.left_frac, right=root_node.frac)
		else:
			child_frac = mediant(root_node.right_frac, root_node.frac)
			root_node = ProcSBNode(frac=child_frac, is_left_child=False, parent=root_node, left=root_node.frac, right=root_node.right_frac)
	return root_node

class ProcSBNode():
	"""Procedurally generated node in the Stern-Brocot tree"""
	def __init__(self, frac=(1,1), is_left_child=True, parent=None, left=(0,1), right=(1,0)):
		self.parent = parent # the node this stems from. None if the top of the tree.
		self.frac = frac # the fraction at this node
		self.is_left_child = is_left_child # which side of immediate tree this is on
		self.left_frac = left # keep track of the fractions to the left and right of this one
		self.right_frac = right

		self.l_counted = False
		self.r_counted = False
		# print "Node:", frac

	def get_leftmost_child(self, max_denom):
		"""Returns the node furthest down the tree to the left that still has a denominator < max_denom"""
		child = self
		frac = mediant(child.frac, child.left_frac)
		while frac[1] < max_denom:
			child = ProcSBNode(frac=frac, is_left_child=True, parent=child, left=child.left_frac, right=child.frac)
			frac = mediant(child.frac, child.left_frac)
		return child

	def get_rightmost_child(self, max_denom):
		"""Returns the node furthest down the tree to the right that still has a denominator < max_denom"""
		child = self
		frac = mediant(child.frac, child.right_frac)
		while frac[1] < max_denom:
			child = ProcSBNode(frac=frac, is_left_child=False, parent=child, left=child.frac, right=child.right_frac)
			frac = mediant(child.frac, child.right_frac)
		return child

	def get_lowest_right_parent(self):
		"""returns the lowest parent up the tree from here that is a right child."""
		# no difference from non-procedural model
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
		# no difference from non-procedural model
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

	def get_left_rational_number(self, max_denom):
		"""Returns the rational number immediately adjacent to this one on the left."""
		if mediant(self.frac, self.left_frac)[1] >= max_denom:
			# if at the end of the branch to the left
			if self.is_left_child:
				return self.get_lowest_right_parent().parent
			else:
				# if it is a right branch, the closest is just the parent
				return self.parent
		else:
			# if we have to go further down the tree
			left_child = ProcSBNode(frac=mediant(self.frac, self.left_frac), is_left_child=True, parent=self, left=self.left_frac, right=self.frac)
			return left_child.get_rightmost_child(max_denom)

	def get_right_rational_number(self, max_denom):
		"""Returns the rational number immediately adjacent to this one on the right."""
		if mediant(self.frac, self.right_frac)[1] >= max_denom:
			# if at the end of the branch to the right
			if not self.is_left_child:
				return self.get_lowest_left_parent().parent
			else:
				# if it is a left branch, the closest is just the parent
				return self.parent
		else:
			# if we have to go further down the tree
			right_child = ProcSBNode(frac=mediant(self.frac, self.right_frac), is_left_child=False, parent=self, left=self.frac, right=self.right_frac)
			return right_child.get_leftmost_child(max_denom)

	def get_left_child(self):
		"""Returns the left child of the current node."""
		return ProcSBNode(frac=mediant(self.frac, self.left_frac), is_left_child=True, parent=self, left=self.left_frac, right=self.frac)

	def get_right_child(self):
		"""Returns the right child of the current node."""
		return ProcSBNode(frac=mediant(self.frac, self.right_frac), is_left_child=False, parent=self, left=self.frac, right=self.right_frac)

	def denom(self):
		"""Returns the denominator of the fraction."""
		return self.frac[1]

	def numer(self):
		"""Returns the numerator of the fraction."""
		return self.frac[0]

	def search_tree(self, tgt_frac, max_denom):
		"""Search through the tree and return the SBNode with the target fraction."""
		child = self
		while child.frac != tgt_frac:
			if compare_fracs(child.frac, tgt_frac):
				# child > tgt
				# too far right
				child = ProcSBNode(frac=mediant(self.frac, self.left_frac), is_left_child=True, parent=self, left=self.left_frac, right=self.frac)
			else:
				# child < tgt
				# too far left
				child = ProcSBNode(frac=mediant(self.frac, self.right_frac), is_left_child=False, parent=self, left=self.frac, right=self.right_frac)

	def get_tree_size(self, max_denom):
		"""Return the number of nodes in the tree with d<max_denom including this one."""
		node = self
		count = 1
		while True:
			# print node, node.l_counted, node.r_counted
			if node.frac == self.frac and node.l_counted and node.r_counted:
				break
			if not node.l_counted:
				left_child = node.get_left_child()
				
				node.l_counted = True
				if left_child.denom() <= max_denom and left_child.denom() > left_child.numer():
					# if the next node is still valid within the constraintsj
					print "L",left_child
					count += 1
					node = left_child
			elif not node.r_counted:
				right_child = node.get_right_child()
				
				node.r_counted = True
				if right_child.denom() <= max_denom and right_child.denom() > right_child.numer():
					# if the next node is still valid within the constraints
					print "R",right_child
					count += 1
					node = right_child
			else:
				# if both have been counted
				node = node.parent
		return count


	def __str__(self):
		return "%s/%s" % (self.frac[0], self.frac[1])

if __name__ == '__main__':
	root = ProcSBNode()
	print root.get_tree_size(5)