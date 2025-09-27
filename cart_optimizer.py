from collections import defaultdict

def optimize_cart(budget, food_items, nutrition_choice='protein'):
    if nutrition_choice == 'carb':
        nutrition_choice = 'carbs'
    categories = set(item['category'] for item in food_items)
    used_budget = 0
    cart = []  # List of dicts, will aggregate later
    total_protein = 0
    total_carbs = 0
    total_fiber = 0
    total_calories = 0

    # Step 1: Pick the best item from each category, sorted by value desc to prioritize high-value categories
    cat_best = []
    for category in categories:
        cat_items = [item for item in food_items if item['category'] == category]
        if cat_items:
            best_item = max(cat_items, key=lambda i: i.get(nutrition_choice, 0) / min(i['price'].values()))
            price = min(best_item['price'].values())
            value = best_item.get(nutrition_choice, 0) / price if price > 0 else 0
            cat_best.append((value, category, best_item, price))
    cat_best.sort(reverse=True)  # High value first

    for value, category, best_item, price in cat_best:
        if used_budget + price <= budget:
            cart.append({'name': best_item['name'], 'price': price, 'calories': best_item.get('calories', 0)})
            used_budget += price
            total_protein += best_item.get('protein', 0)
            total_carbs += best_item.get('carbs', 0)
            total_fiber += best_item.get('fiber', 0)
            total_calories += best_item.get('calories', 0)

    # Step 2: Fill remaining budget with top scoring items (greedy)
    sorted_items = sorted(
        food_items,
        key=lambda item: item.get(nutrition_choice, 0) / min(item['price'].values()),
        reverse=True
    )
    while True:
        item_added = False
        for item in sorted_items:
            price = min(item['price'].values())
            if used_budget + price <= budget:
                cart.append({'name': item['name'], 'price': price, 'calories': item.get('calories', 0)})
                used_budget += price
                total_protein += item.get('protein', 0)
                total_carbs += item.get('carbs', 0)
                total_fiber += item.get('fiber', 0)
                total_calories += item.get('calories', 0)
                item_added = True
        if not item_added:
            break

    return cart, used_budget, total_protein, total_carbs, total_fiber, total_calories