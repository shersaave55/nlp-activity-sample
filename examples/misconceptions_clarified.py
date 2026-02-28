"""
CLARIFYING MISCONCEPTIONS ABOUT CODE ASSIGNMENT
================================================

Let's address each point and clarify the system!
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║              YOUR UNDERSTANDING - WHAT'S CORRECT? ✓              ║
╚══════════════════════════════════════════════════════════════════╝

✓ CORRECT: "It's like storing each character in its own independent box"
   → YES! Each unique character gets exactly ONE code assignment
   → It IS like a dictionary/hashmap: character → code
   
✓ CORRECT: "We assign it a value so we can reverse the translation"
   → YES! This is a BIJECTIVE mapping (one-to-one correspondence)
   → Each character → unique code
   → Each code → unique character
   → Perfect reversibility!

✓ CORRECT: "Similar to the process of hash maps"
   → YES! It's exactly like a dictionary/lookup table
   → Python dict: {'བ': 'Af', 'ོ': 'V', 'ད': 'S'}


╔══════════════════════════════════════════════════════════════════╗
║           YOUR UNDERSTANDING - MISCONCEPTIONS ✗                  ║
╚══════════════════════════════════════════════════════════════════╝

✗ MISCONCEPTION #1: "Basic = first letter capital, rest lowercase"
   
   What you said: 
   "The first letter is capital and if the word is longer then 
    first is capital, everything after is lowercase"
   
   REALITY:
   → Basic codes are NOT based on word structure!
   → Codes are ASSIGNED TO INDIVIDUAL CHARACTERS, not words
   → Pattern: B, C, D, E, ... Z (singles), then Aa, Ab, Ac, ... Az,
              Ba, Bb, ..., Ca, Cb, ... (doubles)
   
   Example misconception vs reality:
   
   ❌ WRONG: "First char of word gets capital B, rest get lowercase"
   ✓ RIGHT:  "The 1st most frequent CHARACTER gets code 'B'
              The 2nd most frequent CHARACTER gets code 'C'
              The 26th CHARACTER gets code 'Aa'
              The 27th CHARACTER gets code 'Ab'"
   
   It's NOT about word position - it's about FREQUENCY RANK!


✗ MISCONCEPTION #2: "Optimized uses most common English words"
   
   What you said:
   "Optimized uses the most common English words"
   
   REALITY:
   → NOT words! Individual LETTERS/CHARACTERS!
   → Uses common English LETTERS: e, t, a, i, n, s, r, o, l, ...
   → Also uses symbols: ▁, ), ., (, *, etc.
   
   Example:
   ❌ WRONG: Assign "the", "and", "is" to frequent characters
   ✓ RIGHT:  Assign "e", "t", "a", "i" to frequent characters
   
   Why? Because 'e' is ONE TOKEN in LLaMA2 tokenizer
           But 'the' is ALSO one token... but we need 100+ codes!
           
   So we use: single letters + symbols + special chars


╔══════════════════════════════════════════════════════════════════╗
║                  THE ACTUAL SYSTEM - DETAILED                    ║
╚══════════════════════════════════════════════════════════════════╝

STEP 1: Count all character frequencies across 3 languages
───────────────────────────────────────────────────────────

Original corpus characters:
   Space:         3,738,461 occurrences  → RANK 1
   ་ (tsheg):     3,158,047 occurrences  → RANK 2
   ى (Arabic):    1,957,239 occurrences  → RANK 3
   ᠠ (Mongolian): 1,363,662 occurrences  → RANK 4
   ...
   བ (Tibetan):     500,618 occurrences  → RANK 27
   ...

(162 unique characters total across Tibetan, Mongolian, Uyghur)


STEP 2a: BASIC Assignment - Use alphabetical pattern
─────────────────────────────────────────────────────

Code generation pattern (automatic):
   Position 1-24:   B, C, D, E, F, G, H, I, J, K, L, M, N, P, Q, R, 
                    S, T, V, W, X (skip A, O, U - reserve for special)
   Position 25+:    Aa, Ab, Ac, Ad, Ae, ... Az,
                    Ba, Bb, Bc, ... Bz,
                    Ca, Cb, ... etc.

Assignment by RANK (not by word position!):
   RANK 1  (Space)        → Code: B
   RANK 2  (་)            → Code: C
   RANK 3  (ى)            → Code: D
   RANK 4  (ᠠ)            → Code: E
   ...
   RANK 27 (བ)            → Code: Af
   RANK 28 (ར)            → Code: Ag

Now when you see this CHARACTER བ anywhere:
   བ → Af (always, regardless of position in word!)


STEP 2b: OPTIMIZED Assignment - Use single-token codes
───────────────────────────────────────────────────────

Code pool (manually tested in tokenizer):
   Single letters: e, t, a, i, n, s, r, o, l, d, c, u, p, m, h, g, ...
   Symbols:        ▁, ), (, ., *, +, -, /, =, ;, :, ', ", ...
   Special:        ű, ö, é, и, etc. (Unicode chars that are 1 token)

Assignment by RANK (same ranks as basic!):
   RANK 1  (Space)        → Code: ▁  (special space token)
   RANK 2  (་)            → Code: e  (most common English letter)
   RANK 3  (ى)            → Code: t  (2nd most common)
   RANK 4  (ᠠ)            → Code: a
   ...
   RANK 27 (བ)            → Code: )  (symbol)
   RANK 28 (ར)            → Code: g

Same principle: བ → ) (always, regardless of word position!)


╔══════════════════════════════════════════════════════════════════╗
║                    HASHMAP ANALOGY - REFINED                     ║
╚══════════════════════════════════════════════════════════════════╝

YES, it IS like a hashmap, but more specifically:

Python Implementation:

# Basic mapping (character → code)
char_to_basic = {
    ' ':  'B',    # Space → B
    '་': 'C',    # Tsheg → C  
    'ས': 'I',    # SA → I
    'བ': 'Af',   # BA → Af
    'ོ': 'V',    # vowel O → V
    'ད': 'S',    # DA → S
}

# Optimized mapping (character → code)
char_to_optimized = {
    ' ':  '▁',   # Space → ▁
    '་': 'e',    # Tsheg → e
    'ས': 's',    # SA → s
    'བ': ')',    # BA → )
    'ོ': '.',    # vowel O → .
    'ད': 'g',    # DA → g
}

# Reverse mappings (for restoration)
basic_to_char = {v: k for k, v in char_to_basic.items()}
optimized_to_char = {v: k for k, v in char_to_optimized.items()}


Transliteration process:

text = "བོད་"

# Basic transliteration
result = ""
for char in text:
    result += char_to_basic[char]  # Lookup in hashmap!
print(result)  # "AfVSC"

# Reverse translation
original = ""
for code in parse_codes("AfVSC"):  # Need smart parsing for multi-char codes
    original += basic_to_char[code]
print(original)  # "བོད་"


╔══════════════════════════════════════════════════════════════════╗
║              KEY INSIGHT: CHARACTER-LEVEL, NOT WORD-LEVEL        ║
╚══════════════════════════════════════════════════════════════════╝

This system works at CHARACTER LEVEL, not WORD LEVEL!

Example word: བོད་ (3 characters + 1 punctuation)

Character-by-character mapping:
   
   Position in word    Character    Frequency Rank    Basic Code
   ────────────────────────────────────────────────────────────
   1st in word         བ            27                Af
   2nd in word         ོ            19                V
   3rd in word         ད            17                S
   4th in word         ་            2                 C

Notice: Codes are based on FREQUENCY RANK, not position in word!
   - ད gets 'S' because it's 17th most frequent (not 3rd position)
   - ་ gets 'C' because it's 2nd most frequent (not 4th position)


╔══════════════════════════════════════════════════════════════════╗
║                          CORRECTED SUMMARY                       ║
╚══════════════════════════════════════════════════════════════════╝

✓ YES: It's like a hashmap/dictionary (character → code)
✓ YES: Each character gets its own independent code
✓ YES: Bijective mapping allows perfect reversal
✓ YES: Frequency-based assignment (Huffman principle)

✗ NO:  NOT based on word structure or position in word
✗ NO:  NOT using "English words" - using English LETTERS/symbols
✗ NO:  Capital/lowercase is NOT about word position
       It's just part of the code pattern (Aa, Ab, Ac, ...)

CORRECT UNDERSTANDING:
   1. Count frequency of each unique character across corpus
   2. Sort characters by frequency (most → least)
   3. Assign codes in order: frequent chars get short/simple codes
   4. Create bidirectional lookup table (hashmap)
   5. Transliterate: for each input char, look up its code
   6. Reverse: for each code, look up its original character

""")
