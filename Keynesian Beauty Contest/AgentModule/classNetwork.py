import networkx as nx
import matplotlib.pyplot as plt

class Network():
    def __init__(self, mode = 'undirected'):
        if mode == 'undirected': self.graph = nx.Graph()
        elif mode == 'directed': self.graph = nx.DiGraph()
        self.mode = mode
    
    def graphAddNode(self, index):
        if isinstance(index, int):
            self.graph.add_node(index)
        elif isinstance(index, list):
            self.graph.add_nodes_from(index)
    
    def graphAddEdge(self, connection):
        if isinstance(connection, tuple):
            self.graph.add_edge(connection)
        elif isinstance(connection, list):
            self.graph.add_edges_from(connection)
    
    def graphConnect(self, newIndex, mode = 'all except self'):
        if mode == 'all':
            nodeExisting = list(self.graph.nodes)
            for node in nodeExisting:
                self.graph.add_edge(newIndex, node)
            return
        elif mode == 'all except self':
            nodeExisting = list(self.graph.nodes)
            for node in nodeExisting:
                if node != newIndex:
                    self.graph.add_edge(newIndex, node)
            return
    
    def graphAddEdge(self, nodeFrom, nodeTo, connectionWeight):
        self.graph.add_edge(nodeFrom, nodeTo, weight = connectionWeight)
    
    def caluShortestPath(self, nodeFrom, nodeTo):
        varShortestPath = nx.shortest_path(self.graph, nodeFrom, nodeTo)
        return varShortestPath
    
    def caluDegree(self, index):
        varDegree = self.graph.degree[index]
        return varDegree

    def caluConnectComponents(self):
        components = list(nx.connected_components(self.graph))
        return components
    
    def caluNodeHasEdgeBetween(self, indexFrom, indexTo):
        return self.graph.has_edge(indexFrom, indexTo)
    
    def plotGraph(self, arrows = False, weight = False):
        if self.mode == 'undirected': arrows = False
        else: arrows = True

        if weight == False:
            nx.draw(self.graph, with_labels=True, node_color='lightblue', arrows = arrows)
        else:
            edge_weight = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw(self.graph, with_labels=True)
            nx.draw_networkx_edge_labels(self.graph, pos=nx.spring_layout(self.graph), edge_labels=edge_weight)

        plt.show()
