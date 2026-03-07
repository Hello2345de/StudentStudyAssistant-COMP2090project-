# Task 2 – Self-Study on a New Data Structure and a New Algorithm

**Course**: COMP2090SEF  
**Project**: Data Structures, Algorithms and Problem Solving  
**Semester**: 2026 Spring  

## Selected Data Structure: Trie (Prefix Tree)

### Abstract Data Type (ADT)
A Trie is a tree-based data structure used to store a dynamic set of strings efficiently. Each node represents a single character, and paths from root to a marked node represent valid words.

**Main operations**:
- insert(word)  
- search(word) → check exact match  
- startsWith(prefix) → check if any word begins with given prefix  
- (optional) delete(word), collect all words with prefix

**Key properties**:
- Abstraction: Users interact only with high-level string operations; internal node structure and traversal are hidden.
- Encapsulation: Node children are usually private (dictionary or array).
- Modularity: Trie can be reused for different string-related tasks without changing core logic.

### Real-life applications
- Autocomplete in search engines and mobile keyboards
- Spell checking and correction systems
- Predictive text input in IDEs and messaging apps
- Longest prefix matching in IP routing tables
- Dictionary / word suggestion in text editors

### Time Complexity
- Insert, search, prefix search: O(m) where m is the length of the word  
  (very fast in practice due to constant-time child lookup per character)

## Selected Algorithm: Tim Sort

Tim Sort is a hybrid stable sorting algorithm that combines **insertion sort** (on small runs) with **merge sort** (on larger runs). It is the default sorting algorithm in Python (`list.sort()` and `sorted()`), Java, Android, and many other standard libraries.

### High-level steps
1. **Identify natural runs** — scan the array to find already sorted segments ("runs") of length at least min_run (typically calculated dynamically, often around 32–64).
2. **Sort small runs with insertion sort** — insertion sort is very efficient on small or nearly sorted data.
3. **Merge runs using merge sort** — progressively merge adjacent runs using a modified merge that exploits existing order (galloping mode in real implementations).
4. **Adaptive merging** — use techniques like galloping to skip unnecessary comparisons when one run is much larger.

### Time & Space Complexity
- Best case: O(n) — when array is already sorted or has long runs  
- Average case: O(n log n)  
- Worst case: O(n log n)  
- Space: O(n) — needs temporary array for merging

### Real-life applications
- Default sorting in Python, Java, Swift, Android JDK, Chrome V8 engine
- Sorting large datasets with natural runs (logs, timestamps, partially pre-sorted data)
- Stable sorting where order of equal elements matters (e.g., database records)

## Code Examples & Explanation

### Trie – Basic Implementation (conceptual)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
