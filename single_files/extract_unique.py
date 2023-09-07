import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output.csv')
counts = df['Classification'].value_counts()

counts.plot(kind='bar')
plt.show()