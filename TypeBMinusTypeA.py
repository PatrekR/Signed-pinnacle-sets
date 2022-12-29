import math
import collections
from itertools import combinations
 

# Returns True if there exists a permutation of the given
# size with pinnacles as a pinnacle set with signs depending on
# what type of permutation is being constructed.
def can_exist(pinnacles, size, is_b):
	pinnacles.sort(reverse=True)
	# Try to build a signed permutation that realizes the given pinnacle
	# set.
	permutation = [0] * size
	# Dict that will contain entries {pinnacle: index}, for each entry
	# in pinnacles, where 'index' is the index of the pinnacle in the
	# permutation being constructed (i.e. permutation[indexes[pinnacle]] == pinnacle).
	indexes = {}
	# A list containing all remaining numbers not in the
	# permutation, with signs depending on what type of
	# pinnacles sets it wants.
	if is_b:
		remaining_numbers = [-i for i in range(1, size + 1)]
	else:
		remaining_numbers = list(reversed([i for i in range(1, size + 1)]))
	first_pinnacle_index = 1
	last_pinnacle_index = first_pinnacle_index + 2 * (len(pinnacles) - 1)
	for x, i in zip(pinnacles, range(0, len(pinnacles))):
		index = first_pinnacle_index + i if i % 2 == 0 else last_pinnacle_index - i + 1
		if is_b:
			remaining_numbers.remove(0 - abs(x))
		else:
			remaining_numbers.remove(abs(x))
		indexes[x] = index
		permutation[index] = x
	indexes = collections.OrderedDict(reversed(list(indexes.items())))
	for pinnacle, index in indexes.items():
		if value_at_index_or_max_pinnacle(permutation, index + 2, pinnacles) < value_at_index_or_max_pinnacle(permutation, index - 2, pinnacles):
			if permutation[index + 1] == 0:
				if remaining_numbers[-1] > pinnacle:
					return False
				permutation[index + 1] = remaining_numbers.pop()
			if permutation[index - 1] == 0:
				if remaining_numbers[-1] > pinnacle:
					return False
				permutation[index - 1] = remaining_numbers.pop()
		else:
			if permutation[index - 1] == 0:
				if remaining_numbers[-1] > pinnacle:
					return False
				permutation[index - 1] = remaining_numbers.pop()
			if permutation[index + 1] == 0:
				if remaining_numbers[-1] > pinnacle:
					return False
				permutation[index + 1] = remaining_numbers.pop()
	return True
		

# Returns the value of the permutation at index index,
# and if that doesn't exist, it returns the maximum vale
# in the pinnacles.
def value_at_index_or_max_pinnacle(permutation, index, pinnacles):
	if index == -1 or index == len(permutation):
		return max(pinnacles) + 1
	return permutation[index]

	
def generate_permutations_with(num_pinnacles, size):
	pinnacle_sets = []
	candidate_pinnacle_sets = combinations(list(range(1, size + 1)), num_pinnacles)
	for p in candidate_pinnacle_sets:
		p = list(p)
		if can_exist(p, size, True) and not can_exist(p, size, False):
			pinnacle_sets.append(p)
	return pinnacle_sets


size = int(input("What is the size of the permutation? "))
pinnacle_sets = []
for num_pinnacles in range(1, math.ceil(size / 2)):
	pinnacle_sets.extend(generate_permutations_with(num_pinnacles, size))
pinnacle_sets = list(map(sorted, pinnacle_sets))
print(pinnacle_sets, len(pinnacle_sets))
