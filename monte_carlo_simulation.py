import pandas as pd
import numpy as np
import math
import random
import time
import copy
from tqdm import tqdm

from bidding_simulator import BiddingSimulator
from advertiser import Advertiser

class MonteCarloSimulation:
    def __init__(self):
        self.bidding_simulator = BiddingSimulator()
    
    def run_monte_carlo(self, num_simulations=50, min_adv=15, max_adv=25):
        # Load the advertiser dataset
        advertiser_data = pd.read_csv('advertiser_data_10k.csv')
        
        # Monte Carlo simulation parameters
        decay_factor_range = np.arange(0, 1.01, 0.01)
        results = []

        # Run Monte Carlo simulation
        for i in tqdm(range(num_simulations), desc="Running simulations"):
            # Set a unique seed based on the simulation iteration to ensure different samples
            random.seed(time.time() + i)
            sampled_advertisers = advertiser_data.sample(random.randint(min_adv,max_adv))
            # Convert sampled advertisers to Advertiser objects
            converted_advertisers = {}
            for idx, row in sampled_advertisers.iterrows():
                name = row['AdvertiserId']
                bid = row['Bid']
                budget = row['Budget']
                min_impressions = row['Minimum_Impressions']
                reward = row['Reward']
                converted_advertisers[name] = Advertiser(name=name,bid=bid,budget=budget,min=min_impressions,reward=reward)

            best_decay_factor = None
            max_reward = 0
            best_allocation = None
            actual_impressions = self.bidding_simulator.traffic.get_actual_impressions(24)
            # Test different decay factors
            for decay_factor in decay_factor_range:
                advertisers_copy = copy.deepcopy(converted_advertisers)
                reward, simulated_advertisers = self.bidding_simulator.run_simulation(custom_advertisers=advertisers_copy, run_gpg=False, decay_rate=decay_factor, actual_impressions=actual_impressions)
                if reward > max_reward:
                    max_reward = reward
                    best_decay_factor = decay_factor
                    best_allocation = simulated_advertisers.copy()
                del simulated_advertisers
                del advertisers_copy
            
            optimal, optimal_adv = self.bidding_simulator.optimal_revenue(converted_advertisers,actual_impressions)
            # Save the result for this simulation
            results.append({
                'advertiser_ids': sampled_advertisers['AdvertiserId'].tolist(),
                'optimal_revenue': optimal,
                'max_reward': max_reward,
                'max_competetive_ratio': max_reward/optimal,
                'best_decay_factor': best_decay_factor,
            })
            print(f"{i+1} --> {optimal}, {max_reward}, {max_reward/optimal}, {best_decay_factor}")
                        
        # Save results to a file
        output_file = 'monte_carlo_results.csv'
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        
        return results_df
