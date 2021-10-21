from collections import defaultdict
import Propositional_KB_agent as pkb


def forwardchain(KB, theorem, verbose=True):

	# use a set to check whether rule antecedents
	#   are satisfied by the fact base
	fact_set = set(KB.FB)

	# use a dict to track what rules have consequents
	#   that are not already in the fact base
	rule_map = defaultdict(list)
	for rule in KB.RB:
		if rule.then_part not in fact_set:
			rule_map[rule.then_part].append(rule)

	if verbose:
		print('Inference:')

	# repeat until no new facts are inferred
	found_theorem = (theorem in fact_set)
	found_new_facts = True
	n_rules_checked = 0
	while found_new_facts and not found_theorem:
		found_new_facts = False

		# scan rules with consequents not already in fact base
		for fact, rules in list(rule_map.items()):
			for rule in rules:

				# check whether all antecedents are satisfied
				satisfied = all(f in fact_set for f in rule.cond_part)
				n_rules_checked += 1

				if verbose:
					print(f'\t{" ^ ".join(rule.cond_part)} -> {fact}: {satisfied}')

				if not satisfied:
					continue

				if verbose:
					print(f'\t\tProved {fact}')

				# antecedents are satisfied, so a new fact can be inferred
				found_new_facts = True
				found_theorem = (fact == theorem)

				# add the new fact to knowledge base
				KB.add_fact(fact)
				fact_set.add(fact)

				# stop checking rules that lead to this fact
				del rule_map[fact]
				break

			if found_theorem:
				break

		if found_theorem:
			break

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
	forwardchain(KB, alpha)
