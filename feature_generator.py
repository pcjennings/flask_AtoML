"""Base feature generation."""
import numpy as np

from mendeleev import element

# Define atomic properties to add as features.
prop = ['period', 'group_id', 'atomic_number', 'atomic_volume',
        'atomic_weight', 'melting_point', 'boiling_point', 'density',
        'dipole_polarizability', 'lattice_constant', 'vdw_radius',
        'covalent_radius_cordero', 'en_pauling', 'mass', 'heat_of_formation']

# Initialize finger vector for support elements.
elemdict = {'Ag': [], 'Al': [], 'As': [], 'Au': [], 'B': [], 'Ba': [],
            'Be': [], 'Bi': [], 'Ca': [], 'Cd': [], 'Co': [], 'Cr': [],
            'Cs': [], 'Cu': [], 'Fe': [], 'Ga': [], 'Ge': [], 'Hf': [],
            'Hg': [], 'In': [], 'Ir': [], 'K': [], 'La': [], 'Li': [],
            'Mg': [], 'Mn': [], 'Mo': [], 'Na': [], 'Nb': [], 'Ni': [],
            'O': [], 'Os': [], 'Pb': [], 'Pd': [], 'Pt': [], 'Rb': [],
            'Re': [], 'Rh': [], 'Ru': [], 'Sb': [], 'Sc': [], 'Si': [],
            'Sn': [], 'Sr': [], 'Ta': [], 'Te': [], 'Ti': [], 'Tl': [],
            'V': [], 'W': [], 'Y': [], 'Zn': [], 'Zr': []}

for e in elemdict:
    for p in prop:
        elemdict[e].append(getattr(element(e), p))
elemdict['La'][1] = 2.5

ads = {'C (graphene)': ['C'], 'CH2CH2': ['C', 'C', 'H', 'H', 'H', 'H'],
       'CH3CH2CH3': ['C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
       'CH3CH3': ['C', 'C', 'H', 'H', 'H', 'H', 'H', 'H'], 'CO': ['C', 'O'],
       'CO2': ['C', 'O', 'O'], 'H2O': ['H', 'H', 'O'], 'HCN': ['H', 'C', 'N'],
       'NH3': ['N', 'H', 'H', 'H'], 'NO': ['N', 'O'], 'O2': ['O', 'O'],
       'hfO2': ['O']}

adsdict = {}
for a in ads:
    adsdict[a] = np.zeros(len(prop))
    for e in ads[a]:
        for r in range(len(prop)):
            adsdict[a][r] += getattr(element(e), prop[r])

facetdict = {'0001': 1., '0001step': 2., '100': 3., '110': 4., '111': 5.,
             '211': 6., '311': 7., '532': 8.}

sitedict = {'AA': 1., 'BA': 2., 'BB': 3.}

store_dict = {'adsdict': adsdict, 'facetdict': facetdict, 'elemdict': elemdict,
              'sitedict': sitedict}


def finger(r):
    """Define feature space."""
    afinger = adsdict[r['a']]
    facetfinger = np.asarray([facetdict[r['facet']]])
    m1finger = np.asarray(elemdict[r['m1']])
    m2finger = np.asarray(elemdict[r['m2']])
    msum = m1finger + m2finger
    concfinger = np.asarray([r['conc']])
    sitefinger = np.asarray([sitedict[r['site']]])

    return np.concatenate((afinger, m1finger, m2finger, concfinger,
                           facetfinger, sitefinger, msum))
