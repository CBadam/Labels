import pandas as pd
df =pd.read_csv("prices.csv", sep=',', encoding='utf-8')
print(len(df))
for i in range(len(df)):
    product=df.loc[i,"product"]
    price=df.loc[i,"price"]
    print(f"{product} : {price}")