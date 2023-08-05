"""Test module for progress and reaction rate methods."""

import os
from flamespeed.test import env
from flamespeed import chemkin
import numpy as np

# =================
# TEST PARAM
# =================

def test_threebody_param():
    """Test progress rate values."""
    a = chemkin.ReactionRate()
    a.read_XML('./data/rxn_ThreeBody.xml', verify_integrity=True, convert_units=True)
    test = [[{'Type': 'Kooij', 'A': 38000000000.0, 'b': -2.0, 'E': 0.0, 'name': None}, 
            {'Type': 'efficiencies', 'H2': '2.5', 'H2O': '12.0', 'default': '1.0'}], 
            [{'Type': 'Kooij', 'A': 48000000000.0, 'b': -5.0, 'E': 4.1840000000000002, 'name': None}, 
            {'Type': 'efficiencies', 'H2': '2.5', 'H2O': '12.0', 'default': '1.0'}
            ]]
    assert (a.k_params_nonelementary == test)

def test_threebodytroe_param():
    """Test progress rate values."""
    a = chemkin.ReactionRate()
    a.read_XML('./data/rxn_TroeFalloffThreeBody.xml', verify_integrity=True, convert_units=True)    
    test = [[{'Type': 'Kooij', 'A': 636600000.0, 'b': -1.72, 'E': 2195.7631999999999, 'name': 'k0'}, 
                {'Type': 'Kooij', 'A': 1475000.0, 'b': 0.6, 'E': 0.0, 'name': None}, 
                {'Type': 'Troe', 'alpha': 0.8, 't1': 1e+30, 't2': 1e+30, 't3': 1e+30}, 
                {'Type': 'efficiencies', 'H2': '2.0', 'H2O': '11.0', 'O2': '0.78', 'default': '1.0'}
                ]]
    assert (a.k_params_nonelementary == test)

def test_duplicate_param():
    """Test progress rate values."""
    a = chemkin.ReactionRate()
    a.read_XML('./data/rxn_Duplicate.xml', verify_integrity=True, convert_units=True)
    test = [[{'Type': 'Arrhenius', 'A': 420000000.0, 'E': 50132.688000000002}, 
                {'Type': 'Arrhenius', 'A': 130000.0, 'E': -6816.9912000000004}]]
    assert (a.k_params_nonelementary == test)