"""
VISUAL PROOF: Character-level, not Word-level
==============================================
This shows codes are based on CHARACTER FREQUENCY, not word position!
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.transliterator import create_transliterator

basic = create_transliterator('basic')
optimized = create_transliterator('optimized')

print("""
╔══════════════════════════════════════════════════════════════════╗
║          PROOF: CODES ARE CHARACTER-LEVEL, NOT WORD-LEVEL        ║
╚══════════════════════════════════════════════════════════════════╝

Let's track the character ས (Tibetan SA) in different positions:
""")

# Examples with ས in different positions
examples = [
    ("སངས་", "1st position in word"),
    ("བསྟན་", "2nd position in word"),
    ("གནས་", "3rd position in word"),
]

print("\nThe character ས appears in different word positions:\n")

for text, description in examples:
    basic_result = basic.transliterate_to_latin(text)
    opt_result = optimized.transliterate_to_latin(text)
    
    print(f"Original: {text:10} ({description})")
    print(f"   Basic:     {basic_result}")
    print(f"   Optimized: {opt_result}")
    
    # Show where ས maps to
    if 'ས' in text:
        pos = text.index('ས')
        basic_code = basic.char_to_latin.get('ས', '?')
        opt_code = optimized.char_to_latin.get('ས', '?')
        print(f"   ས always maps to: Basic='{basic_code}' | Optimized='{opt_code}'")
    print()

print("""
╔══════════════════════════════════════════════════════════════════╗
║                          KEY OBSERVATION                         ║
╚══════════════════════════════════════════════════════════════════╝

Notice: The character ས ALWAYS becomes the SAME code:
   - Basic:     ས → 'I'  (always, regardless of position!)
   - Optimized: ས → 's'  (always, regardless of position!)

This proves it's CHARACTER-LEVEL mapping, not word-level!


╔══════════════════════════════════════════════════════════════════╗
║                    WHY FREQUENCY MATTERS                         ║
╚══════════════════════════════════════════════════════════════════╝

Let's see WHY ས gets code 'I' in basic system:
""")

# Show top 10 characters and their codes
print("\nTop 10 most frequent characters in the corpus:\n")
print("Rank  Character  Frequency    Basic Code  Optimized Code")
print("─" * 65)

top_chars = [
    (1, ' ', 3738461, 'B', '▁'),
    (2, '་', 3158047, 'C', 'e'),
    (3, 'ى', 1957239, 'D', 't'),
    (4, 'ᠠ', 1363662, 'E', 'a'),
    (5, 'ᠢ', 1074071, 'F', 'i'),
    (6, 'ᠡ', 1015893, 'G', 'n'),
    (7, 'ا', 979501, 'H', 'o'),
    (8, 'ས', 941743, 'I', 's'),  # Here it is!
    (9, 'ᠭ', 847367, 'J', 'h'),
    (10, 'ᠨ', 846990, 'K', 'r'),
]

for rank, char, freq, basic_code, opt_code in top_chars:
    char_display = char if char != ' ' else '(space)'
    print(f"{rank:2}    {char_display:5}      {freq:>9,}    {basic_code:^10}  {opt_code:^15}")

print("""
ས is the 8th most frequent character → gets 8th code in the sequence!
   Basic sequence:   B, C, D, E, F, G, H, I, ...
                                          ↑
                                       8th code
   
   Optimized sequence: ▁, e, t, a, i, n, o, s, ...
                                             ↑
                                          8th code


╔══════════════════════════════════════════════════════════════════╗
║                   HASHMAP ANALOGY - CONCRETE                     ║
╚══════════════════════════════════════════════════════════════════╝

Think of it EXACTLY like this Python code:

# Step 1: Build the frequency-based mapping (like a hashmap)
char_to_code = {}
code_to_char = {}

# After analyzing corpus, we create the mapping:
frequency_sorted_chars = [
    (' ', 3738461),   # Rank 1
    ('་', 3158047),   # Rank 2
    ('ى', 1957239),   # Rank 3
    # ... more ...
    ('ས', 941743),    # Rank 8
    # ... etc ...
]

code_pattern = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', ...]

for i, (char, freq) in enumerate(frequency_sorted_chars):
    code = code_pattern[i]
    char_to_code[char] = code      # Forward map
    code_to_char[code] = char      # Reverse map

# Now the hashmap is built!
# char_to_code = {' ': 'B', '་': 'C', ..., 'ས': 'I', ...}


# Step 2: Use it for transliteration (lookup in hashmap!)
def transliterate(text):
    result = ""
    for char in text:
        result += char_to_code.get(char, f'@{char}@')
    return result

def restore(latin_text):
    # Parse codes and look up in reverse hashmap
    result = ""
    for code in parse_codes(latin_text):
        result += code_to_char[code]
    return result


# Examples:
transliterate("སངས་")  → "ICkAhC"
                          ↑ ↑  ↑  ↑
                          │ │  │  └─ ་ → C (Rank 2)
                          │ │  └──── ང → Ah (Rank 29)
                          │ └─────── ང → Ah (Rank 29) 
                          └───────── ས → I (Rank 8)

Same character ས → Always I (like hashmap lookup!)


╔══════════════════════════════════════════════════════════════════╗
║                     FINAL CORRECTED SUMMARY                      ║
╚══════════════════════════════════════════════════════════════════╝

✓ Hashmap/Dictionary analogy is PERFECT!
  → character → code (forward lookup)
  → code → character (reverse lookup)

✓ Each character has ONE fixed code based on its frequency rank
  → Not based on word position
  → Not based on context
  → Just: frequency rank → code assignment

✓ Basic codes pattern: B, C, D, ..., Aa, Ab, Ac, ...
  → The capital/lowercase is just the PATTERN for generating codes
  → Has nothing to do with word structure!
  → It's: 1st='B', 2nd='C', ..., 25th='Aa', 26th='Ab', etc.

✓ Optimized codes: Single-character tokens
  → Uses: e, t, a, i, n, s, ... (LETTERS not words!)
  → Plus symbols: ▁, ), ., etc.
  → Goal: each code = 1 token in LLaMA2

✗ NOT word-level encoding
✗ NOT using English words (using letters/symbols)
✗ Capital/lowercase NOT related to word position

It's pure character-level substitution cipher with frequency-based code assignment! 🎯
╚══════════════════════════════════════════════════════════════════╝
""")
