"""Test module for progress and reaction rate methods."""

import os
from flamespeed.test import env
from flamespeed import chemkin
import numpy as np

# =================
# TEST PARAM
# =================

def test_instance():
    """Test progress rate values."""
    a = chemkin.ReactionRate()
    a.read_XML('./data/rxns_units.xml', verify_integrity=True, convert_units=True)
    test = "Number_of_reactions:3 \nNumber_of_species:6 \nNumber_of_reversible_reactions:0 \nReversible:No \nReaction_type:Elementary \nSpecies_list:['H', 'O', 'OH', 'H2', 'H2O', 'O2']\n"
    test = test.replace('\n', '').replace(' ', '')
    res = str(a).replace('\n', '').replace(' ', '')
    assert (res == test)
