import import_dataframe
import get_averages
import best_offer
from scipy.optimize import fsolve
import numpy as np


def main():

  filepath = 'data.tsv'
  print()

  # Step 1: Import the Data
  df = import_dataframe.import_dataframe(filepath)

  if df is not None:
    print(df.head())
    print(f"\n Total rows: {len(df)}")
  else:
    print("Seriously? You fucked up loading the data? I'm jk loading the data is a pain")
    return

  # Step 2: Compute the averages
  avgs = get_averages.get_averages(df)

  if avgs is not None:
    print(f"\n The average score is {avgs[0]} and ratio is {avgs[1]}")
  else:
    print("Bruh you didn't compute the averages")
    return

  # Step 3: Solve the equation to get the score:
  equations = best_offer.equations
  initial_guess = [1,1]
  set_equity = 0.3
  offer = fsolve(lambda x: equations(x, avgs, set_equity), initial_guess)

  if offer is not None:
    print(f"\n Before rounding, if you're to accept the 30% equity ownership offer, you should add a vesting period of {np.round((offer[1] / 365),2)} years and a cliff at {np.round((offer[0] / 365),2)} years. \n")
  else:
    print("Uh oh! No offer found...")
    return


if __name__ == "__main__":
  main()