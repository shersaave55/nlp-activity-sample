"""
VISUAL EXPLANATION: What is Code Assignment?
==============================================

Code Assignment = The "translation table" that says which ASCII/Latin 
                 string should represent each original character.

Think of it like creating a SECRET CODE or CIPHER for your language!
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║           WHAT IS "CODE ASSIGNMENT"? - Simple Analogy            ║
╚══════════════════════════════════════════════════════════════════╝

Imagine you're creating a SECRET CODE for Tibetan letters:

TIBETAN ORIGINAL    →    YOUR SECRET CODE
─────────────────────────────────────────────────────────
    བ (BA)          →         ???
    ོ (vowel O)      →         ???  
    ད (DA)          →         ???
    ་ (tsheg)        →         ???


You need to decide: What ASCII/Latin symbols will represent each?

╔══════════════════════════════════════════════════════════════════╗
║                    OPTION 1: BASIC ASSIGNMENT                    ║
╚══════════════════════════════════════════════════════════════════╝

Pattern: B, C, D, E, F, ... then Aa, Ab, Ac, Ad, ...
         (systematic, predictable, easy to generate)

TIBETAN CHAR    FREQUENCY    →    BASIC CODE ASSIGNED
───────────────────────────────────────────────────────
   Space        3,738,461    →         B
   ་ (tsheg)    3,158,047    →         C        ← 2nd most frequent
   ى            1,957,239    →         D        ← 3rd most frequent
   ས            941,743      →         I        ← 8th most frequent
   བ            500,618      →         Af       ← 27th most frequent
   ོ            643,702      →         V        ← 19th most frequent
   ད            670,354      →         S        ← 17th most frequent

So: བོད་ → "AfVSC"
         ↑  ↑ ↑ ↑
         │  │ │ └─ ་ becomes C
         │  │ └─── ད becomes S  
         │  └───── ོ becomes V
         └──────── བ becomes Af


╔══════════════════════════════════════════════════════════════════╗
║                  OPTION 2: OPTIMIZED ASSIGNMENT                  ║
╚══════════════════════════════════════════════════════════════════╝

Pattern: Common English letters, symbols that are 1 token in LLaMA2
         (▁, e, t, a, i, o, n, s, r, ...) - based on English frequency!
         (carefully chosen, requires testing)

TIBETAN CHAR    FREQUENCY    →    OPTIMIZED CODE ASSIGNED
─────────────────────────────────────────────────────────────
   Space        3,738,461    →         ▁        ← special space token
   ་ (tsheg)    3,158,047    →         e        ← common English 'e'
   ى            1,957,239    →         t        ← common English 't'
   ས            941,743      →         s        ← common English 's'
   བ            500,618      →         )        ← single char symbol
   ོ            643,702      →         .        ← period symbol
   ད            670,354      →         g        ← common English 'g'

So: བོད་ → ").ge"
         ↑  ↑ ↑ ↑
         │  │ │ └─ ་ becomes e
         │  │ └─── ད becomes g  
         │  └───── ོ becomes .
         └──────── བ becomes )


╔══════════════════════════════════════════════════════════════════╗
║                      THE KEY DIFFERENCE                          ║
╚══════════════════════════════════════════════════════════════════╝

SAME INPUT:  བོད་

DIFFERENT "CODE ASSIGNMENT" (different translation tables):
   Basic:     AfVSC        (uses pattern B, C, D, Aa, Ab, ...)
   Optimized: ).ge         (uses e, t, a, i, ..., symbols)

BOTH ARE CORRECT! Both are 100% reversible!
   Basic:     "AfVSC"  → translates back → བོད་ ✓
   Optimized: ").ge"   → translates back → བོད་ ✓


╔══════════════════════════════════════════════════════════════════╗
║                  WHY TWO DIFFERENT ASSIGNMENTS?                  ║
╚══════════════════════════════════════════════════════════════════╝

BASIC Assignment Goal:
   → Simple, automatic, human-readable
   → Pattern: B, C, D, ..., Aa, Ab, Ac, ...
   → Problem: "Af" is 2 characters, tokenizes as 2 tokens

OPTIMIZED Assignment Goal:
   → Each code is exactly 1 token in LLaMA2 tokenizer
   → Reuses common English letters: e, t, a, i, n, s, r, ...
   → Benefit: "e" is 1 character, tokenizes as 1 token


╔══════════════════════════════════════════════════════════════════╗
║              FOR YOUR NEW LANGUAGE - WHAT YOU NEED               ║
╚══════════════════════════════════════════════════════════════════╝

STEP 1: Count character frequencies in your corpus
   → Sort by frequency (most frequent first)

STEP 2: Decide your "code assignment" strategy:

   A) BASIC (Easy):
      Most frequent char → "B"
      2nd frequent char  → "C"  
      3rd frequent char  → "D"
      ...
      26th char          → "Aa"
      27th char          → "Ab"
      (automatic pattern, runs via char_analyzer.py)

   B) OPTIMIZED (Manual):
      Most frequent char → "▁" or "e" (test if 1 token)
      2nd frequent char  → "t" (test if 1 token)
      3rd frequent char  → "a" (test if 1 token)
      (manually choose, test each in tokenizer)

STEP 3: Create JSON mapping with your chosen codes

STEP 4: Use the transliterator!


╔══════════════════════════════════════════════════════════════════╗
║                          FINAL ANALOGY                           ║
╚══════════════════════════════════════════════════════════════════╝

Think of "code assignment" like choosing HOW TO SPELL OUT numbers:

   Same number: 123

   Assignment Option 1: "one hundred twenty-three"  (verbose)
   Assignment Option 2: "123"                        (compact)
   
   Both represent the same thing!
   Both can convert back!
   Just different ways to write it!

HuffmanTranslit does the same for non-Latin scripts:
   Basic:     "AfVSC"     (systematic codes)
   Optimized: ").ge"      (tokenizer-friendly codes)
   
   Same meaning, different encoding!

╚══════════════════════════════════════════════════════════════════╝
""")
