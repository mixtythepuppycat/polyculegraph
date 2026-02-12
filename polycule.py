from enum import Enum
import networkx as nx
import gravis as gv
import os

class RelationshipType(Enum):
    Partner = "red"
    Dating = "yellow"
    Married = "purple"
    FWB = "green"
    Unknown = "gray"

class RegistrationError(Exception):
    pass

class Polycule:
    def __init__(self, id):
        self.id = id
        if os.path.isfile(f"{self.id}.gml"):
            self.G = nx.read_gml(f"{self.id}.gml", destringizer=int)
        else:
            self.G = nx.Graph()

            self.G.graph['node_label_size'] = 15
            self.G.graph['node_label_color'] = 'black'

            self.G.graph['edge_label_size'] = 10
            self.G.graph['edge_label_color'] = 'blue'

    def add_relationship(self, id: int, partnerId: int, partnerName: str, type: RelationshipType):
        # Check to see if they were registered as an offserver node.
        # If the partner already exists
        
        if self.G.has_node(id) is False or self.G.nodes[id].get("claimed") is False:
            raise RegistrationError("Need to register")
        if partnerId is None:
            partnerId = partnerName
            self.G.add_node(partnerId, display_name=partnerName, id_not_unique=True)
        elif self.G.has_node(partnerId) is False:
            self.G.add_node(partnerId, display_name=partnerName, claimed=False)
            
        self.G.add_edge(id, partnerId, relationship=type.name, color=type.value, click=f"Relationship Type: {type.name}", size=5)

    def get_relationships(self, member: int) -> str:
        response = "You have registered the following partners:\n"

        for nbr, datadict in self.G.adj[member].items():
            response += f"{self.G.nodes[nbr]['display_name']} ({datadict['relationship']})\n"
        
        return response
    
    def remove_relationship(self, id: int, partnerId: str, discord: bool = True):
        if discord:
            self.G.remove_edge(id, partnerId)
        else:
            partnerId = (id, partnerId)
            self.G.remove_edge(id, partnerId)

            # If this was the last link to the partner, remove them from the graph
            if self.G.degree(partnerId) == 0:
                self.G.remove_node(partnerId)

    def register(self, userId: int, display_name: str, pronouns:str = "", type:str = ""):
        self.G.add_node(userId, display_name=display_name, click=f"Pronouns: {pronouns}<br/>Critter Type: {type}", claimed=True)

    def render_graph(self):
        nx.write_gml(self.G, f"{self.id}.gml")
        graph = gv.d3(data=self.G, graph_height=880, use_collision_force=True, zoom_factor=1.5, 
                    show_details=True, use_many_body_force=False, use_links_force=True,
                    links_force_strength=1, collision_force_strength=1, node_label_data_source="display_name")
        graph.export_html(f"{self.id}.html", overwrite=True)

class Polycules:
    def __init__(self):
        self.store: dict = {}

    def get(self, polyculeId: int) -> Polycule:
        polycule = self.store.get(polyculeId)
        if polycule is None:
            polycule = Polycule(polyculeId)
            self.store[polyculeId] = polycule
        
        return polycule