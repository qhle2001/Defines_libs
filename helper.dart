class TreeNode {
    int val;
    TreeNode? left;
    TreeNode? right;
    TreeNode([this.val = 0, this.left, this.right]);
  }

class CreateTreeNode{
  TreeNode? fromList(List<int?> values) {
    if (values.isEmpty || values[0] == null) return null;

    TreeNode root = TreeNode(values[0]!);
    List<TreeNode?> queue = [root];
    int i = 1;
    while (i < values.length){
      TreeNode? current = queue.removeAt(0);

      if (current != null) {
        // Left Child
        if (i < values.length && values[i] != null){
          current.left = TreeNode(values[i]!);
          queue.add(current.left);
        }
        i++;
        // Right Child
        if (i < values.length && values[i] != null){
          current.right = TreeNode(values[i]!);
          queue.add(current.right);
        }
        i++;
      }
    }
    return root;
  }
}
class Queue<T> {
  List<T> _queue = [];

  void add(T value) {
    _queue.add(value);
  }

  void addFirst(T value) {
    _queue.insert(0, value);
  }

  void addAll(List<T> values) {
    _queue.addAll(values);
  }

  T removeFirst() {
    if (_queue.isEmpty) {
      throw StateError("Queue is empty");
    }
    return _queue.removeAt(0);
  }

  T removeLast() {
    if (_queue.isEmpty) {
      throw StateError("Queue is empty");
    }
    return _queue.removeLast();
  }

  T first() {
    if (_queue.isEmpty) {
      throw StateError("Queue is empty");
    }
    return _queue[0];
  }

  T last() {
    if (_queue.isEmpty) {
      throw StateError("Queue is empty");
    }
    return _queue[_queue.length - 1];
  }

  bool get isEmpty => _queue.isEmpty;

  bool get isNotEmpty => _queue.isNotEmpty;

  int get length => _queue.length;

  List<T> toList() => List.from(_queue);

  @override
  String toString() => _queue.toString();
}