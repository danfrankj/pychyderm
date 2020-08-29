from pychyderm.compute_edge import ComputeEdge
from pychyderm.data_node import DataNode
from pychyderm.dag import Dag

node_a = DataNode(node_id="a")
node_a.commit({"a": 1}, commit_sha="a=1")

node_b = DataNode(node_id="b")
node_b.commit({"b": 1}, commit_sha="b=1")

node_c = DataNode(node_id="c")
node_c.commit({"c": 100}, commit_sha="c=100")

node_merge = DataNode(node_id="merge")
node_out = DataNode(node_id="out")


def plus_func(data):
    total = 0
    for val in data.values():
        total += val
    return {"sum": total}


def plus_func_doubled(data):
    total = 0
    for val in data.values():
        total += val
    return {"sum": total * 2}


plus = ComputeEdge(edge_id="plus_all")
plus.commit(func=plus_func, commit_sha="regular_plus")
plus.commit(func=plus_func_doubled, commit_sha="double_plus")
plus.checkout(commit_sha="regular_plus")


def ident_func(data):
    return data


identity = ComputeEdge(edge_id="identity")
identity.commit(func=ident_func, commit_sha="ident")

# a -identity->
#               > merge -plus-> out
# b -identity->
dag = Dag(
    links=[
        (node_a, identity, node_merge),
        (node_b, identity, node_merge),
        (node_merge, plus, node_out),
    ],
)
dag.run()
dag.run()  # no new computation

# commit some new data
node_a.commit({"a": 2}, commit_sha="a=2")
dag.run()

# update the compute
plus.checkout("double_plus")
dag.run()
plus.checkout("regular_plus")  # reset
dag.run()  # no new compute

# add a new link
dag.add_link(node_c, identity, node_merge)
dag.run()