from random import Random

class SkipListNode:
    def __init__(self, value: int, levels: int): 
        self.value = value
        self.forward = [None] * levels

class SkipListSet:
    def __init__(
        self,
        max_level: int = 32,
        promotion_probability: float = 0.5,
        rng: Random | None = None,
    ) -> None:
        """Create an empty randomized skip-list ordered set."""
        if max_level < 1 or (promotion_probability < 0.1 or promotion_probability > 0.9):
            raise ValueError
        self.head = SkipListNode(None, max_level)
        self.level = 0
        self.max_level = max_level
        self.promotion_probability = promotion_probability
        self.rng = rng or Random()
        self.node_count = 0

    def insert(self, key: int) -> bool:
        """Insert key; return True if it was new, otherwise False."""
        if self.contains(key):
            return False

        # Determine how many levels to promote this value based on rng
        top_node_level = 0
        while self.rng.random() < self.promotion_probability:
            if top_node_level >= self.max_level - 1:
                break
            top_node_level += 1

        # Update current highest level so height stays accurate
        if top_node_level > self.level: 
            self.level = top_node_level

        new_node = SkipListNode(key, top_node_level + 1)
        # search to find spot it should be placed in each level and update the pointers
        predecessor_nodes = self._predecessor_search_helper(key, top_node_level)
        for current_level in range(top_node_level, -1, -1):
            previous_node = predecessor_nodes[current_level]
            previous_forward = previous_node.forward[current_level]
            previous_node.forward[current_level] = new_node
            new_node.forward[current_level] = previous_forward

        self.node_count += 1
        return True

        
    def contains(self, key: int) -> bool:
        """Return whether key is in the set."""
        if self.head.forward[0] == None:
            return False
        current_node = self.head
        current_level = self.level

        while current_level >= 0:
            next_node = current_node.forward[current_level]
            if next_node is None:
                current_level -= 1
                continue
            if next_node.value == key:
                return True
            if next_node.value > key:
                current_level -= 1
            else:
                current_node = next_node
        return False
    
    def delete(self, key: int) -> bool:
        """Delete key; return True if it existed, otherwise False."""
        if not self.contains(key):
            return False
        if self.head.forward[0] is None:
            return False
        predecessor_nodes = self._predecessor_search_helper(key, self.level)
        next_node = predecessor_nodes[0].forward[0]
        if next_node is None or next_node.value != key:
            return False

        for current_level in range(self.level, -1, -1):
            previous_node = predecessor_nodes[current_level]
            next_node = previous_node.forward[current_level]
            if next_node is not None and next_node.value == key:
                previous_node.forward[current_level] = next_node.forward[current_level]

        # Decrease active levels if top level gets removed with this deletion
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        self.node_count -= 1
        return True
    
    def _predecessor_search_helper(self, key: int, level: int) -> list[SkipListNode]:
        """Return recorded predecessor nodes for indicated levels for a given key."""
        predecessor_nodes = [self.head] * (level + 1)
        current_node = self.head
        for current_level in range(level, -1, -1):
            next_node = current_node.forward[current_level]
            while next_node is not None and next_node.value < key:
                current_node = next_node
                next_node = current_node.forward[current_level]
            predecessor_nodes[current_level] = current_node
        return predecessor_nodes
    
    def predecessor(self, key: int) -> int | None:
        """Return the greatest stored key strictly less than key."""
        predecessor_list = self._predecessor_search_helper(key, self.level)
        return predecessor_list[0].value if predecessor_list[0] is not self.head else None
    
    def successor(self, key: int) -> int | None:
        """Return the smallest stored key strictly greater than key."""
        predecessor_list = self._predecessor_search_helper(key, self.level)
        next_node = predecessor_list[0].forward[0]
        if next_node is not None and next_node.value == key:
            next_node = next_node.forward[0]
        return None if next_node is None else next_node.value
    
    def to_list(self) -> list[int]:
        """Return all stored keys in increasing order."""
        key_list = []
        current_node = self.head.forward[0]
        while current_node is not None:
            key_list.append(current_node.value)
            current_node = current_node.forward[0]
        return key_list

    def __len__(self) -> int:
        """Return the number of stored keys."""
        return self.node_count
    
    @property
    def height(self) -> int:
        """Return the number of active levels, including level 0."""
        return self.level + 1


timmy = SkipListSet(10, .5)
print(SkipListSet.insert(timmy, 17))