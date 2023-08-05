"""Parser methods for chemical kinetics data.

This module contains a ReactionParser class with methods for
parsing reaction data from input XML files and interacting
with the SQL database used by the thermo module.
"""

import os
import sqlite3
import csv
import numpy as np


class ReactionParser():
    """This class contains functions to parse reaction data from XML."""

    def __init__(self, supported, hook):
        """Initialize ReactionParser."""
        self.struct = []
        self.keys = []
        self.hooked_rxn = hook
        self.supported_rxn = supported
        self.keys.append('phase')
        self.keys.append('reactionData')
        self.keys.append('reaction')
        self.keys.append('rateCoeff')
        self.keys.append('reactants')
        self.keys.append('products')

    def parse_species(self, rxns):
        """Return list of species.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        species: list of species

        """
        for s in rxns.findall('phase'):
            species = s.find('speciesArray').text.split()
        self.species = species

        return species

    def check_keys(self):
        """Check XML tags for completeness.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if tags are missing

        """
        for k in self.keys:
            varlist = [j.tag for j in self.rxns.iter(k)]
            if len(varlist) == 0:
                raise ValueError(k + " type not included in input file.")
            self.struct.append([k, len(varlist)])

    def check_structure(self):
        """Check XML file for consistency.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if system not covered or if data is missing

        """
        num_items = 0
        for k in self.struct:
            key, val = k
            if key in ('phase', 'reactionData'):
                if val != 1:
                    raise NotImplementedError("Cannot deal with " +
                                              "more than one system.")
            else:
                if num_items == 0:
                    num_items = val
                elif num_items != val:
                    raise ValueError("Missing data in input file.")

    def check_reaction_types(self):
        """Check acceptable reaction types.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if reaction type not covered

        """
        for r in self.rxns.iter('reaction'):
            rxn_type = r.attrib['type']
            rxn_id = r.attrib['id']
            if rxn_type != 'Elementary' and rxn_type not in self.hooked_rxn:
                raise NotImplementedError(
                                  "{} cannot be parsed." +
                                  "\nReaction type: {}" +
                                  "\nSupported: {}" +
                                  "\nHooked: {}".format(rxn_id,
                                                        rxn_type,
                                                        self.supported_rxn,
                                                        self.hooked_rxn))

    def check_reaction_consistency(self):
        """Check if reaction types consistent with equations.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if reaction type tag not consistent with equations.

        """
        rev_tags = []
        for r in self.rxns.iter('reaction'):
            if r.attrib['reversible'] == "yes":
                rev_tags.append(1)
            else:
                rev_tags.append(0)

        rev_eqs = []
        for r in self.rxns.iter('equation'):
            eq = r.text
            if eq.find('[=]') > 0:
                rev_eqs.append(1)
            else:
                rev_eqs.append(0)

        count = 0
        for tag, eq in zip(rev_tags, rev_eqs):
            count += 1
            if tag != eq:
                raise ValueError("Reversible tag inconsistent with reaction " +
                                 "equation for reaction id: {}".format(count))

    def check_species_eq_consistency(self):
        """Check that species in phase attribute and equations match.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if species listed in phase attribute are not consistent
        with species included in reaction equations.

        """
        # Reaction equations
        species_eq = []
        for r in self.rxns.iter('equation'):
            eq = r.text.split()
            for s in eq:
                char_mask = [c.isalpha() for c in s]
                if any(char_mask):
                    first = np.where(char_mask)[0][0]
                    specie = s[first:]

                    # Do not add 'M' in the specie list
                    if specie == 'M':
                        continue

                    species_eq.append(specie)

                    if specie not in self.species and specie != 'M':
                        raise ValueError("Specie '{}'".format(s) +
                                         " listed in reaction equation, not"
                                         " included in species phase array.")

        if set(self.species) != set(species_eq):
            d = set(self.species) - set(species_eq)
            raise ValueError("Phase array includes species not included in " +
                             "any of the reactions: {}".format(d))

    def check_species_stoich_consistency(self):
        """Check that species in phase attribute match products/reactants.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if species listed in phase attribute are not consistent
        with species included in reactants and products attributes.

        """
        # Reactants / Products
        types = ['reactants', 'products']
        species_stoich = []
        for t in types:
            for r in self.rxns.iter(t):
                string = r.text.replace(":", " ").split()
                for s in string:
                    if any(c.isalpha() for c in s):
                        species_stoich.append(s)
                        if s not in self.species:
                            raise ValueError("Specie '{}'".format(s) +
                                             " listed in " + t +
                                             " not included in phase array.")

        if set(self.species) != set(species_stoich):
            d = set(self.species) - set(species_stoich)
            raise ValueError("Phase array includes species not included in " +
                             "any of the reactions: {}".format(d))

    def check_species_in_db(self):
        """Check that data exists in thermo db for required species.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error message if species listed in phase attribute do not have valid
        data in the thermo SQL database.

        """
        # Connect to database
        path = os.path.dirname(__file__)
        db = sqlite3.connect(path + '/data/thermo.sqlite')
        cursor = db.cursor()

        # Check if data exists in SQL db
        tbls = ['LOW', 'HIGH', 'WEIGHTS']
        for t in tbls:
            query = "SELECT SPECIES_NAME FROM " + t + \
                    " WHERE SPECIES_NAME in " + \
                    str(self.species).replace("[", "(").replace("]", ")")
            species_db = [s[0] for s in cursor.execute(query).fetchall()]
            if len(species_db) != len(self.species):
                d = set(self.species) - set(species_db)
                raise ValueError("No data exists in the thermo database " +
                                 "for the following species: {}".format(d))

    def check_input_file(self, rxns):
        """Perform initial check on XML file by running check methods.

        INPUTS:
        =======
        rxns: XML file

        RETURNS:
        ========
        Error messages if any

        """
        # Initialize reaction variable
        self.rxns = rxns

        # Initial checks on XML structure
        self.check_keys()
        self.check_structure()

        # Reaction data consistency checks
        self.parse_species(rxns)
        self.check_reaction_types()
        self.check_reaction_consistency()
        self.check_species_eq_consistency()
        self.check_species_stoich_consistency()
        self.check_species_in_db()

    def parse_reaction_rate_params(self, reaction, convert_units):
        """Parse reaction rate coefficient parameters.

        INPUTS:
        =======
        reaction: parsed from XML
        convert_units: boolean whether to convert units or not

        RETURNS:
        ========
        d: dictionary of reaction rate coefficient type and relevant parameters

        NOTES:
        ========
        If convert_units is set to True, reaction rate coefficient units will
        be converted into the base SI-units: meter / Joule / mol. Users can
        add additional units to the data/unit.csv file if so desired

        """
        if convert_units:
            # Connect to csv file containing units
            path = os.path.dirname(__file__)
            with open(path + '/data/units.csv', 'r') as unit:
                next(unit)
                unit_dict = dict(csv.reader(unit))
            # Create dictionary of units
            dict_ = dict((k, float(v)) for k, v in unit_dict.items())

        # Loop over rateCoeff's and convert units where desired
        rateCoeffs = reaction.find('rateCoeff')

        output = []
        for rateCoeff in rateCoeffs:
            if rateCoeff.tag == 'Arrhenius':
                # If 'Arrhenius' units are to be converted
                if convert_units:
                    A_unit = rateCoeff.find('A').attrib['units'].split('/')
                    E_unit = rateCoeff.find('E').attrib['units'].split('/')
                    A_conv_lis = []
                    for unit in A_unit:
                        try:
                            A_conv_lis.append(dict_[unit])
                        except:
                            raise NotImplementedError(unit +
                                                      " not implemented.")
                    A_conversion = np.prod(np.array(A_conv_lis))
                    E_conv_lis = []
                    for unit in E_unit:
                        try:
                            E_conv_lis.append(dict_[unit])
                        except:
                            raise NotImplementedError(unit +
                                                      " not implemented.")
                    E_conversion = np.prod(np.array(E_conv_lis))
                    try:
                        A = float(rateCoeff.find('A').text)*A_conversion
                        E = float(rateCoeff.find('E').text)*E_conversion
                        d = {'Type': rateCoeff.tag, 'A': A, 'E': E}
                    except:
                        print("Conversion failed. " +
                              "Resulting units have not been converted.")
                        A = float(rateCoeff.find('A').text)
                        E = float(rateCoeff.find('E').text)
                        d = {'Type': rateCoeff.tag, 'A': A, 'E': E}
                    if rateCoeff.find('b') is not None:
                        raise ValueError("Cannot use 'b' in Arrhenius type.")
                # If 'Arrhenius' units are not to be converted
                if not convert_units:
                    try:
                        A = float(rateCoeff.find('A').text)
                        E = float(rateCoeff.find('E').text)
                        d = {'Type': rateCoeff.tag, 'A': A, 'E': E}
                    except:
                        raise ValueError("Reaction coefficient parameters " +
                                         "not as expected.")
                    if rateCoeff.find('b') is not None:
                        raise ValueError("Cannot use 'b' in Arrhenius type.")

            elif rateCoeff.tag in ('ModifiedArrhenius',
                                   'modifiedArrhenius',
                                   'Kooij'):
                kooij_name = ''
                try:
                    kooij_name = rateCoeff.attrib['name']
                except:
                    kooij_name = None
                # If 'modifiedArrhenius' units are to be converted
                if convert_units:
                    A_unit = rateCoeff.find('A').attrib['units'].split('/')
                    E_unit = rateCoeff.find('E').attrib['units'].split('/')
                    A_conv_lis = []
                    for unit in A_unit:
                        try:
                            A_conv_lis.append(dict_[unit])
                        except:
                            raise NotImplementedError(unit +
                                                      " not implemented.")
                    A_conversion = np.prod(np.array(A_conv_lis))
                    E_conv_lis = []
                    for unit in E_unit:
                        try:
                            E_conv_lis.append(dict_[unit])
                        except:
                            raise NotImplementedError(unit +
                                                      " not implemented.")
                    E_conversion = np.prod(np.array(E_conv_lis))
                    try:
                        A = float(rateCoeff.find('A').text)*A_conversion
                        b = float(rateCoeff.find('b').text)
                        E = float(rateCoeff.find('E').text)*E_conversion
                        d = {'Type': rateCoeff.tag, 'A': A, 'b': b, 'E': E}
                        if rateCoeff.tag == 'Kooij':
                            d['name'] = kooij_name
                    except:
                        print("Conversion failed. " +
                              "Resulting units have not been converted.")
                        A = float(rateCoeff.find('A').text)
                        b = float(rateCoeff.find('b').text)
                        E = float(rateCoeff.find('E').text)
                        d = {'Type': rateCoeff.tag, 'A': A, 'b': b, 'E': E}
                        if rateCoeff.tag == 'Kooij':
                            d['name'] = kooij_name
                # If 'modifiedArrhenius' units are not to be converted
                if not convert_units:
                    try:
                        A = float(rateCoeff.find('A').text)
                        b = float(rateCoeff.find('b').text)
                        E = float(rateCoeff.find('E').text)
                        d = {'Type': rateCoeff.tag, 'A': A, 'b': b, 'E': E}
                        if rateCoeff.tag == 'Kooij':
                            d['name'] = kooij_name
                    except:
                        raise ValueError("Reaction coefficient parameters " +
                                         "not as expected.")

            elif rateCoeff.tag == 'Constant':
                try:
                    k = float(rateCoeff.find('k').text)
                    d = {'Type': rateCoeff.tag, 'k': k}
                except:
                    raise ValueError("Non-numeric coefficient parameters.")

            elif rateCoeff.tag == 'efficiencies':
                temp_list = [item.split(':') for item
                             in rateCoeff.text.split(' ')]
                efficiencies = dict()
                efficiencies['Type'] = 'efficiencies'
                for item in temp_list:
                    efficiencies[item[0]] = item[1]
                efficiencies['default'] = rateCoeff.attrib['default']
                d = efficiencies

            elif rateCoeff.tag == 'Troe':
                alpha = float(rateCoeff.find('alpha').text)
                t1 = float(rateCoeff.find('T1').text)
                t2 = float(rateCoeff.find('T2').text)
                t3 = float(rateCoeff.find('T2').text)

                d = {'Type': rateCoeff.tag,
                     'alpha': alpha,
                     't1': t1,
                     't2': t2,
                     't3': t3}
            else:
                raise NotImplementedError(rateCoeff.tag + " not implemented.")

            output.append(d)
        return output

    def parse_stoich_coefs(self, string, species):
        """Parse stoichiometric coefficients.

        INPUTS:
        =======
        species: string parsed from XML

        RETURNS:
        ========
        coef_out: numpy array of integers

        """
        coef_out = np.zeros(len(species))
        components = string.split()
        try:
            for c in components:
                specie, coef = c.split(':')
                idx = species.index(specie)
                coef_out[idx] = int(coef)
        except:
            raise ValueError("Coefficient could not be matched with specie.")

        return coef_out

    def get_weight(self, string, species):
        """Get molecular weight of each reaction.

        INPUTS:
        =======
        species: string parsed from XML

        RETURNS:
        ========
        total_weight: total molecular weight (kg/kmol)

        """
        # Get stoiciometric coefficients
        coefs = self.parse_stoich_coefs(string, species)

        # Connect to database
        path = os.path.dirname(__file__)
        db = sqlite3.connect(path + '/data/thermo.sqlite')
        cursor = db.cursor()

        # Get molecular weight for each specie
        weights = np.zeros(len(species))
        for s in species:
            query = "SELECT MOLEC_WEIGHT FROM WEIGHTS WHERE SPECIES_NAME = '" + s + "'"
            w, = cursor.execute(query).fetchall()[0]
            idx = species.index(s)
            weights[idx] = w

        total_weight = np.dot(coefs, weights)
        return total_weight
