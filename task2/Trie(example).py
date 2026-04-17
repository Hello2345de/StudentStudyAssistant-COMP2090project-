class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.word_list = {}

    def insert(self, word):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if word not in self.word_list:
            self.word_list[word] = 0
                
    def delete(self, word):
        word = word.lower()
        if word in self.word_list:
            del self.word_list[word]
            self._delete(self.root, word, 0)
        else:
            return
        
    def _delete(self, node, word, index):
        if index == len(word):
            if not node.is_end_of_word:
                return False
            node.is_end_of_word = False
            return len(node.children) == 0
        char = word[index]
        if char not in node.children:
            if len(word) > 1:
                    return self.spell_check(word)
            else:
                return False
        child = node.children[char]
        should_delete_child = self._delete(child, word, index+1)
        if should_delete_child:
            del node.children[char]
        return (not node.is_end_of_word) and (len(node.children) == 0 )

    def search(self, word):
        word = word.lower()
        node = self.root
        for char in word:
            if char not in node.children:
                if len(word) > 1:
                    return self.spell_check(word)
                else:
                    return False
            node = node.children[char]
        if node.is_end_of_word:
            self.word_list[word] += 1
            print(True)
        return node.is_end_of_word

    def starts_with(self, prefix):
        prefix = prefix.lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def _get_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect(self, node, prefix, result):
        if node.is_end_of_word:
            result.append(prefix)
        for ch, child in node.children.items():
            self._collect(child, prefix + ch, result)
            
    def words_with_prefix(self, prefix):
        prefix = prefix.lower()
        node = self._get_node(prefix)
        if node is None:
            return
        result = []
        self._collect(node, prefix, result)
        return result 
    
    def word_library(self):
        print(self.word_list)
        return self.word_list
    
    def autocomplete(self, prefix):
        prefix = prefix.lower()
        word_choice = self.words_with_prefix(prefix)   
        if not word_choice:
            print(None)
            return None        
        best_word = self._suggested_wording(word_choice)
        print("Suggested words: ")
        for i,j in enumerate(best_word, 1):
            print(f"{i}. {j}")

    def spell_check(self, word):
        word = word.lower()
        matches = []
        for w in self.word_list:
            if w == word:
                print("The word", word,"is in the wordlist already")
                return
            if abs(len(w) - len(word)) == 1:
                if self._difference_in_word_length(word, w):
                    if w not in matches:
                        matches.append(w)
            if abs(len(w) - len(word)) == 0:
                if self._difference_in_character(word, w):
                    if w not in matches:
                        matches.append(w)
                if self._difference_in_order(word, w):
                    if w not in matches:
                        matches.append(w)
        if not matches:
            print("None")
            return None
        best_word = self._suggested_wording(matches)
        print("Do you want to search : ")
        for i,j in enumerate(best_word, 1):
            print(f"{i}. {j}")

    def _difference_in_word_length(self, search_word, w):
        if len(search_word) > len(w):
            search_word, w = w, search_word
        i = j = 0
        mismatch = 0
        while i < len(search_word) and j < len(w):
            if search_word[i] == w[j]:
                i, j = i+1, j+1
            else:
                mismatch = mismatch + 1
                if mismatch > 1:
                    return False
                j= j + 1
        return True
        
    def _difference_in_character(self, search_word, w):
        i = j = 0
        mismatch = 0
        while i < len(search_word) and j < len(w):
            if search_word[i] != w[j]:
                mismatch = mismatch + 1
                if mismatch > 1:
                    return False
            i, j = i+1, j+1
        return True
    
    def _difference_in_order(self, search_word, w):
        i = j = 0
        mismatch = 0
        while i < len(search_word) and j < len(w):
            if search_word[i] != w[j]:
                if i + 1 >= len(search_word) or j + 1 >= len(w):
                    return False              
                elif search_word[i+1] != w[j] or search_word[i] != w[j+1]:
                    return False
                mismatch = mismatch + 1
                if mismatch > 1:
                    return False
                i += 2
                j += 2
            else:
                i += 1
                j += 1
        return True
                    
    def _suggested_wording(self, wordlist, max_freq = 0, best_word = []):
        for word in wordlist:
            if self.word_list[word] >= max_freq:
                max_freq = self.word_list[word]
        if not best_word:
            best_word = [word for word in wordlist if self.word_list[word] == max_freq]
        else:
            best_word += [word for word in wordlist if self.word_list[word] == max_freq]
        best_word = best_word[:5]
        new_word = [word for word in wordlist if word not in best_word]
        if len(best_word) < 5 and new_word and max_freq >=0:
            return self._suggested_wording(new_word, max_freq - 1, best_word)
        return best_word
        

#Code Explanation:
        
#TrieNode uses a dictionary for children (flexible for any alphabet).
#is_end_of_word flag indicates a complete word.
#self.freq indicates the frequency of word searched (used for autocomplete and spell check)
#insert traverses and builds path.
#search verifies full path + end flag.
#starts_with checks path only (useful for autocomplete).
#delete remove the nodes that are end characters
#word_with_prefix gives the words follow a specific prefix
#autocomplete suggests words based on prefix and frequency.
#spell_check checks for words with 1 character difference, 1 character order difference, and 1 word length difference.


sample= Trie()
sample.insert("Can")
sample.insert("Car")
sample.insert("Cat")
sample.insert("Candy")
sample.insert("Cat")
sample.insert("cART")
sample.insert("Sat")
sample.insert("cUT")
sample.insert("sand")

sample.delete("cART")

sample.search("Cat")
sample.search("cat")
sample.search("sand")
sample.search("cone")

print("\nReturn true:\n")
print(sample.starts_with("ca"))
print("\nReturn false:\n")
print(sample.starts_with("cam"))

print("\nReturn a word list:\n")
print(sample.words_with_prefix("ca"))
print("\nReturn none:\n")
print(sample.words_with_prefix("cam"))

print("\nReturn a word list:\n")
sample.autocomplete("ca")
print("\nReturn none:\n")
sample.autocomplete("ba")

# Case with 1 word length difference
print("\nWord with 1 word length difference:\n")
sample.spell_check("acandy")
print("\nWord with 1 word length difference:\n")
sample.spell_check("canndy")
print("\nWord with 1 word length difference:\n")
sample.spell_check("candyy")

# Case with 1 character difference
print("\nWord with 1 character difference:\n")
sample.spell_check("mandy")

# Case with 1 character order difference
print("\nWord with 1 character order difference:\n")
sample.spell_check("cadny")

# Failure case
print("\nFailure case:\n")
sample.spell_check("raw")
sample.spell_check("caaaan")
sample.spell_check("ydnac")

# Normal case
print("\nNormal case:\n")
sample.spell_check("cat")

# Function in search(word)
print("\nFunction in search(word):\n")
sample.search("sad")
print("\nFunction in search(word):\n")
sample.search("grow")

print("\n")
print(sample.word_list)
