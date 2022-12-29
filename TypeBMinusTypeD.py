import math
import collections
from itertools import combinations

 
# Returns True if there exists a signed permutations of the given
# size with pinnacles as a pinnacle set.
def can_exist(pinnacles, size, is_d):
	pinnacles.sort(reverse=True)
	# Try to build a signed permutation that realizes the given pinnacle
	# set.
	permutation = [0] * size
	# Dict that will contain entries {pinnacle: index}, for each entry
	# in pinnacles, where 'index' is the index of the pinnacle in the
	# permutation being constructed (i.e. permutation[indexes[pinnacle]] == pinnacle).
	indexes = {}
	# A list containing the negative version of all remaining numbers
	# not in the permutation.
	remaining_numbers = [-i for i in range(1, size + 1)]
	first_pinnacle_index = 1
	last_pinnacle_index = first_pinnacle_index + 2 * (len(pinnacles) - 1)
	for x, i in zip(pinnacles, range(0, len(pinnacles))):
		index =  first_pinnacle_index + i if i % 2 == 0 else last_pinnacle_index - i + 1
		remaining_numbers.remove(0 - abs(x))
		indexes[x] = index
		permutation[index] = x
	if is_d:
		pinnacle_negatives = 0
		for x in pinnacles:
			if x < 0:
				pinnacle_negatives += 1
		if (pinnacle_negatives + len(remaining_numbers)) % 2 == 1:
			highest = max(remaining_numbers)
			remaining_numbers.remove(highest)
			remaining_numbers.insert(0, 0 - highest) 
	indexes = collections.OrderedDict(reversed(list(indexes.items())))
	for x, y in indexes.items():
		if value_at_index_or_max_pinnacle(permutation, y + 2, pinnacles) < value_at_index_or_max_pinnacle(permutation, y - 2, pinnacles):
			if permutation[y + 1] == 0:
				if remaining_numbers[-1] > x:
					return False
				permutation[y + 1] = remaining_numbers.pop()
			if permutation[y - 1] == 0:
				if remaining_numbers[-1] > x:
					return False
				permutation[y - 1] = remaining_numbers.pop()
		else:
			if permutation[y - 1] == 0:
				if remaining_numbers[-1] > x:
					return False
				permutation[y - 1] = remaining_numbers.pop()
			if permutation[y + 1] == 0:
				if remaining_numbers[-1] > x:
					return False
				permutation[y + 1] = remaining_numbers.pop()
	return True

	
# Returns the value of the permutation at index index,
# and if that doesn't exist, it returns the maximum vale
# in the pinnacles.
def value_at_index_or_max_pinnacle(permutation, index, pinnacles):
	if index == -1 or index == len(permutation):
		return max(pinnacles) + 1
	return permutation[index]
 

def sign_at(sign_bitmap, index):
	return  (-1) ** (sign_bitmap >> index & 1)
	

def generate_permutations_with(num_pinnacles, size):
	pinnacle_sets = []
	possible = combinations(list(range(1, size + 1)), num_pinnacles)
	for p in possible:
		for sign_bitmap in range(2 ** num_pinnacles):
			signed_p = [sign_at(sign_bitmap, index) * p[index] for index in range(num_pinnacles)]
			if can_exist(signed_p, size, False) and not can_exist(signed_p, size, True):
				pinnacle_sets.append(signed_p)
	return pinnacle_sets

 
size = int(input("What is the size of the permutation? "))
pinnacle_sets = []
for num_pinnacles in range(1, math.ceil(size / 2)):
	pinnacle_sets.extend(generate_permutations_with(num_pinnacles, size))
pinnacle_sets = list(map(sorted, pinnacle_sets))
print(pinnacle_sets, len(pinnacle_sets))
