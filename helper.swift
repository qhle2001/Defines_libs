struct Queue<T> {
  private var elements: [T] = []

  mutating func add(_ value: T) {
    elements.append(value)
  }

  mutating func addFirst(_ value: T){
    elements.insert(value, at: 0)
  }

  mutating func addAll(_ value: [T]){
    elements.append(contentsOf: value)
  }
  
  mutating func removeFirst() -> T? {
    return elements.isEmpty ? nil : elements.removeFirst()
  }

  mutating func removeLast() -> T? {
    return elements.isEmpty ? nil : elements.removeLast()
  }

  var first: T? { return elements.isEmpty ? nil : elements.first }
  var last: T? { return elements.isEmpty ? nil : elements.last }
  var isEmpty: Bool { return elements.isEmpty }
  var isNotEmpty: Bool { return !elements.isEmpty }
  var count: Int { return elements.count }
  var toList: [T] { return Array(elements) }
}