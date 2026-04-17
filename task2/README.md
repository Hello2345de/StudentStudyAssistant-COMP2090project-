# Task 2 – Self-Study on a New Data Structure and a New Algorithm
                          
**Course**: COMP2090SEF  
**Topic**: Data Structures, Algorithms and Problem Solving  

## Selected Data Structure: Trie (Prefix Tree)

### Abstract Data Type (ADT)
A Trie is a tree-based data structure used to store a dynamic set of strings efficiently. Each node represents a single character, and paths from root to a marked node represent valid words.

**Main operations**:
- insert(word) -> add word to wordlist
- search(word) → check exact match, if match not found, execute `spell_check(word)` to find any word similar to searched word
- starts_with(prefix) → check if any word begins with given prefix
- delete(word) -> remove the word from the wordlist
- words_with_prefix(prefix) -> find the words starting with a specific prefix
- word_library() -> check the wordlist
- autocomplete(prefix) -> give suggestions on word starting with a specific prefix, ordered base on the searching frequency
- spell_check(word) -> give suggestions on word that searched word is not appear but similar to the words in wordlist, ordered base on the searching frequency

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

# How To Use :
### Success cases:
- `insert("Horse")` 
- `self.wordlist` = `{"horse" : 0}`
- `self.root`
- root.children = `"{h" : <node_h>}`            ,`root.is_end_of_word` is `False`
-  node_h.children = `{"o" : <node_ho>}`         ,`node_h.is_end_of_word` is `False`
- ...
-  node_hors.children = `{"e" : <node_horse>}`   ,`node_hors.is_end_of_word` is `False`
-  node_horse.children = `{}`                    ,`node_horse.is_end_of_word` is `True`
- `search("Horse")`
-  return `True`, self_wordlist = `{"horse" : 1}`
- `delete("Horse")`
-  self.wordlist = `{}`
- `starts_with("ho")`
-  node_ho.children = `{"r" : <node_r>}`
- ...
-  node_horse.children = {}, `node_horse.is_end_of_word` = `True`
-  return `True`
- `words_with_prefix("ho")`
-  node_ho.children = `{"r" : <node_r>}`
- ...
-  node_horse.children = `{}`, `node_horse.is_end_of_word` = `True`
-  return "horse"
- `autocomplete("ho")`  -->  execute `words_with_prefix("ho")`
-  "horse" found
-  suggest word "horse"
- `spell_check("house")`
-  scan wordlist, found 1 character difference between "horse" and "house"
-  suggest word "horse"
### Fail cases:  (Assume there is the word "horse")
- `insert(123)`    *Number can't apply to `.lower()` function*
- `search("hot")`
-  Not Found
-  execute `spell_check("hot")`
-  Not Found, return `False`
- `delete("hope")`
-  Not Found
- `starts_with("ha")`
-  Not Found, return `False`
- `words_with_prefix("ha")`
-  Not found
- `autocomplete("ha")`  -->  execute `words_with_prefix("ha")`
-  Not Found
- `spell_check("hurt")`
-  scan wordlist, no similar word
- return `None`

## Selected Algorithm: Tim Sort

Tim Sort is a hybrid stable sorting algorithm that combines **insertion sort** (on small runs) with **merge sort** (on larger runs). It is the default sorting algorithm in Python (`list.sort()` and `sorted()`), Java, Android, and many other standard libraries.

### Basic Operation :
Use `tim_sort(array)` to sort a single array

### High-level steps
1. **Identify natural runs** — scan the array to find already sorted segments ("runs") of length at least `min_run` (typically calculated dynamically, often around 32–64).
2. **Reduce comparison** - Use the sorted segments to reduce binary search for sorting remaining items
3. **Use binary insertion sort for small or nearly sorted run** — binary insertion sort is more efficient than insertion sort (*O(n log n) vs O(n^2)*)  on small or nearly sorted data.
4. **Merge runs using merge sort** — progressively merge adjacent runs using a modified merge that exploits existing order (galloping mode in real implementations).
5. **Adaptive merging** — use galloping to skip unnecessary comparisons when one run is much larger.

### Time & Space Complexity
- Best case: O(n) — when array is already sorted or has long runs  
- Average case: O(n log n)  
- Worst case: O(n log n)  
- Space: O(n) — needs temporary array for merging

### Real-life applications
- Default sorting in Python, Java, Swift, Android JDK, Chrome V8 engine
- Sorting large datasets with natural runs (logs, timestamps, partially pre-sorted data)
- Stable sorting where order of equal elements matters (e.g., database records)

# How To Use :
- `import random`
- `number = list(range(1,1000))`
- `sample = random.sample(number, 200)`   1. *Generate a random list*
- `print(sample)`  2. *For user to see the number list*
- `print(sorted(sample))`   3. *See the sorted list sorted by python default function*
- `print(tim_sort(sample))`  4. *See the sorted list sorted by self-defined tim sort*
- `print(sorted(sample) == tim_sort(sample))`   5. *See if self-defined tim sort successfully sort the list*
