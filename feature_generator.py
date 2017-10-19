"""Base feature generation."""
import numpy as np
import json

from mendeleev import element


def return_features(inp):
    """Return feature space."""
    # Open previously generated features.
    with open('feature_store.json', 'r') as featurefile:
        store_dict = json.load(featurefile)

    # Pull out all relevant features for supplied system.
    afinger = np.asarray(store_dict['adsdict'][inp['a']], np.float64)
    facetfinger = np.asarray(store_dict['facetdict'][inp['facet']], np.float64)
    m1finger = np.asarray(store_dict['elemdict'][inp['m1']], np.float64)
    m2finger = np.asarray(store_dict['elemdict'][inp['m2']], np.float64)
    msum = m1finger + m2finger
    concfinger = np.asarray([inp['conc']], np.float64)
    sitefinger = np.asarray(store_dict['sitedict'][inp['site']], np.float64)

    return np.concatenate((afinger, m1finger, m2finger, concfinger,
                           facetfinger, sitefinger, msum))


def _feature_generate():
    """Base generator."""
    # Define atomic properties to add as features.
    prop = ['period', 'group_id', 'atomic_number', 'atomic_volume',
            'atomic_weight', 'melting_point', 'boiling_point', 'density',
            'dipole_polarizability', 'lattice_constant', 'vdw_radius',
            'covalent_radius_cordero', 'en_pauling', 'mass',
            'heat_of_formation']

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

    # Generate the features for all support elements.
    for e in elemdict:
        for p in prop:
            elemdict[e].append(getattr(element(e), p))
    elemdict['La'][1] = 2.5

    # Define the avaliable adsorbates.
    ads = {'C (graphene)': ['C'], 'CH2CH2': ['C']*2 + ['H']*4,
           'CH3CH2CH3': ['C']*3 + ['H']*8, 'CH3CH3': ['C']*2 + ['H']*6,
           'CO': ['C', 'O'], 'CO2': ['C'] + ['O']*2, 'H2O': ['H']*2 + ['O'],
           'HCN': ['H', 'C', 'N'], 'NH3': ['N'] + ['H']*3, 'NO': ['N', 'O'],
           'O2': ['O']*2, 'hfO2': ['O']}

    # Generate the summed features for all adsorbate elements.
    adsdict = {}
    for a in ads:
        adsdict[a] = list(np.zeros(len(prop)))
        for e in ads[a]:
            for r in range(len(prop)):
                adsdict[a][r] += getattr(element(e), prop[r])

    # Define facet features.
    facetdict = {'0001': [1.], '0001step': [2.], '100': [3.], '110': [4.],
                 '111': [5.], '211': [6.], '311': [7.], '532': [8.]}

    # Define site features.
    sitedict = {'AA': [1.], 'BA': [2.], 'BB': [3.]}

    store_dict = {'adsdict': adsdict, 'facetdict': facetdict,
                  'elemdict': elemdict, 'sitedict': sitedict}

    # Save the potential feature space.
    with open('feature_store.json', 'w') as featurefile:
        json.dump(store_dict, featurefile)


if __name__ == '__main__':
    _feature_generate()
