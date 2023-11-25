import io
import pandas as pd

with open("src/russia.csv", encoding="utf-8",) as f:
            state_data = pd.read_csv(io.StringIO(f.read()))
    
    

state_data.sort_values(["Name"])
print(state_data)