import pandas as pd

from DFagent import Agent

data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Emily"],
    "Age": [25, 30, 35, 40, 45],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Salary": [50000, 60000, 70000, 80000, 90000],
}

# Creating a DataFrame from the dictionary
df = pd.DataFrame(data)
dfs = [df]

agent = Agent(dfs)

result = agent.act(
    "what are the names with salary greater than 50k?"
)

print("Result: ", result)
