# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:02:20 2025

@author: Shubham Mohindru
"""

import re

class ParseError(Exception):
    pass

def parse_decision_tree(text: str) -> dict:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines or not lines[0].lower().startswith('decision:'):
        raise ParseError("First line must start with 'Decision:'")
    decision = lines[0].split(':', 1)[1].strip()

    options = []
    # pattern: - OptionName [prob1:val1, prob2:val2, ...]
    pattern = r'-\s*([^\[]+)\s*\[(.+)\]'
    for line in lines[1:]:
        match = re.match(pattern, line)
        if not match:
            continue
        name, rest = match.groups()
        outcomes = []
        for part in rest.split(','):
            prob_str, val_str = part.split(':')
            p = prob_str.strip()
            # support both "70%" and "0.7"
            if p.endswith('%'):
                prob = float(p[:-1]) / 100
            else:
                prob = float(p)
            value = float(val_str.strip())
            outcomes.append((prob, value))
        options.append({
            'name': name.strip(),
            'outcomes': outcomes
        })

    return {'decision': decision, 'options': options}

def compute_ev(tree: dict) -> dict:
    for opt in tree.get('options', []):
        ev = sum(prob * val for prob, val in opt['outcomes'])
        opt['ev'] = ev
    return tree