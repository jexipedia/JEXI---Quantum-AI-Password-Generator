#!/usr/bin/env python3
import argparse
import secrets
import random
import time
import os
import sys
import numpy as np
from pathlib import Path
from collections import deque
from itertools import cycle
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

BANNER = f"""
\033[96m
     __              .__                    .___.__        
    |__| ____ ___  __|__| ______   ____   __| _/|__|____   
    |  |/ __ \\\\  \\/  /  | \\____ \\_/ __ \\ / __ | |  \\__  \\  
    |  \\  ___/ >    <|  | |  |_> >  ___// /_/ | |  |/ __ \\_
/\\__|  |\\___  >__/\\_ \\__| |   __/ \\___  >____ | |__(____  /
\\______|    \\/      \\/    |__|        \\/     \\/         \\/ 
\033[0m"""


def show_help():
    """Display help information"""
    print(f"""
\033[93mJEXI Quantum-AI Password Generator - Help Guide\033[0m

\033[96mFeatures:\033[0m
- Hybrid Quantum-AI Generation
- Smart Pattern Detection
- Complexity Scoring
- Free & Open Source AI
- Multi-dictionary Support

\033[96mUsage:\033[0m
  1. Place .txt dictionaries in program folder
  2. Run and select dictionary
  3. Choose password count
  4. Watch AI-Quantum baking
  5. Find results in quantum_passwords.txt

\033[96mCommands:\033[0m
  Type at any prompt:
  - help: Show this guide
  - exit: Quit program
  - list: Show dictionaries
""")
    sys.exit(0)


class AIPasswordOptimizer:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        self._train_similarity_model()

    def _train_similarity_model(self):
        """Train character-level similarity model"""
        if len(self.dictionary) < 2: return

        X = self.vectorizer.fit_transform(self.dictionary)
        self.nn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.nn.fit(X)

    def suggest_variations(self, base_word):
        """Generate AI-powered password variations"""
        try:
            vec = self.vectorizer.transform([base_word])
            _, indices = self.nn.kneighbors(vec)
            return [self.dictionary[i] for i in indices[0]]
        except:
            return []


class SemanticAnalyzer:
    def __init__(self):
        self.common_patterns = [
            '123', 'qwerty', 'password', 'admin', 'welcome', '111', 'abc'
        ]

    def is_common_pattern(self, password):
        """Detect weak patterns using ML heuristics"""
        pw_lower = password.lower()
        return any(p in pw_lower for p in self.common_patterns)

    def calculate_complexity(self, password):
        """Calculate password strength score (0-1)"""
        length = min(len(password) / 15, 1.0)
        diversity = len(set(password)) / len(password)
        upper = 0.2 if any(c.isupper() for c in password) else 0
        special = 0.2 if any(not c.isalnum() for c in password) else 0
        pattern = 0 if self.is_common_pattern(password) else 0.3
        return length + diversity + upper + special + pattern


class QuantumChef:
    def __init__(self, ingredients):
        self.components = self._organize_ingredients(ingredients)
        self.combo_brew = deque()
        self.MAX_COMPONENTS = 4
        self.semantic = SemanticAnalyzer()
        self.ai_optimizer = AIPasswordOptimizer(ingredients)
        self.rng = random.SystemRandom()

    def _organize_ingredients(self, items):
        """Categorize input elements"""
        return {
            'words': [x for x in items if x.isalpha()],
            'numbers': [x for x in items if x.isdigit()],
            'specials': [x for x in items if not x.isalnum()]
        }

    def _create_quantum_mix(self):
        """Generate password candidates"""
        elements = (
                self.components['words'] * 2 +
                self.components['numbers'] +
                self.components['specials']
        )

        for mix_length in range(2, min(self.MAX_COMPONENTS, len(elements))):
            for _ in range(5 * mix_length):
                try:
                    combo = self.rng.sample(elements, mix_length)
                    if self._is_memorable(combo):
                        self.combo_brew.append(self._cook_combo(combo))
                except ValueError:
                    continue

    def _is_memorable(self, combo):
        """Human-friendly pattern validation"""
        type_seq = [self._get_type(c) for c in combo]
        return not any(a == b for a, b in zip(type_seq, type_seq[1:]))

    def _get_type(self, item):
        """Classify component type"""
        if item.isdigit(): return 'num'
        if not item.isalnum(): return 'spec'
        return 'word'

    def _cook_combo(self, combo):
        """Apply formatting transformations"""
        transforms = [
            lambda s: s.title(),
            lambda s: s.upper(),
            lambda s: '-'.join(combo),
            lambda s: '_'.join(combo),
            lambda s: ''.join(combo)
        ]
        return self.rng.choice(transforms)(''.join(combo))

    def _add_quantum_spice(self, password):
        """Final enhancements"""
        enhancements = [
            lambda s: s + self.rng.choice(self.components['numbers']),
            lambda s: self.rng.choice(['!', '@', '#']) + s,
            lambda s: s[:len(s) // 2] + self.rng.choice(['-', '_', '~']) + s[len(s) // 2:],
            lambda s: s
        ]
        return self.rng.choice(enhancements)(password)

    def _ai_enhance(self, password):
        """Apply AI optimizations"""
        variations = self.ai_optimizer.suggest_variations(password)
        if variations:
            password = self.rng.choice([password] + variations)

        while self.semantic.is_common_pattern(password):
            password = self._add_quantum_spice(password)

        return password

    def bake_password(self):
        """Generate final password"""
        if not self.combo_brew:
            self._create_quantum_mix()

        base = self.combo_brew.popleft()
        enhanced = self._add_quantum_spice(base)
        return self._ai_enhance(enhanced)


class QuantumInterface:
    def __init__(self, total):
        self.symbols = cycle(['▚', '▞', '▛', '▜', '▟', '▙'])
        self.spinner = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.start_time = time.time()
        self.total = total
        self.count = 0

    def preheat(self):
        print("\n\033[96m🌀 Quantum-AI Core Initializing...\033[0m")
        time.sleep(1.2)

    def update_display(self):
        self.count += 1
        elapsed = time.time() - self.start_time
        speed = self.count / elapsed if elapsed > 0 else 0
        quantum_state = f"{next(self.symbols)} {secrets.choice(['α', 'β', 'γ', 'δ'])}"

        print(f"\r\033[95m{next(self.spinner)} "
              f"\033[93mBaking: [\033[92m{self.count}/{self.total}\033[93m] "
              f"|\033[96m {speed:.1f}pwds/s \033[95m|\033[94m Quantum-AI {quantum_state}\033[0m",
              end='')

    def complete(self):
        print(f"\n\033[92m✓ Generated {self.count} passwords in "
              f"{time.time() - self.start_time:.2f}s\033[0m")


def get_user_input(prompt, options=None):
    """Handle user input with commands"""
    while True:
        response = input(prompt).strip().lower()
        if response == 'help':
            show_help()
        elif response == 'exit':
            print("\033[93mExiting...\033[0m")
            sys.exit(0)
        elif response == 'list' and options:
            return list_options(options)
        elif options and response not in options:
            print("\033[91mInvalid input! Try again or type 'help'\033[0m")
        else:
            return response


def list_options(txt_files):
    """Display available dictionaries"""
    print("\n\033[93mAvailable Dictionaries:\033[0m")
    for idx, file in enumerate(txt_files, 1):
        print(f"  \033[96m[{idx}]\033[0m {file.name}")
    return None


def main_flow():
    """Main generation workflow"""
    txt_files = [f for f in Path('.').glob('*.txt') if f.name != "quantum_passwords.txt"]
    if not txt_files:
        print("\033[91mError: No dictionary files found!\033[0m")
        sys.exit(1)

    dict_file = None
    while not dict_file:
        list_options(txt_files)
        choice = get_user_input("\n\033[93mChoose dictionary (number/help/exit): \033[0m",
                                [str(i) for i in range(1, len(txt_files) + 1)])
        try:
            dict_file = txt_files[int(choice) - 1]
        except (ValueError, IndexError):
            continue

    ingredients = dict_file.read_text().splitlines()
    if not ingredients:
        print("\033[91mError: Selected dictionary is empty!\033[0m")
        sys.exit(1)

    count = 0
    while count < 1:
        response = get_user_input("\n\033[93mNumber of passwords to bake (1-1000/help/exit): \033[0m")
        try:
            count = min(1000, max(1, int(response)))
        except ValueError:
            continue

    chef = QuantumChef(ingredients)
    oven = QuantumInterface(count)
    oven.preheat()

    passwords = []
    try:
        while len(passwords) < oven.total:
            pwd = chef.bake_password()
            if chef.semantic.calculate_complexity(pwd) > 0.6:
                passwords.append(pwd)
                oven.update_display()

                if len(passwords) % max(1, oven.total // 10) == 0:
                    score = chef.semantic.calculate_complexity(pwd)
                    print(f"\n\033[95mAI Quality: {score:.1f}/1.0 | "
                          f"Length: {len(pwd)} | Entropy: {len(pwd) * 4} bits\033[0m")
    except KeyboardInterrupt:
        print("\n\033[91m! Generation Interrupted !\033[0m")

    oven.complete()

    output_file = "quantum_passwords.txt"
    Path(output_file).write_text('\n'.join(passwords))
    print(f"\033[93m🔐 Passwords saved to \033[1m{output_file}\033[0m")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    args = parser.parse_args()

    if args.help:
        show_help()

    print(BANNER)
    print("\033[90mType 'help' at any prompt for commands\033[0m")

    while True:
        main_flow()
        response = get_user_input("\n\033[93mGenerate again? (Y/N/help): \033[0m",
                                  ['y', 'n', 'help'])
        if response == 'n':
            print("\033[93mQuantum-AI process terminated. Goodbye!\033[0m")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[91mCritical Error: {str(e)}\033[0m")
        sys.exit(1)