from collections import defaultdict
import Propositional_KB_agent as pkb


def backwardchain(KB, theorem, verbose=True):

	# use a set to check whether rule antecedents
	#   are satisfied by the fact base
	fact_set = set(KB.FB)

	# use a dict to access what antecedent facts
	#   can be reached from each consequent fact
	rule_map = defaultdict(list)
	for rule in KB.RB:
		rule_map[rule.then_part].append(rule)

	if verbose:
		print('Inference:')

	n_rules_checked = 0

	def is_provable(fact, d=1):
		nonlocal n_rules_checked

		indent = "\t"*d
		print(f'{indent}Proving {fact}')

		if fact in fact_set:
			print(f'{indent}{fact}: Proof succeeded')
			return True

		for rule in rule_map[fact]:

			# check if antecedents are provable
			print(f'{indent}{fact} <- {" ^ ".join(rule.cond_part)}')
			n_rules_checked += 1
			if all(is_provable(f, d+1) for f in rule.cond_part):

				# a new fact can be proven
				KB.add_fact(fact)
				fact_set.add(fact)
				print(f'{indent}{fact}: Proof succeeded')
				return True

		print(f'{indent}{fact}: Proof failed')
		return False

	found_theorem = is_provable(theorem)

	if verbose:
		print('Fact base:')
		print(f'\t{" ^ ".join(KB.FB)}')
		print(f'KB |= {theorem}: {found_theorem}')
		print(f'n_rules_checked = {n_rules_checked}')
		print(f'len_fact_base = {len(fact_set)}\n')

	return found_theorem


for alpha in [
	pkb.theorem1,
	pkb.theorem2,
	pkb.theorem3,
	pkb.theorem4,
	pkb.theorem5,
]:
	KB = pkb.KB(pkb.init_RB, pkb.init_FB)
	backwardchain(KB, alpha)
