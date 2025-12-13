from flask import Flask, request, jsonify
from flask_cors import CORS
import import_dataframe
import get_averages
import best_offer
from scipy.optimize import fsolve
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        set_equity = float(data.get('set_equity', 0.3))
        
        # Load data
        filepath = 'data.tsv'
        df = import_dataframe.import_dataframe(filepath)
        
        if df is None or df.empty:
            return jsonify({'error': 'Failed to load data'}), 500
        
        # Calculate averages
        avgs = get_averages.get_averages(df)
        
        if avgs is None:
            return jsonify({'error': 'Failed to calculate averages'}), 500
        
        # Solve equations
        initial_guess = [1, 1]
        offer = fsolve(lambda x: best_offer.equations(x, avgs, set_equity), initial_guess)
        
        # Convert days to years
        vesting_years = np.round((offer[1] / 365), 2)
        cliff_years = np.round((offer[0] / 365), 2)
        
        return jsonify({
            'success': True,
            'set_equity': set_equity,
            'vesting_years': float(vesting_years),
            'cliff_years': float(cliff_years),
            'vesting_days': int(offer[1]),
            'cliff_days': int(offer[0]),
            'avg_score': float(avgs[0]),
            'avg_ratio': float(avgs[1])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
