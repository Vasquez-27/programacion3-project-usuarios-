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
        if self.root is None:
            return []
        result = []
        self.traverse_tree(self.root, result)
        return result

    def traverse_tree(self, node: NodeN, result: List[Person]) -> None:
        result.append(node.person)
        for child in node.children:
            self.traverse_tree(child, result)