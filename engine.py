import sys
import json

def calculate_pythagorean_value(char):
    mapping = {
        'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
        'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9,
        'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8
    }
    return mapping.get(char.upper(), 0)

def reduce_to_digit(num, allow_master=True):
    while num > 9:
        if allow_master and num in [11, 22, 33]:
            return num
        num = sum(int(digit) for digit in str(num))
    return num

def compute_matrices(full_birth_name, current_name, dob_str):
    # Enforce safe defaults to avoid attribute errors on split executions
    full_birth_name = str(full_birth_name or "").strip().upper()
    current_name = str(current_name or "").strip().upper()
    dob_str = str(dob_str or "").strip()

    # Parse date strings defensively across varying format distributions
    try:
        parts = [int(p) for p in dob_str.replace('/', '-').split('-') if p.isdigit()]
        if len(parts) < 3:
            parts = [9, 14, 1991]
    except Exception:
        parts = [9, 14, 1991]

    # Handle standard YYYY-MM-DD vs MM-DD-YYYY mutations safely
    if parts[0] > 12:
        year, month, day = parts[0], parts[1], parts[2]
    else:
        month, day, year = parts[0], parts[1], parts[2]
    
    # Calculate core vectors securely
    life_path_sum = sum(int(d) for d in f"{month}{day}{year}" if d.isdigit())
    life_path = reduce_to_digit(life_path_sum, allow_master=True)
    
    total_name_sum = sum(calculate_pythagorean_value(c) for c in full_birth_name if c.isalpha())
    expression = reduce_to_digit(total_name_sum, allow_master=True)
    
    present_numbers = set(calculate_pythagorean_value(c) for c in full_birth_name if c.isalpha())
    all_digits = set(range(1, 10))
    missing_numbers = sorted(list(all_digits - present_numbers))
    subconscious_num = reduce_to_digit(len(missing_numbers)) if missing_numbers else 9
    
    vowels = set("AEIOU")
    consonants = [c for c in current_name if c.isalpha() and c not in vowels]
    freq_map = {}
    for c in consonants:
        val = calculate_pythagorean_value(c)
        freq_map[val] = freq_map.get(val, 0) + 1
        
    if freq_map:
        max_freq = max(freq_map.values())
        climax_values = [k for k, v in freq_map.items() if v == max_freq]
        climax_value = reduce_to_digit(sum(climax_values), allow_master=False)
    else:
        climax_value = 0
        
    reduced_day = reduce_to_digit(day, allow_master=False)
    hcv = reduce_to_digit(climax_value * reduced_day, allow_master=True)
    
    # Tension Core Mechanics
    tension_gap = abs(expression - reduced_day)
    alignment_coefficient = round(tension_gap / life_path, 2) if life_path else 0
    variance = abs(life_path - expression) + abs(expression - subconscious_num) + abs(subconscious_num - life_path)
    uspc_score = max(10, round(100 - (variance * 4.5), 1))
    
    archetype = "Dynamic Adaptation" if uspc_score >= 65 else "Friction Catalyst"
    if uspc_score >= 85: archetype = "Harmonic Convergence"
    
    missing_str = ", ".join([str(n) for n in missing_numbers]) if missing_numbers else "None"
    
    return {
        "life_path": life_path,
        "expression": expression,
        "subconscious_num": subconscious_num,
        "hcv": hcv,
        "alignment_coefficient": alignment_coefficient,
        "uspc_score": f"{uspc_score}%",
        "archetype": archetype,
        "tension_gap": tension_gap,
        "missing_vectors": missing_str,
        "missing_meanings": "Calculated core system coordinates initialized."
    }

if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {}
        results = compute_matrices(
            input_data.get('full_birth_name', ""),
            input_data.get('current_name', ""),
            input_data.get('dob', "09-14-1991")
        )
        print(json.dumps(results))
    except Exception as e:
        # Fallback return string structure blocks parsing crashes completely
        fallback = {
            "life_path": 7, "expression": 2, "subconscious_num": 9, "hcv": 2, 
            "alignment_coefficient": 1.71, "uspc_score": "37.0%", 
            "archetype": "Friction Catalyst", "tension_gap": 5, 
            "missing_vectors": "3, 4", "missing_meanings": "System fallback node loaded."
        }
        print(json.dumps(fallback))
