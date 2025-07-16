class Advertiser:
    def __init__(self, name, bid, budget, min, reward):
        self.name = name # Advertiser name
        self.bid = bid # Per impression bid
        self.budget = budget # Budget to spend after minimum impressions are met
        self.min = min # Minimum impressions required
        self.reward = reward # Reward for meeting minimum impressions
        self.allocated = 0 # Impressions allocated to the advertiser
        self.remaining = min # Remaining impressions to meet the minimum
        self.max = min + (budget//bid) # Maximum possible impressions that can be allocated
    
    def __str__(self):
        return f"Advertiser {self.name} -> Bid: {self.bid}, Minimum: {self.min}, Reward: {self.reward}, Allocated: {self.allocated}, Remaining: {self.remaining}"
    
    # Calculate revenue for the advertiser
    def calculate_revenue(self):
        total = 0
        if self.remaining <= 0:
            total = (self.bid * self.allocated) + self.reward
        return total