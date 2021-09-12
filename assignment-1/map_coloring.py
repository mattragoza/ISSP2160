
n = 3 # number of colors
k = 9 # number of countries

def n_states(i):
	if i == 0:
		return 1
	else:
		return n_states(i-1) * n # * (k - i)

total = 0
for i in range(0, k+1):
	total += n_states(i)

print(total)
