from pychyderm.compute_edge import ComputeEdge
from pychyderm.data_node import DataNode
from pychyderm.dag import Dag
import numpy as np

node_a = DataNode(node_id="a")
node_a.commit(1, message="a=1")

node_b = DataNode(node_id="b")
node_b.commit(1, message="b=1")

node_c = DataNode(node_id="c")
node_c.commit(100, message="c=100")

node_merge = DataNode(node_id="merge")
node_out = DataNode(node_id="out")
node_out_2 = DataNode(node_id="out_2")


def plus_func(data):
    return np.sum(data)  # np.sum handles scalars & lists


def plus_func_doubled(data):
    return np.sum(data) * 2  # np.sum handles scalars & lists


plus = ComputeEdge(edge_id="plus_all")
plus.commit(plus_func, message="regular_plus")
plus.commit(plus_func_doubled, message="double_plus")
plus.checkout_by_message(message="regular_plus")


identity = ComputeEdge(edge_id="identity")
identity.commit(lambda data: data, message="ident")

# a -identity->
#               > merge -plus-> out
# b -identity->
dag = Dag(
    links=[
        (node_a, identity, node_merge),
        (node_b, identity, node_merge),
        (node_merge, plus, node_out),
        (node_merge, identity, node_out_2),
    ],
)
dag.run()
dag.run()  # no new computation

# commit some new data
node_a.commit(2, message="a=2")
dag.run()

# update the compute
plus.checkout_by_message("double_plus")
dag.run()
plus.checkout_by_message("regular_plus")  # reset
dag.run()  # no new compute

# add a new link
dag.add_link(node_c, identity, node_merge)
dag.run()