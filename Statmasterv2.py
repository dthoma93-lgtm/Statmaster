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
BACKGROUNDS_2024 = {
    "Acolyte":    (["INT", "WIS", "CHA"], "Magic Initiate (Cleric)"),
    "Artisan":    (["STR", "DEX", "INT"], "Crafter"),
    "Charlatan":  (["DEX", "CON", "CHA"], "Skilled"),
    "Criminal":   (["DEX", "CON", "INT"], "Alert"),
    "Entertainer":(["STR", "DEX", "CHA"], "Musician"),
    "Farmer":     (["STR", "CON", "WIS"], "Tough"),
    "Guard":      (["STR", "INT", "WIS"], "Alert"),
    "Guide":      (["DEX", "CON", "WIS"], "Magic Initiate (Druid)"),
    "Hermit":     (["CON", "WIS", "CHA"], "Healer"),
    "Merchant":   (["CON", "INT", "CHA"], "Lucky"),
    "Noble":      (["STR", "INT", "CHA"], "Skilled"),
    "Sage":       (["CON", "INT", "WIS"], "Magic Initiate (Wizard)"),
    "Sailor":     (["STR", "DEX", "WIS"], "Tavern Brawler"),
    "Scribe":     (["DEX", "INT", "WIS"], "Skilled"),
    "Soldier":    (["STR", "DEX", "CON"], "Savage Attacker"),
    "Wayfarer":   (["DEX", "WIS", "CHA"], "Lucky")
} #

def roll_4d6_drop_lowest():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])

def generate_full_stat_block():
    raw_scores = [roll_4d6_drop_lowest() for _ in range(7)]
    raw_scores.sort()
    mulligan = raw_scores.pop(0) 
    return sorted(raw_scores, reverse=True), mulligan
def apply_background_2024(base_stats):
    print("\n--- CHOOSE A 2024 BACKGROUND ---")
    bg_names = list(BACKGROUNDS_2024.keys())
    for i, name in enumerate(bg_names,1):
        stats, feat = BACKGROUNDS_2024[name]
        print(f"{i:2}. {name:11} | Stats: {','.join(stats):13} | Feat: {feat}")
    choice = int(input("\n Select Background 9=(1-16): ")) - 1
    selected_bg = bg_names[choice]
    eligible_stats, feat = BACKGROUNDS_2024[selected_bg]

    print(f"\nBackground Selected: {selected_bg}")
    print(f"Origin Feat Gained: {feat}")
    print("\nHow would you like to distribute your +3 bonus?")
    print("1. +2 to one stat, +1 to another")
    print("2. +1 to all three eligible stats")
    
    mode = input("Choice (1 or 2): ")
    
    # We create a dictionary to track the bonuses to add to the base rolls later
    bonuses = {s: 0 for s in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]}
    if mode == "1":
        print(f"Eligible: {eligible_stats}")
        p2 = input("Stat for +2: ").upper()
        p1 = input("Stat for +1: ").upper()
        bonuses[p2] += 2
        bonuses[p1] += 1
    else:
        for s in eligible_stats:
            bonuses[s] += 1
            
    return bonuses, selected_bg, feat



def recommend_classes(final_stats, bg_bonuses):
    recommendations = []
    sorted_stats = sorted(final_stats, reverse=True)
    
    # 1. Convert dict to list of items so we can shuffle them
    class_items = list(CLASS_MAP.items())
    random.shuffle(class_items) # Breaks the alphabetical tie-breaker

    for dnd_class, priority in class_items:
        assignment = dict(zip(priority, sorted_stats))

        #add background bonuses to assigned stats

        for stat in assignment:
            assignment[stat] += bg_bonuses[stat]
        
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
    print("--- D&D 2024 Stat & Background Prototype ---")
    
    base_rolls, dropped = generate_full_stat_block()
    print(f"\nYour Base Rolls: {base_rolls} (Mulligan: {dropped})")

    bg_bonuses, bg_name, origin_feat = apply_background_2024(base_rolls)
    
    recs = recommend_classes(base_rolls, bg_bonuses)
    
    print(f"\n--- FINAL RESULTS FOR {bg_name.upper()} ---")
    print(f"Origin Feat: {origin_feat}")
    print("\nTOP 3 RECOMMENDED CLASSES (Including Background Bonuses):")
    for i in range(3):
        score, name, mapping = recs[i]
        print(f"{i+1}. {name} (Fit Score: {score}):")
        print(f"   {mapping}")