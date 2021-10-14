import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

def bool_format(b):
	return '$\\top$' if b else ''

symbols = ['$P$', '$Q$', '$R$', '$S$', '$T$', '$U$']

index = pd.MultiIndex.from_product(
	names=symbols,
	iterables=[[False, True]]*len(symbols),
)
tt = pd.DataFrame(index=index).reset_index()
P, Q, R, S, T, U = tt.T.values

tt[
	'$\\neg (P \\land \\neg Q) \\lor \\neg (\\neg S \\land T) $'
] = ~(P & ~Q) | ~(~S & ~T)
tt[
	'$\\neg (T \\lor Q)$'
] = ~(T | Q)
tt[
	'$\\Rightarrow (\\neg T \\rightarrow (\\neg S \\land P))$'
] = U <= (~T <= (~S & P))
tt[
	'$\\neg U$'
] = ~U
tt.columns = range(10)
print(tt.to_latex(
	index=False,
	formatters=[bool_format]*len(tt.columns),
	escape=False,
	col_space=0,
))
