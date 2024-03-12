# Dataframe-Agent
Pandas dataframe agent. Ask your queries in natural language

## Usage
1. Import agent

```from DFagent import Agent```

2. Initialize the agent

```
df = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
})
dfs = [df]
agent = Agent(dfs)
```

3. Ask questions
```
result = agent.act("which country has the highest gdp?")
```
