# Equity Split Calculator

A modern React web application for calculating optimal vesting period and cliff based on equity ownership.

## Features

- Simple, modern UI with gradient design
- Real-time calculation of vesting and cliff periods
- Input validation and error handling
- Responsive design for mobile and desktop

## Setup

### Backend (Flask)

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Install Python dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python3 app.py
```

Alternatively, use the convenience script:
```bash
./run_server.sh
```

The API will be available at `http://localhost:5001`

### Frontend (React)

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the React development server:
```bash
npm run dev
```

The app will open at `http://localhost:5173` (Vite's default port)

## Usage

1. Enter an equity value (e.g., 0.3 for 30%)
2. Press Enter or click "Calculate Splits"
3. View the calculated vesting period and cliff in years and days

## API Endpoints

- `POST /api/calculate` - Calculate splits based on equity value
  - Body: `{ "set_equity": 0.3 }`
  - Returns: Vesting period, cliff period, and related metrics

- `GET /api/health` - Health check endpoint
