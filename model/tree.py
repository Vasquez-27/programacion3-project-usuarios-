from typing import List, Optional
from pydantic import BaseModel
from .person import Person

class NodeN(BaseModel):
    person: Person
    children: List["NodeN"] = []

    def add_child(self, child: "NodeN") -> None:
        self.children.append(child)

    def remove_child_by_id(self, id: str) -> bool:
        for i, child in enumerate(self.children):
            if child.person.id == id:
                self.children.pop(i)
                return True
        for child in self.children:
            if child.remove_child_by_id(id):
                return True
        return False

    def update_person_by_id(self, id: str, updated_person: Person) -> bool:
        if self.person.id == id:
            self.person = updated_person
            return True
        for child in self.children:
            if child.update_person_by_id(id, updated_person):
                return True
        return False

    def find_person_by_id(self, id: str) -> Optional[Person]:
        if self.person.id == id:
            return self.person
        for child in self.children:
            found = child.find_person_by_id(id)
            if found:
                return found
        return None

class TreeN(BaseModel):
    root: Optional[NodeN] = None

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        new_node = NodeN(person=person)
        if self.root is None:
            self.root = new_node
            return True
        if parent_id is None:
            self.root.add_child(new_node)
            return True
        return self.find_and_add_child(self.root, parent_id, new_node)

    def find_and_add_child(self, node: NodeN, parent_id: str, new_node: NodeN) -> bool:
        if node.person.id == parent_id:
            node.add_child(new_node)
            return True
        for child in node.children:
            if self.find_and_add_child(child, parent_id, new_node):
                return True
        return False

    def get_persons(self) -> List[Person]:
        result = []
        if self.root:
            self.traverse_tree(self.root, result)
        return result

    def traverse_tree(self, node: NodeN, result: List[Person]) -> None:
        result.append(node.person)
        for child in node.children:
            self.traverse_tree(child, result)

    def get_person_by_id(self, person_id: str) -> Optional[Person]:
        if not self.root:
            return None
        return self.root.find_person_by_id(person_id)

    def update_person(self, id: str, updated_person: Person) -> bool:
        if not self.root:
            return False
        return self.root.update_person_by_id(id, updated_person)

    def delete_person(self, id: str) -> bool:
        if not self.root:
            return False
        if self.root.person.id == id:
            self.root = None
            return True
        return self.root.remove_child_by_id(id)