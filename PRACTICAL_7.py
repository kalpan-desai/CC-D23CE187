# Define the grammar
grammar = {
    "S": [["A", "B", "C"], ["D"]],
    "A": [["a"], ["ε"]],
    "B": [["b"], ["ε"]],
    "C": [["(", "S", ")"], ["c"]],
    "D": [["A", "C"]]
}

first_sets = {}
follow_sets = {}

# Compute First Set
def compute_first(symbol):
    if symbol in first_sets:
        return first_sets[symbol]

    first = set()
    
    # Terminal case
    if symbol not in grammar:
        return {symbol}

    # Iterate over productions
    for production in grammar[symbol]:
        for i, sym in enumerate(production):
            first_of_sym = compute_first(sym)

            first.update(first_of_sym - {"ε"})
            
            # If ε is not in First(sym), stop
            if "ε" not in first_of_sym:
                break
        else:
            first.add("ε")

    first_sets[symbol] = first
    return first

# Compute Follow Set
def compute_follow(symbol):
    if symbol in follow_sets:
        return follow_sets[symbol]

    follow = set()
    
    # Start symbol gets $
    if symbol == "S":
        follow.add("$")

    for lhs, productions in grammar.items():
        for production in productions:
            for i, sym in enumerate(production):
                if sym == symbol:
                    # Check next symbol in production
                    for j in range(i + 1, len(production)):
                        next_symbol = production[j]
                        first_next = compute_first(next_symbol)

                        follow.update(first_next - {"ε"})
                        
                        # If next_symbol does not derive ε, stop
                        if "ε" not in first_next:
                            break
                    else:
                        # If nothing follows or everything can be ε, add Follow(LHS)
                        if lhs != symbol:
                            follow.update(compute_follow(lhs))

    follow_sets[symbol] = follow
    return follow

# Compute First and Follow for all non-terminals
for non_terminal in grammar.keys():
    compute_first(non_terminal)
    compute_follow(non_terminal)

# Print results
print("First Sets:")
for symbol, first in first_sets.items():
    print(f"First({symbol}) = {first}")

print("\nFollow Sets:")
for symbol, follow in follow_sets.items():
    print(f"Follow({symbol}) = {follow}")
