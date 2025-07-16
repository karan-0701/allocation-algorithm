def main():
    """
    Main function to run the complete ad bidding simulation pipeline.
    This will:
    1. Generate the advertiser dataset
    2. Run Monte Carlo simulations to find optimal decay factors
    3. Output results to CSV
    """
    from dataset_generator import generate_advertiser_dataset
    from monte_carlo_simulation import MonteCarloSimulation

    print("Starting Ad Bidding Simulation Pipeline...")
    
    # Step 1: Generate advertiser dataset
    print("\n1. Generating advertiser dataset...")
    dataset = generate_advertiser_dataset(num_entries=10000, filename='advertiser_data_10k.csv')
    print("Dataset generated successfully!")
    
    # Step 2: Run Monte Carlo simulation
    print("\n2. Running Monte Carlo simulation...")
    simulator = MonteCarloSimulation()
    results = simulator.run_monte_carlo(num_simulations=50, min_adv=15, max_adv=25)
    
    # Step 3: Display summary results
    print("\n3. Simulation Results Summary:")
    print(f"Average competitive ratio: {results['max_competetive_ratio'].mean():.4f}")
    print(f"Average decay factor: {results['best_decay_factor'].mean():.4f}")
    print(f"Results saved to 'monte_carlo_results.csv'")
    
    return results

if __name__ == "__main__":
    main()