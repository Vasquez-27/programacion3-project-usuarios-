from typing import Optional, List
from pydantic import BaseModel
from .person import Person

class NodeN(BaseModel):
    person: Person
    parent: Optional["NodeN"] = None

    def find_person_by_id(self, id: str) -> Optional["NodeN"]:
        if self.person.id == id:
            return self
        if self.parent:
            return self.parent.find_person_by_id(id)
        return None

    def update_person_by_id(self, id: str, updated_person: Person) -> bool:
        node = self.find_person_by_id(id)
        if node:
            node.person = updated_person
            return True
        return False

    def get_ancestry(self) -> List[Person]:
        lineage = []
        node = self
        while node:
            lineage.append(node.person)
            node = node.parent
        return lineage[::-1]  # Desde el ancestro hasta el actual

class TreeN(BaseModel):
    nodes: List[NodeN] = []

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        parent_node = None
        if parent_id:
            parent_node = self.find_node_by_id(parent_id)
            if not parent_node:
                return False
        new_node = NodeN(person=person, parent=parent_node)
        self.nodes.append(new_node)
        return True

    def find_node_by_id(self, id: str) -> Optional[NodeN]:
        for node in self.nodes:
            if node.person.id == id:
                return node
        return None

    def get_persons(self) -> List[Person]:
        return [node.person for node in self.nodes]

    def get_person_by_id(self, id: str) -> Optional[Person]:
        node = self.find_node_by_id(id)
        return node.person if node else None

    def update_person(self, id: str, updated_person: Person) -> bool:
        node = self.find_node_by_id(id)
        if node:
            node.person = updated_person
            return True
        return False

    def delete_person(self, id: str) -> bool:
        node = self.find_node_by_id(id)
        if not node:
            return False
        self.nodes.remove(node)
        return True