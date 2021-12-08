import pandas as pd

data = pd.read_csv('bbn_data.csv', sep=' ').astype(bool)

def pr(x):
	print(f'{x.sum()} / {len(x)} = {x.mean()}')

pr(data.G)
pr(data.loc[data.B].L)
pr(data.loc[~data.B].L)
pr(data.loc[data.B].I)
pr(data.loc[data.I & data.G].E)
pr(data.loc[data.I & ~data.G].E)

