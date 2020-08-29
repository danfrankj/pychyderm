import networkx as nx
import hashlib


class Dag:
    def __init__(self, links):  # links are node-edge->node triples
        self._digraph = nx.DiGraph()
        self._edge_index = {}
        for from_node, via_edge, to_node in links:
            self.add_link(from_node, via_edge, to_node)

    def add_link(self, from_node, via_edge, to_node):
        self._edge_index[via_edge.edge_id] = via_edge
        if from_node.node_id not in self._digraph.nodes:
            self._digraph.add_node(from_node.node_id, obj=from_node)
        if to_node.node_id not in self._digraph.nodes:
            self._digraph.add_node(to_node.node_id, obj=to_node)
        self._digraph.add_edge(from_node.node_id, to_node.node_id, obj=via_edge)

    def run(self, verbose=True):
        assert nx.is_directed_acyclic_graph(self._digraph)
        for node_id in nx.lexicographical_topological_sort(self._digraph):
            node = self._digraph.nodes[node_id]["obj"]

            upstream_ids = list(self._digraph.reverse().neighbors(node_id))
            if not upstream_ids:
                print(f"skipping {node_id}... no upstreams")
                continue

            upstreams = sorted(
                [
                    self._digraph.nodes[upstream_id]["obj"]
                    for upstream_id in upstream_ids
                ],
                key=lambda x: x.node_id,
            )
            hsh = hashlib.sha256()
            for upstream in upstreams:
                edge = self._digraph.edges[upstream.node_id, node.node_id]["obj"]
                hsh.update(upstream.commit_sha.encode("utf"))
                hsh.update(edge.commit_sha.encode("utf"))
            commit_sha = str(hsh.hexdigest())
            if node.has_commit(commit_sha):
                node.checkout(commit_sha)
                print(f"found data for ... {node.node_id}")
                continue

            node_data = {}
            for upstream in upstreams:
                upstream_data = upstream.extract()
                edge = self._digraph.edges[upstream.node_id, node.node_id]["obj"]
                print(
                    f"computing ... {upstream.node_id} -{edge.edge_id}-> {node.node_id}"
                )
                computed = edge.compute(data=upstream_data)
                node_data.update(computed)

            node.commit(node_data, commit_sha=commit_sha)

        if verbose:
            leaf_node_ids = [
                node
                for node in self._digraph.nodes()
                if self._digraph.out_degree(node) == 0
            ]
            for leaf_node_id in leaf_node_ids:
                leaf_node = self._digraph.nodes[leaf_node_id]["obj"]
                print(
                    f"terminal node {leaf_node.node_id} produced value {leaf_node.extract()}"
                )
