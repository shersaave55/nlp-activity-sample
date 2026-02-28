import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.char_analyzer import CharacterAnalyzer

# Step 1: Analyze character frequencies in your corpus
analyzer = CharacterAnalyzer()
analyzer.analyze_file('data/samples/chinese.txt')

# Step 2: Generate optimized character mappings
mappings = analyzer.create_basic_mapping(num_chars=200)
analyzer.save_mapping_json(mappings, 'chinese_basic_mappings.json')

# Step 3: Use with the transliterator
from core.transliterator import HuffmanTransliterator
transliterator = HuffmanTransliterator('chinese_basic_mappings.json', use_optimized=False)

# Step 4: Test the transliterator with Chinese text
print("="*60)
print("CHINESE TRANSLITERATION TEST")
print("="*60)

# Test with actual Chinese text samples from the corpus
chinese_samples = [
    "经济学是一门对产品和服务的生产",
    "经济学注重的是研究经济行为",
    "微观经济学检视一个社会里基本",
    "宏观经济学则分析整个经济体",
    "经济学的分析也被用在其他"
]

print("\nTesting Basic Transliteration:")
print("-"*60)

for text in chinese_samples:
    # Transliterate to Latin
    latin = transliterator.transliterate_to_latin(text)
    
    # Restore original
    restored = transliterator.transliterate_from_latin(latin)
    
    # Check if lossless
    is_lossless = (text == restored)
    
    print(f"\nOriginal:  {text}")
    print(f"Latin:     {latin}")
    print(f"Restored:  {restored}")
    print(f"Lossless:  {'✓' if is_lossless else '✗'}")

# Summary
print("\n" + "="*60)
print("Character Analysis Summary:")
print("="*60)
analyzer.print_summary()

print("\n✓ Demo completed successfully!")
print(f"✓ JSON mapping file created: chinese_basic_mappings.json")
print(f"✓ Chinese is a NON-LATIN script - you should see visible transliteration!")
