import random, os, time

CLASS_MAP = {
    "Barbarian": ["STR", "CON", "DEX", "WIS", "CHA", "INT"],
    "Bard":      ["CHA", "DEX", "CON", "WIS", "INT", "STR"],
    "Cleric":    ["WIS", "CON", "STR", "DEX", "CHA", "INT"],
    "Druid":     ["WIS", "CON", "DEX", "CHA", "INT", "STR"],
    "Fighter":   ["STR", "CON", "DEX", "WIS", "CHA", "INT"],
    "Monk":      ["DEX", "WIS", "CON", "CHA", "STR", "INT"],
    "Paladin":   ["STR", "CHA", "CON", "WIS", "INT", "DEX"],
    "Ranger":    ["DEX", "WIS", "CON", "STR", "INT", "CHA"],
    "Rogue":     ["DEX", "CHA", "CON", "WIS", "INT", "STR"],
    "Sorcerer":  ["CHA", "CON", "DEX", "WIS", "INT", "STR"],
    "Warlock":   ["CHA", "CON", "DEX", "WIS", "INT", "STR"],
    "Wizard":    ["INT", "DEX", "CON", "WIS", "CHA", "STR"]
}

def roll_4d6_drop_lowest():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])

def generate_full_stat_block():
    raw_scores = [roll_4d6_drop_lowest() for _ in range(7)]
    raw_scores.sort()
    mulligan = raw_scores.pop(0) 
    return sorted(raw_scores, reverse=True), mulligan

def recommend_classes(final_stats):
    recommendations = []
    sorted_stats = sorted(final_stats, reverse=True)
    
    # 1. Convert dict to list of items so we can shuffle them
    class_items = list(CLASS_MAP.items())
    random.shuffle(class_items) # Breaks the alphabetical tie-breaker

    for dnd_class, priority in class_items:
        assignment = dict(zip(priority, sorted_stats))
        
        # 2. Smart Weighting (Primary x3, Secondary x2, Tertiary x1)
        p_val = assignment[priority[0]]
        s_val = assignment[priority[1]]
        t_val = assignment[priority[2]]
        fit_score = (p_val * 3) + (s_val * 2) + t_val
        
        recommendations.append((fit_score, dnd_class, assignment))

    # 3. Sort by fit_score (descending)
    recommendations.sort(key=lambda x: x[0], reverse=True)
    return recommendations

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- D&D 2025 Stat Prototype (4d6 Drop Lowest + Mulligan) ---")
    
    final_stats, dropped = generate_full_stat_block()
    print(f"\nYour Rolls: {final_stats} (Dropped Mulligan: {dropped})")

    recs = recommend_classes(final_stats)
    print("\nTOP 3 RECOMMENDED CLASSES:")
    for i in range(3):
        score, name, mapping = recs[i]
        print(f"{i+1}. {name} (Fit: {score}): {mapping}")
    print(f"these base stats exclude background bonuses!")