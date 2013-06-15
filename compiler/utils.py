import pygraphviz as pgv

from models import Node

class NodeDrawer:
	def draw(self, node):
		gr = pgv.AGraph(directed=True, rankdir='TB', ordering='out', strict=True)
		self.id = 0
		self.draw_node(gr, node)
		gr.write('foo.dot')
		image = pgv.AGraph('foo.dot')
		image.layout(prog='dot')
		image.draw('foo.png')
		image.close()

	def draw_node(self, gr, node):
		node_id = self.id
		if isinstance(node, Node):
			gr.add_node(self.id, label=node.type)
			self.id += 1

			for children in node.children:
				children_id = self.draw_node(gr, children)
				gr.add_edge(node_id, children_id)

			for leaf in node.leaf:
				leaf_id = self.id
				gr.add_node(self.id, label=leaf)
				self.id += 1
				gr.add_edge(node_id, leaf_id)
		else:
			gr.add_node(self.id, label=node)
			self.id += 1

		return node_id

