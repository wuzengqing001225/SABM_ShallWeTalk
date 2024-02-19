import matplotlib.pyplot as plt
import pandas as pd

import Function_Plot
import Function_Theoretical_Solution

para_cost = [2, 2]
para_a = 14
para_d = 0.00333333333333
#para_d = 0.0
para_beta = 0.00666666666666

ideal_price_lb = [0, 0]
ideal_price_ub = [0, 0]
ideal_profit_lb = [0, 0]
ideal_profit_ub = [0, 0]
ideal_solution = [ideal_price_lb, ideal_price_ub, ideal_profit_lb, ideal_profit_ub]
ideal_solution = Function_Theoretical_Solution.theoretical_upperbound(para_cost, para_a, para_d, para_beta)

id = "11-05-230913"
csv_file = f"{id}/logs_decision_plot.csv"
df_decision = pd.DataFrame(pd.read_csv(csv_file))

Function_Plot.data_visulization([], df_decision, ideal_solution, output_folder=f"{id}/")
