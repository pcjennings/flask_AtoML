import numpy as np

from mendeleev import element

# Defining the finger vector
elemdict = {'Ag': [],
            'Al': [],
            'As': [],
            'Au': [],
            'B': [],
            'Ba': [],
            'Be': [],
            'Bi': [],
            'Ca': [],
            'Cd': [],
            'Co': [],
            'Cr': [],
            'Cs': [],
            'Cu': [],
            'Fe': [],
            'Ga': [],
            'Ge': [],
            'Hf': [],
            'Hg': [],
            'In': [],
            'Ir': [],
            'K': [],
            'La': [],  # 2.5
            'Li': [],
            'Mg': [],
            'Mn': [],
            'Mo': [],
            'Na': [],
            'Nb': [],
            'Ni': [],
            'O': [],
            'Os': [],
            'Pb': [],
            'Pd': [],
            'Pt': [],
            'Rb': [],
            'Re': [],
            'Rh': [],
            'Ru': [],
            'Sb': [],
            'Sc': [],
            'Si': [],
            'Sn': [],
            'Sr': [],
            'Ta': [],
            'Te': [],
            'Ti': [],
            'Tl': [],
            'V': [],
            'W': [],
            'Y': [],
            'Zn': [],
            'Zr': []}

p = [
        'period',
        'group_id',
        'atomic_number',
        'atomic_volume',
        'atomic_weight',
        'melting_point',
        'boiling_point',
        'density',
        'dipole_polarizability',
        'lattice_constant',
        'vdw_radius',
        'covalent_radius_cordero',
        'en_pauling',
        'mass',
        'heat_of_formation',
    ]
for i in elemdict:
    for j in p:
        elemdict[i].append(getattr(element(i), j))
elemdict['La'][1] = 2.5

adslist = {'C (graphene)': ['C'],
           'CH2CH2': ['C', 'C', 'H', 'H', 'H', 'H'],
           'CH3CH2CH3': ['C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                         'H'],
           'CH3CH3': ['C', 'C', 'H', 'H', 'H', 'H', 'H', 'H'],
           'CO': ['C', 'O'],
           'CO2': ['C', 'O', 'O'],
           'H2O': ['H', 'H', 'O'],
           'HCN': ['H', 'C', 'N'],
           'NH3': ['N', 'H', 'H', 'H'],
           'NO': ['N', 'O'],
           'O2': ['O', 'O'],
           'hfO2': ['O']
           }

adsdict = {}
for i in adslist:
    adsdict[i] = np.zeros(len(p))
    for j in adslist[i]:
        for k in range(len(p)):
            adsdict[i][k] += getattr(element(j), p[k])

alist = adsdict

facetlist = {'0001': 1., '0001step': 2., '100': 3., '110': 4., '111': 5.,
             '211': 6., '311': 7., '532': 8.}

sitelist = {'AA': 1., 'BA': 2., 'BB': 3.}


def finger(r):
    """Define feature space."""
    afinger = alist[r['a']]
    facetfinger = np.asarray([facetlist[r['facet']]])
    m1finger = np.asarray(elemdict[r['m1']])
    m2finger = np.asarray(elemdict[r['m2']])
    msum = m1finger + m2finger
    concfinger = np.asarray([r['conc']])
    sitefinger = np.asarray([sitelist[r['site']]])
    return np.concatenate((afinger, m1finger, m2finger, concfinger,
                           facetfinger, sitefinger, msum))
