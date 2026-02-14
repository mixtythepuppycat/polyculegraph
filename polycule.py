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

class NodeNotFound(Exception):
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

    # For adding your own relationship
    def add_self_relationship(self, self_id: int, partner_id: int, partner_name: str, type: RelationshipType):        
        if self.G.has_node(self_id) is False or self.G.nodes[self_id].get("claimed") is False:
            raise RegistrationError("Need to register")
        
        # add the partner in case they don't exist yet
        partner_id = self._add_node(partner_id, partner_name)

        self._add_edge(self_id, partner_id, type)

    # Intended for polycule admins, limit access when possible
    def add_others_relationship(self, person1_id, person1_name: str, person2_id, person2_name: str, relationship_type: RelationshipType):
        person1_id = self._add_node(person1_id, person1_name)
        person2_id = self._add_node(person2_id, person2_name)
        self._add_edge(person1_id, person2_id, relationship_type)

    def _add_node(self, id: int, display_name: str, pronouns:str = "", type:str = "", claimed: bool = False, force_update: bool = False):
        unique_id = True
        if id is None:
            id = display_name
            unique_id = False

        if not self.G.has_node(id) or force_update:
            self.G.add_node(id, display_name=display_name, click=f"Pronouns: {pronouns}<br/>Critter Type: {type}", claimed=claimed, unique_id=unique_id)

        return id

    def _add_edge(self, person1_id, person2_id, type: RelationshipType):
        self.G.add_edge(person1_id, person2_id, relationship=type.name, color=type.value, click=f"Relationship Type: {type.name}", size=5)

    def get_relationships(self, member: int) -> str:
        response = "You have registered the following partners:\n"

        for nbr, datadict in self.G.adj[member].items():
            response += f"{self.G.nodes[nbr]['display_name']} ({datadict['relationship']})\n"
        
        return response
    
    def remove_relationship(self, id, partnerId):
            if not self.G.has_node(id):
                raise NodeNotFound("User wasn't found")
            elif not self.G.has_node(partnerId):
                raise NodeNotFound("Partner wasn't found")
            
            self.G.remove_edge(id, partnerId)

            # If either weren't unique users, remove them from the graph if they got no other links
            if self.G.degree(id) == 0 and self.G.nodes[id]['unique_id'] is False:
                self.unregister(id)
            if self.G.degree(partnerId) == 0 and self.G.nodes[partnerId]['unique_id'] is False:
                self.unregister(partnerId)

    def register(self, userId: int, display_name: str, pronouns:str = "", type:str = ""):
        self._add_node(userId, display_name, pronouns, type, claimed=True, force_update=True)

    def unregister(self, userId):
        if not self.G.has_node(userId):
            raise NodeNotFound("User wasn't found")
        
        self.G.remove_node(userId)

    def save(self):
        nx.write_gml(self.G, f"{self.id}.gml")

    def render_graph_to_file(self):
        nx.write_gml(self.G, f"{self.id}.gml")
        graph = gv.d3(data=self.G, graph_height=880, use_collision_force=True, zoom_factor=1.5, 
                    show_details=True, use_many_body_force=False, use_links_force=True,
                    links_force_strength=1, collision_force_strength=1, node_label_data_source="display_name")
        graph.export_html(f"{self.id}.html", overwrite=True)

    def render_graph_to_html(self):
        graph = gv.d3(data=self.G, graph_height=880, use_collision_force=True, zoom_factor=1.5, 
            show_details=True, use_many_body_force=False, use_links_force=True,
            links_force_strength=1, collision_force_strength=1, node_label_data_source="display_name")
        
        return graph.to_html_standalone()

class Polycules:
    def __init__(self):
        self.store: dict = {}

    def get(self, polyculeId: int) -> Polycule:
        polycule = self.store.get(polyculeId)
        if polycule is None:
            polycule = Polycule(polyculeId)
            self.store[polyculeId] = polycule
        
        return polycule