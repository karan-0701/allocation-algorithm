# Ad Bidding Simulation with Monte Carlo Analysis

A comprehensive simulation framework for analyzing online advertising bidding strategies with minimum impression constraints and decay-based allocation algorithms.

## 🎯 Overview

This project simulates real-time ad bidding scenarios where advertisers have minimum impression requirements and compete for limited ad inventory. The system uses Monte Carlo simulations to optimize decay factors and analyze competitive ratios between algorithmic and optimal revenue allocations.

## 🔧 Features

- **Real-time Traffic Simulation**: Models realistic web traffic patterns with peak hours and noise
- **Advertiser Bidding Logic**: Implements sophisticated bidding strategies with budget constraints
- **Decay-based Allocation**: Uses exponential decay functions to prioritize early time slots
- **Monte Carlo Optimization**: Finds optimal decay factors through extensive simulation
- **Competitive Ratio Analysis**: Compares algorithmic performance against optimal solutions
- **Generalized Perturbation Game (GPG)**: Handles excess impressions after minimum requirements

## 📁 Project Structure

```
ad-bidding-simulation/
├── advertiser.py              # Advertiser class definition
├── traffic_simulator.py       # Traffic pattern simulation
├── bidding_simulator.py       # Core bidding logic and algorithms
├── dataset_generator.py       # Synthetic advertiser data generation
├── monte_carlo_simulation.py  # Monte Carlo analysis framework
├── main.py                    # Main pipeline orchestrator
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/karan-0701/allocation-algorithm
```

2. Install dependencies:
```bash
pip install pandas numpy matplotlib tqdm
```

### Running the Simulation

Execute the complete pipeline:

```bash
python main.py
```

This will:
1. Generate a synthetic dataset of 10,000 advertisers (`advertiser_data_10k.csv`)
2. Run 50 Monte Carlo simulations with varying decay factors
3. Output results to `monte_carlo_results.csv`

## 📊 Understanding the Output

### Generated Files

#### `advertiser_data_10k.csv`
Contains synthetic advertiser data with the following columns:
- `AdvertiserId`: Unique identifier
- `Minimum_Impressions`: Required minimum impressions (500-10,000)
- `Budget`: Available budget after minimum requirements (10,000-25,000)
- `Bid`: Per-impression bid amount (1-100)
- `Reward`: Bonus reward for meeting minimum requirements (10,000-25,000)
- `Performance`: Historical performance metric (0.0-1.0)

#### `monte_carlo_results.csv`
Contains simulation results with:
- `advertiser_ids`: List of advertisers in the simulation
- `optimal_revenue`: Theoretical maximum revenue
- `max_reward`: Best achieved revenue from algorithm
- `max_competitive_ratio`: Ratio of achieved/optimal revenue
- `best_decay_factor`: Optimal decay factor for this scenario

## 🔬 Algorithm Details

### Core Components

1. **Traffic Simulation**: Models realistic web traffic with peak hours (9 AM - 5 PM) and random variations

2. **Allocation Strategy**: 
   - Prioritizes advertisers by expected revenue (bid × minimum impressions)
   - Applies exponential decay: `e^(-decay_rate × time_slot)`
   - Distributes remaining impressions proportionally

3. **Revenue Calculation**:
   ```
   Revenue = (bid × allocated_impressions) + reward_bonus
   ```
   (Only if minimum impressions are met)

### Key Parameters

- **Time Slots**: 24 (representing hours)
- **Decay Rate**: 0.01 - 1.0 (optimized via Monte Carlo)
- **Traffic Range**: 500-1,500 impressions per hour
- **Peak Amplitude**: 1.2× during business hours

## 📈 Customization

### Modifying Simulation Parameters

Edit the constants in `monte_carlo_simulation.py`:

```python
NUM_TIME_SLOTS = 24        # Simulation duration
NUM_SIMULATIONS = 50       # Monte Carlo iterations
MIN_ADV = 15              # Minimum advertisers per simulation
MAX_ADV = 25              # Maximum advertisers per simulation
```

### Custom Advertiser Sets

Replace the default advertisers in `bidding_simulator.py`:

```python
def init_advertisers(self):
    return {
        "Custom1": Advertiser("Custom1", bid=30, budget=300, min=15000, reward=150),
        "Custom2": Advertiser("Custom2", bid=25, budget=250, min=12000, reward=120),
        # Add more advertisers...
    }
```

### Traffic Patterns

Modify traffic characteristics in `traffic_simulator.py`:

```python
TrafficSimulator(
    min_impressions=500,    # Base traffic floor
    max_impressions=1500,   # Base traffic ceiling  
    peak_start=9,          # Peak hours start
    peak_end=17,           # Peak hours end
    peak_amplitude=1.2     # Peak traffic multiplier
)
```

## 🧪 Experimental Results

The system typically achieves:
- **Competitive Ratios**: 0.63 (algorithm vs optimal)
- **Optimal Decay Factors**: 0.2-0.6 (varies by scenario)
- **Runtime**: ~10-15 minutes for 50 simulations

Higher decay factors prioritize early allocation for high priority advertisers, while lower values spread impressions more evenly across time slots.