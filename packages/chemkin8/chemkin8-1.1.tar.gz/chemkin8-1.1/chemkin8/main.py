# import numpy as np
# import chemkin8
# from chemkin8 import chemkin
# import os

# # Input variables
# x1 = [2., 1., .5, 1., 1., 1.]
# x2 = [2., 1., .5, 1., 1., 1., .5, 1.]
# x3 = [0.5, 0., 0., 2., 0., 1., 0., 0.]
# T = 2500

# test_data_dir = os.path.join(os.path.dirname(chemkin8.__file__), 'tests/')
# fname1 = os.path.join(test_data_dir, 'rxns.xml')
# fname2 = os.path.join(test_data_dir, 'rxnset_long.xml')
# fname3 = os.path.join(test_data_dir, 'rxns_reversible.xml')
# fname4 = os.path.join(test_data_dir, 'rxns_irreversible.xml')
# fname5 = os.path.join(test_data_dir, 'rxns_mixed.xml')

#c = chemkin.chemkin(fname1)
# print(c.reaction_rates(x1, T))
# print("NASA Coeffs:", c.NASAcoeffs())

#c = chemkin.chemkin(fname2)
# print(c.reaction_rates(x2, T))

#c = chemkin.chemkin(fname3)
#print(c.reaction_rates(x3, T))

#c = chemkin.chemkin(fname4)
#print(c.reaction_rates(x3, T))

# c = chemkin.chemkin(fname5)
# print(c.reaction_rates(x2, T))

# Small Test:
# import chemkin as cmod
# cmod.chemkin(fname1)
# n = cmod.nuclear(['U'], ['Th'], [238], [234]) # Just an example, not an actual reaction
# # n = n.check_stable()
# n.generate_decay_series('Np', 237)


# from chemkin import *

# n = nuclear('tests/rxns_nuclear.xml')
# n.print_reaction(verbose=False)
