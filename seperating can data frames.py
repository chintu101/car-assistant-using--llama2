import csv
import pandas as pd
from asammdf import MDF

# Load your MF4 file
df = pd.read_csv("D:\DevTools\Projects\LLMS\data\Tesla_log.csv")
half = len(df) // 2
df = df.iloc[:half]

# Export to CSV
df.to_csv("D:\DevTools\Projects\LLMS\data\Tesla_log.csv")



'''df = pd.read_csv("D:\DevTools\Projects\LLMS\data\CAN signal extraction and translation dataset\log 1.csv")
print(df)'''

