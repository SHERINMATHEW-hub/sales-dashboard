import pandas as pd
import numpy as np

def generate_tyre_data(rows=1000):
    np.random.seed(42) # Ensures the data is the same every time you run it

    # --- 1. DEFINE POSSIBILITIES ---
    towns = ['Kannur Town', 'Taliparamba', 'Payyanur', 'Thalassery', 'Iritty', 'Mattannur']
    brands = ['MRF', 'Apollo', 'CEAT', 'JK Tyre', 'Michelin', 'Bridgestone']
    vehicles = ['Motorcycle', 'Scooter', 'Car (Hatchback)', 'Car (Sedan)', 'Car (SUV)']
    factors = ['Price', 'Durability (Long Life)', 'Road Grip', 'Brand Trust', 'Mechanic Advice']

    # --- 2. GENERATE DATA WITH PROBABILITIES ---
    # We use probabilities (p) to make it realistic. 
    # E.g., MRF is more popular (30%) than Michelin (5%) in this region.
    
    data = {
        'Respondent_ID': range(1, rows + 1),
        'Town': np.random.choice(towns, rows),
        
        'Vehicle_Type': np.random.choice(vehicles, rows, p=[0.3, 0.2, 0.3, 0.1, 0.1]),
        
        'Current_Brand': np.random.choice(brands, rows, p=[0.30, 0.25, 0.20, 0.15, 0.05, 0.05]),
        
        'Purchase_Factor': np.random.choice(factors, rows, p=[0.4, 0.3, 0.1, 0.1, 0.1]),
        
        # Generate prices based on a normal distribution (Bell Curve)
        'Price_Paid': np.random.normal(3500, 1200, rows).astype(int),
        
        # Satisfaction Score (1-10)
        'Satisfaction_Score': np.random.randint(4, 11, rows)
    }

    # Adjust prices: Ensure no negative prices and valid range
    data['Price_Paid'] = np.abs(data['Price_Paid']) 
    
    df = pd.DataFrame(data)
    return df

# Run the function and save to CSV
if __name__ == "__main__":
    df = generate_tyre_data()
    df.to_csv("kerala_tyre_data.csv", index=False)
    print("✅ Success! 'kerala_tyre_data.csv' has been generated.")
