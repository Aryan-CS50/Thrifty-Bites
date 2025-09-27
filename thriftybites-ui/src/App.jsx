import { useState } from 'react';
import './App.css'; 

function App() {
  const [budget, setBudget] = useState('');
  const [duration, setDuration] = useState('week');
  const [nutrition, setNutrition] = useState('protein');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/optimize-cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          budget: parseInt(budget),
          duration: duration,
          nutrition_choice: nutrition
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (e) {
      setError('Failed to fetch data from the server. Is the Python server running?');
      console.error('There was an error!', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>ThriftyBites - Smart Grocery Cart</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Budget (₹):
          <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} required />
        </label>
        <label>
          Duration:
          <select value={duration} onChange={(e) => setDuration(e.target.value)}>
            <option value="day">Day</option>
            <option value="week">Week</option>
            <option value="month">Month</option>
          </select>
        </label>
        <label>
          Nutrition Priority:
          <select value={nutrition} onChange={(e) => setNutrition(e.target.value)}>
            <option value="protein">Protein</option>
            <option value="carbs">Carbohydrates</option>
            <option value="fiber">Fiber</option>
          </select>
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Shopping Cart'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {results && (
        <div className="results">
          <h2>Generated Cart</h2>
          <ul>
            {results.cart.map((item, index) => (
              <li key={index}>{item.quantity} x {item.name}</li>
            ))}
          </ul>
          <p>Total Cost: {results.total_cost}</p>
          <p>Total Nutrition: {results.total_nutrition}</p>
          <p>Total Calories: {results.total_calories}</p>
          <h3>Price Comparison</h3>
          {Object.entries(results.prices_by_platform).map(([platform, price]) => (
            <p key={platform}>{platform}: {price}</p>
          ))}
          <p>Best Platform: {results.best_platform}</p>
        </div>
      )}
    </div>
  );
}

export default App;