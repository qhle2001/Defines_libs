from typing import Optional, List
from collections import deque, defaultdict
import heapq

class TreeNode:
    def __init__(self, val: int, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val   = val
        self.left  = left
        self.right = right

class TreeValue:
    def __init__(self):
        pass

    def build_tree(self, values: List[Optional[int]]) -> Optional[TreeNode]:
        if not values:
            return None

        root = TreeNode(values[0])
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            current = queue.popleft()
            if i < len(values) and values[i] is not None:
                current.left = TreeNode(values[i])
                queue.append(current.left)
            i += 1

            if i < len(values) and values[i] is not None:
                current.right = TreeNode(values[i])
                queue.append(current.right)
            i += 1

        return root

    def find_node(self, root: TreeNode, val: int) -> Optional[TreeNode]:
        if not root or not val:
            return None

        if root.val == val:
            return root

        left = self.find_node(root.left, val)
        if left:
            return left
        return self.find_node(root.right, val)

    def print_tree(self, root: TreeNode) -> None:
        if not root:
            return
        queue = deque([root])
        while queue:
            length_root = len(queue)
            for _ in range(length_root):
                node = queue.popleft()
                print(node.val, end=' -> ')
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        print(f'None')

class MinHeap:
    def __init__(self):
        pass

    def push(self, heap:list, val: int):
        heap.append(val)
        self._heapify_up(heap, len(heap) - 1)

    def pop(self, heap:list) -> int:
        if not heap:
            raise IndexError("pop from empty heap")

        if len(heap) == 1:
            return heap.pop()

        root    = heap[0]
        heap[0] = heap.pop()
        self._heapify_down(heap, 0)
        return root

    def _heapify_up(self, heap:list, index:int):
        parent = (index - 1) // 2
        while index > 0 and heap[index] < heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            index  = parent
            parent = (index - 1)  // 2

    def _heapify_down(self, heap:list, index:int):
        n = len(heap)
        while True:
            left     = 2 * index + 1
            right    = 2 * index + 2
            smallest = index

            if left < n and heap[left] < heap[smallest]:
                smallest = left

            if right < n and heap[right] < heap[smallest]:
                smallest = right

            if smallest == index:
                break

            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest