from flask import Flask, request, jsonify
from flask_cors import CORS
from food_data import food_items
from cart_optimizer import optimize_cart
from price_comparator import compare_prices
from collections import Counter

# Create a Flask web server and enable CORS
app = Flask(__name__)
CORS(app)

# Root route to avoid 404 on the home page
@app.route('/')
def index():
    return "Backend is running"

# This is the API endpoint. The user interface will send a POST request here.
@app.route('/api/optimize-cart', methods=['POST'])
def optimize_cart_api():
    try:
        data = request.get_json()
        budget = int(data.get('budget'))
        duration = data.get('duration')
        nutrition_choice = data.get('nutrition_choice')

        if not all([budget, duration, nutrition_choice]):
            return jsonify({"error": "Missing parameters"}), 400

        # Your existing logic to calculate values
        duration_multipliers = {'day': 1, 'week': 7, 'month': 30}
        multiplier = duration_multipliers.get(duration, 1)
        daily_budget = budget / multiplier
        
        cart, daily_cost, total_protein, total_carbs, total_fiber, total_calories = optimize_cart(daily_budget, food_items, nutrition_choice)
        
        if nutrition_choice == 'protein':
            daily_nutrition = total_protein
        elif nutrition_choice == 'carbs':
            daily_nutrition = total_carbs
        elif nutrition_choice == 'fiber':
            daily_nutrition = total_fiber
        else:
            daily_nutrition = 0

        # Reformat the results into a JSON object
        total_cost = daily_cost * multiplier
        total_nutrition = daily_nutrition * multiplier
        total_calories_total = total_calories * multiplier
        
        prices = compare_prices(cart, food_items)
        best_platform = min(prices, key=prices.get)
        best_scaled_price = prices[best_platform] * multiplier

        aggregated_cart = Counter(item['name'] for item in cart)
        
        return jsonify({
            "cart": [{"name": name, "quantity": qty} for name, qty in aggregated_cart.items()],
            "total_cost": f"₹{total_cost:.2f}",
            "total_nutrition": f"{total_nutrition:.2f}g",
            "total_calories": f"{total_calories_total:.0f} kcal",
            "prices_by_platform": {platform: f"₹{cost * multiplier:.2f}" for platform, cost in prices.items()},
            "best_platform": f"{best_platform} (₹{best_scaled_price:.2f})"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
