# bidding_simulator.py
import math
import random
import copy
from itertools import combinations

from advertiser import Advertiser
from traffic_simulator import TrafficSimulator

class BiddingSimulator:
    def __init__(self, min_impressions=500, max_impressions=1500, 
                    peak_start=9, peak_end=17, peak_amplitude=1.2,
                    decay_rate=0.01, alpha=0.7, beta=0.15):
        self.min_impressions = min_impressions
        self.max_impressions = max_impressions
        self.peak_start = peak_start
        self.peak_end = peak_end
        self.peak_amplitude = peak_amplitude
        self.decay_rate = decay_rate
        self.alpha = alpha
        self.beta = beta
        self.traffic = TrafficSimulator(min_impressions, max_impressions, peak_start, peak_end, peak_amplitude)
        self.run_gpg = True
        
    def init_advertisers(self):
        return {
            "A": Advertiser("A", 25, 250, 20000, 100), 
            "B": Advertiser("B", 24, 240, 15000, 100), 
            "C": Advertiser("C", 12, 125, 10000, 50),  
            "D": Advertiser("D", 30, 150, 5000, 0) 
        }

    # Sort advertisers by expected revenue of meeting minimum impressions
    def sort_advertisers(self, advertisers):
        advertisers_list = list(advertisers.values())
        advertisers_list.sort(key=lambda advertiser: advertiser.min * advertiser.bid, reverse=True)
        return advertisers_list

    # Estimate impressions for the current time slot
    def get_estimated_impressions(self, actual_impressions, initial_estimate, alpha=0.7):
        estimated = [initial_estimate]
        for i in range(1, len(actual_impressions)):
            estimated.append(int(alpha * actual_impressions[i-1] + (1 - alpha) * estimated[i-1]))
        return estimated

    # Calculate the decay probability for the current time slot
    def decay_probability(self, time_slot, decay_rate=0.01):
        return math.exp(-decay_rate * time_slot)

    def get_estimated_allocation(self, advertisers, estimated, time_slot):
        allocation = []
        decayed = int(estimated * self.decay_probability(time_slot))
        first_adv = min(decayed, advertisers[0].remaining)
        allocation.append(first_adv)
        impressions_left = estimated - first_adv + (decayed-first_adv)
        remaining_total = sum(advertiser.remaining * advertiser.bid for advertiser in advertisers[1:])
        for advertiser in advertisers[1:]:
            allocation.append(int(((advertiser.remaining * advertiser.bid)/ remaining_total) * impressions_left))
        return allocation

    def allocate(self, advertisers, index, impressions):
        if(impressions>0 and advertisers[index].remaining > 0):
            val = min(impressions, advertisers[index].remaining)
            advertisers[index].allocated += val
            advertisers[index].remaining -= val
            return_val = impressions - val
            return return_val
        return 0

    def check_satisfaction(self, advertisers, remaining_advertisers):
        for adv in remaining_advertisers[:]:
            if adv.remaining <= 0:
                advertisers[adv.name] = adv
                remaining_advertisers.remove(adv)

    def exp_beta(self, random_value, beta=0.15):
        return math.exp(beta*(random_value - 1))

    def gpg(self, advertisers):
        valid_advertisers = [adv for adv in advertisers.values() if adv.allocated < adv.max]
        if valid_advertisers:
            max_bid = float('-inf')
            selected_advertiser = None
            for advertiser in valid_advertisers:
                bid = advertiser.bid * (1-self.exp_beta(random.uniform(0,1)))
                if bid > max_bid:
                    max_bid = bid
                    selected_advertiser = advertiser
            return selected_advertiser.name, max_bid
        else:
            return None, 0
        
    def optimal_revenue(self, advertisers_dict, actual_impressions):
        advertisers = list(advertisers_dict.values())
        total_impressions = sum(actual_impressions)
        max_total_revenue = 0
        best_subset = []
        checked_subsets = []
        print()
        print(len(advertisers))
        for r in range(len(advertisers), 0, -1):
            current_level_subsets = []
            for subset in combinations(advertisers, r):
                subset_names = frozenset(adv.name for adv in subset)
                should_skip = False
                for checked_subset in checked_subsets:
                    if subset_names.issubset(checked_subset):
                        should_skip = True
                        break
                if should_skip:
                    continue
                    
                total_min_impressions = 0
                for adv in subset:
                    total_min_impressions += adv.min
                if total_min_impressions <= total_impressions:
                    current_level_subsets.append(subset_names)
                    subset_revenue = 0
                    for adv in subset:
                        subset_revenue += (adv.min * adv.bid) + adv.reward
                    if subset_revenue > max_total_revenue:
                        max_total_revenue = subset_revenue
                        best_subset = subset
            
            checked_subsets.extend(current_level_subsets)
            
        return max_total_revenue, best_subset

    def simulate_bidding(self, advertisers, num_time_slots, initial_impression_estimate, actual_impressions):
        sim_running = True
        sorted_advertisers = self.sort_advertisers(advertisers)
        remaining_advertisers = sorted_advertisers.copy()
        total_revenue = 0
        estimated_impressions = self.get_estimated_impressions(actual_impressions, initial_impression_estimate)

        for time_slot in range(num_time_slots):
            actual = actual_impressions[time_slot]
            estimated = estimated_impressions[time_slot]
            if remaining_advertisers:
                estimated_allocation = self.get_estimated_allocation(remaining_advertisers, estimated, time_slot)

            while actual>0 and sim_running:
                if remaining_advertisers:
                    for i in range(0, len(remaining_advertisers)):
                        if(estimated_allocation[i] > 0 and actual > 0):
                            val = min(estimated_allocation[i], actual)
                            return_val = self.allocate(remaining_advertisers, i, val)
                            actual = actual - val + return_val
                    self.check_satisfaction(advertisers, remaining_advertisers)
                elif self.run_gpg:
                    winning_adv, winning_bid = self.gpg(advertisers)
                    if winning_adv:
                        actual -= 1
                        advertisers[winning_adv].allocated += 1
                        print(f"Allocated 1 impression to {winning_adv} with perturbated bid {winning_bid:.2f}", end=" | ")
                    else:
                        print(f"All advertisers have reached their maximum impressions!")
                        sim_running = False
                else:
                    sim_running = False
                
        for advertiser in advertisers.values():
            total_revenue += advertiser.calculate_revenue()
        return total_revenue
        
    def run_simulation(self, num_time_slots=24, initial_impression_estimate=2500, custom_advertisers=None, run_gpg=True, decay_rate=0.01, actual_impressions=None):
        advertisers = custom_advertisers if custom_advertisers else self.init_advertisers()
        self.decay_rate = decay_rate
        self.run_gpg = run_gpg
        total_revenue = self.simulate_bidding(advertisers, num_time_slots, initial_impression_estimate, actual_impressions)
        return total_revenue, advertisers