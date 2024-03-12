# Dataframe-Agent
Pandas dataframe agent. Ask your queries in natural language

## Usage
1. Import agent

```from DFagent import Agent```

2. Initialize the agent

```
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
    'Age': [25, 30, 35, 40, 45],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Salary': [50000, 60000, 70000, 80000, 90000]
}

# Creating a DataFrame from the dictionary
df = pd.DataFrame(data)
dfs = [df]
agent = Agent(dfs)
```

3. Ask questions
```
result = agent.act("which country has the highest gdp?")
```

Sample for using agent can be found in demo.py python file

## References
- https://github.com/Sinaptik-AI/pandas-ai