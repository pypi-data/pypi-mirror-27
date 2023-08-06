"""Flamespeed chemical kinetics library."""

import os
import numpy as np
import xml.etree.ElementTree as ET
from flamespeed.thermo import thermochem
from flamespeed.parser import ReactionParser


class ReactionCoefficients():
    """This class contains functions that return reaction rate coefficients."""

    def k_const(self, k=1.0):
        """Simply returns a constant reaction rate coefficient.

        INPUTS:
        =======
        k: float, default value = 1.0
           Constant reaction rate coefficient

        RETURNS:
        ========
        self.kf: float
           Constant reaction rate coefficient

        EXAMPLES:
        =========
        >>> ReactionCoefficients().k_const()
        1.0
        >>> ReactionCoefficients().k_const(5)
        5.0

        """
        if k < 0:
            raise ValueError("Negative reaction rate coefficients prohibited.")

        return float(k)

    def k_arrhenius(self, A, E, T, R=8.3144621):
        """Arrhenius reaction rate coefficient.

        INPUTS
        =======
        A: float, positive
           Arrhenius prefactor
        E: float
           Activation energy
        T: float, positive
           Temperature in Kelvin
        R: float, positive, default value = 8.314
           Ideal gas constant

        RETURNS
        ========
        self.arr: float
           Arrhenius reaction rate coefficient

        EXAMPLES
        =========
        >>> ReactionCoefficients().k_arrhenius(A=10**7, E=15**2, T=100)
        7629118.26701253
        >>> ReactionCoefficients().k_arrhenius(A=2**7, E=15**2, T=100)
        97.65271381776039

        """
        if A < 0:
            raise ValueError("A = {0:18.16e}:  \
                    Negative Arrhenius prefactor not allowed.".format(A))

        if T < 0.0:
            raise ValueError("T = {0:18.16e}: \
                    Negative temperatures not allowed".format(T))

        if R < 0.0:
            raise ValueError("R = {0:18.16e}: \
                    Negative ideal gas constant is prohibited!".format(R))

        self.arr = A * np.exp(-(E / (R * T)))
        return float(self.arr)

    def k_arrhenius_mod(self, A, b, E, T, R=8.3144621):
        """Return Modified Arrhenius reaction rate coefficient.

        INPUTS
        =======
        A: float, positive
           Arrhenius prefactor
        b: float
           Modified Arrhenius parameter
        E: float
           Activation energy
        T: float, positive
           Temperature in Kelvin
        R: float, positive, default value = 8.314
           Ideal gas constant

        RETURNS
        ========
        self.k_modarr: float
           Modified Arrhenius reaction rate coefficient

        EXAMPLES
        =========

        >>> ReactionCoefficients().k_arrhenius_mod(A=2**7, b=1, E=15**2, T=100)
        9765.271381776038
        >>> ReactionCoefficients().k_arrhenius_mod(A=2**7, b=3, E=15**2, T=100)
        97652713.8177604

        """
        if A < 0:
            raise ValueError("A = {0:18.16e}:  \
                    Negative Arrhenius prefactor not allowed.".format(A))

        if T <= 0.0:
            raise ValueError("T = {0:18.16e}: \
                    Negative temperatures not allowed".format(T))

        if R < 0.0:
            raise ValueError("R = {0:18.16e}: \
                    Negative ideal gas constant is prohibited!".format(R))

        self.k_modarr = A * T**b * np.exp(-(E / (R * T)))
        return float(self.k_modarr)


class ReactionRate(ReactionCoefficients):
    """Base class with functions to calculate progress and reaction rates."""

    def __init__(self):
        """Initialize ReactionRate class."""
        super().__init__()
        self.num_reactions = 0
        self.num_species = 0
        self.rev = []
        self.rtype = ""
        self.species_list = []
        self.k_params = []
        self.k_params_nonelementary = []
        self.kf = []
        self.kb = []
        self.reactant_coef = []
        self.product_coef = []
        self.supported_rxn = ['Elementary']
        self.hooked_rxn = ['ThreeBody', 'TroeFalloffThreeBody', 'Duplicate']

    def __str__(self):
        """Return summary of XML file contents."""
        if self.num_reactions == 0:
            return "None"
        else:
            if self.rev.count(True) == self.num_reactions:
                rev_system = "Yes"
            elif (self.rev.count(True) != 0 and
                  self.rev.count(True) != self.num_reactions):
                rev_system = 'Some'
            else:
                rev_system = "No"
            return "Number_of_reactions:{} \
                    \nNumber_of_species:{} \
                    \nNumber_of_reversible_reactions:{} \
                    \nReversible:{} \
                    \nReaction_type:{} \
                    \nSpecies_list:{}\n" \
                        .format(self.num_reactions,
                                self.num_species,
                                self.rev.count(True),
                                rev_system,
                                self.rtype,
                                self.species_list)

    def __repr__(self):
        """Return class type."""
        return "<chemkin.ReactionRate>"

    def __len__(self):
        """Return number of reactions."""
        return self.num_reactions

    def read_XML(self, path, verify_integrity=True, check_mass=True, convert_units=False):
        """Read XML from file path and extracts reaction information.

        INPUTS
        =======
        path: string, path to the XML file

        RETURNS
        ========
        self: ReactionRate class instance

        EXAMPLE
        ========
        >>> ReactionRate().read_XML('./data/rxns_hw5.xml')
        <chemkin.ReactionRate>

        """
        # Clear local class variable contents
        self.__init__()

        # Import file
        path = os.path.join(os.getcwd(), path)
        tree = ET.parse(path)
        rxns = tree.getroot()

        # Instantiate parser
        parser = ReactionParser(self.supported_rxn, self.hooked_rxn)

        # Checks
        if verify_integrity:
            parser.check_input_file(rxns, check_mass)

        # Get list of species
        self.species_list = parser.parse_species(rxns)
        self.num_species = len(self.species_list)

        # Get reaction data
        for reaction in rxns.find('reactionData').findall('reaction'):
            self.num_reactions += 1

            rev = False if reaction.attrib['reversible'] == 'no' else True
            self.rev.append(rev)
            self.rtype = reaction.attrib['type']

            # Elementary, reversible reactions
            if self.rtype == 'Elementary' or self.rtype in self.hooked_rxn:

                # Get reaction rate coefficient parameters
                p = parser.parse_reaction_rate_params(reaction, convert_units)
                self.k_params.append(p[0])
                if len(p) > 1:
                    self.k_params_nonelementary.append(p)

                # Get stoichiometric coefficients
                s = reaction.find('reactants').text
                r_coeffs = parser.parse_stoich_coefs(s, self.species_list)
                self.reactant_coef.append(r_coeffs)

                # Get stoichiometric coefficients for products
                s = reaction.find('products').text
                p_coeffs = parser.parse_stoich_coefs(s, self.species_list)
                self.product_coef.append(p_coeffs)

                # Check conservation of mass
                if check_mass:
                    s = reaction.find('reactants').text
                    r_weight = parser.get_weight(s, self.species_list)
                    s = reaction.find('products').text
                    p_weight = parser.get_weight(s, self.species_list)
                    try:
                        np.testing.assert_almost_equal(r_weight - p_weight, 0,
                                                       decimal=3)
                    except:
                        raise ValueError("Conservation of mass violation " +
                                         "in reaction data.")

            else:
                raise NotImplementedError("[{}] Parsing for this reaction " +
                                          "is not implemented")

        # Transpose and convert to np arrays
        self.reactant_coef = np.asarray(self.reactant_coef).T
        self.product_coef = np.asarray(self.product_coef).T
        self.nu_coef = self.product_coef - self.reactant_coef

        return self

    def set_temp(self, T):
        """Calculate reaction rate coefficients at specified temperature.

        INPUTS
        =======
        T: Float, positive
           Temperature in Kelvin

        RETURNS
        =======
        k: float
           Reaction rate coefficients for each reaction

        EXAMPLE
        ========
        >>> ReactionRate().read_XML('./data/rxns_hw5.xml').set_temp(1500)
        <chemkin.ReactionRate>

        """
        if self.rtype not in self.supported_rxn:
            raise NotImplementedError("{} is not implemented"
                                      .format(self.rtype))

        try:
            T = float(T)
        except:
            raise ValueError("Temperature must be numeric.")

        if len(self.k_params) == 0:
            raise TypeError("Reaction data not imported. Use read_XML method.")

        # Calculate forward reaction rate coefficients
        self.kf = []
        for d in self.k_params:
            name = d['Type']
            if name == 'Arrhenius':
                A, E = d['A'], d['E']
                val = self.k_arrhenius(A, E, T)
            elif name == "modifiedArrhenius":
                A, b, E = d['A'], d['b'], d['E']
                val = self.k_arrhenius_mod(A, b, E, T)
            elif name == "Constant":
                c = d['k']
                val = self.k_const(c)
            else:
                raise TypeError("Reaction rate coefficient not found.")
            self.kf.append(val)

        # Backward reaction rate coefficients for reversible reactions
        if self.rev.count(True) > 0:
            tc = thermochem(self.species_list, self.nu_coef)
            self.kb = tc.backward_coeffs(self.kf, T)

        return self

    def get_progress_rate(self, concs):
        """Calculate progress rate for elementary reactions.

        INPUTS
        =======
        concs:          numpy array of floats
                        size: num_species
                        concentration of species

        RETURNS
        ========
        w:              numpy array of floats
                        size: num_reactions
                        progress rate for each reaction

        EXAMPLES
        =========
        >>> ReactionRate().read_XML('./data/rxns_hw5.xml').set_temp(1500).get_progress_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0]))
        array([  2.81180269e+08,   5.00000000e+03,   4.48513835e+06])

        """
        if len(self.reactant_coef) == 0:
            raise TypeError("Reaction data not imported. Use read_XML method.")

        if len(self.kf) == 0:
            raise TypeError("Reaction coefficients needs to be " +
                            "calculated with set_temp method.")

        if self.num_species != len(concs):
            raise ValueError("Dimensions of concentration and coefficient " +
                             "arrays are not aligned.")

        if np.sum(concs < 0) != 0:
            raise ValueError("Negative specie concentrations.")

        # Get forward component
        wf = np.zeros(self.num_reactions)
        for i in range(self.num_reactions):
            wf[i] = (self.kf[i] *
                     np.product(np.power(concs, self.reactant_coef[:, i])))

        # Get backward component
        wb = np.zeros(self.num_reactions)
        for i in range(self.num_reactions):
            if self.rev[i]:
                wb[i] = (self.kb[i] *
                         np.product(np.power(concs, self.product_coef[:, i])))

        # Total progress rate
        w = wf - wb
        return w

    def get_reaction_rate(self, concs):
        """Calculate reaction rate for a system of elementary reactions.

        INPUTS
        =======
        concs:          numpy array of floats
                        size: num_species
                        concentration of species

        RETURNS
        ========
        f:              numpy array of floats
                        size: num_species
                        reaction rate for each specie

        EXAMPLES
        =========
        >>> ReactionRate().read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0]))
        array([ -2.81180269e+08,  -2.85660407e+08,   5.66840676e+08,
                 4.48013835e+06,  -4.48013835e+06])

        """
        if self.rtype not in self.supported_rxn:
            raise NotImplementedError("{} is not implemented"
                                      .format(self.rtype))

        # Input values
        try:
            concs = np.array(concs)
        except:
            raise ValueError("Specie concentrations not in correct format.")
        if np.sum(concs < 0) != 0:
            raise ValueError("Specie concentrations cannot be negative.")

        # Get progress rate
        w = self.get_progress_rate(concs)

        # Reaction rates
        f = np.dot(self.nu_coef, w)

        return f
