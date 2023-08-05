"""Test module for progress and reaction rate methods."""

import os
from flamespeed.test import env
from flamespeed import chemkin
import numpy as np

# =================
# Progress rate
# =================

def test_progress_rate_01():
    """Test progress rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_progress_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0]))
    test1 = [2.811803e+08,   5.000000e+03,   4.485138e+06]

    np.testing.assert_allclose(rate, test1, 1e-06)


def test_progress_rate_02():
    """Test progress rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_reversible.xml').set_temp(750).get_progress_rate(np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]))
    test1 = [-6.878908e+16,  -5.886229e+11,   2.734270e+12,  -2.208086e+15,
              1.454757e+13,   6.751911e+13,   3.250000e+13,   3.129762e+13,
              1.275050e+13,   1.347004e+13,   2.842058e+12]

    np.testing.assert_allclose(rate, test1, 1e-06)

# test_progress_rate_02()
# =================
# Reaction rate
# =================


def test_reaction_rate_results_01():
    """Test reaction rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(750).get_reaction_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0]))
    test1 = np.array([-3608685.749817, -5615332.353438,  9224018.103256,  2006646.603621, -2006646.603621])
    np.testing.assert_allclose(rate, test1, 1e-06)


def test_reaction_rate_results_02():
    """Test reaction rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0]))
    test1 = np.array([ -2.811803e+08,  -2.856604e+08,   5.668407e+08,   4.480138e+06, -4.480138e+06])
    np.testing.assert_allclose(rate, test1, 1e-06)


def test_reaction_rate__results_03():
    """Test reaction rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([0, 0, 0, 0, 0]))
    test1 = np.array([0, 0, 0, 0, 0])
    np.testing.assert_allclose(rate, test1, 1e-06)


# =========================
# Reaction rate (reversible)
# =========================

def test_reaction_rate_reversible_results_01():
    """Test reaction rate values."""
    rc = chemkin.ReactionRate()
    rate = rc.read_XML('./data/rxns_reversible.xml').set_temp(750).get_reaction_rate(np.array([2.0, 1.0, 0.5, 1.0, 1.0, 1.5, 0.5, 1]))
    test1 = np.array([  3.421869e+16,  -3.381907e+16,  -3.528628e+16,   4.070991e+13,
                        5.865465e+14,   3.439104e+16,  -7.635885e+13,  -5.528322e+13] )
    np.testing.assert_allclose(rate, test1, 1e-06)

def test_reaction_rate_reversible_results_02():
    """Test reaction rate values."""
    rc = chemkin.ReactionRate()
    cwd = os.getcwd()
    print (cwd)
    rate = rc.read_XML('./data/rxns_reversible.xml').set_temp(1500).get_reaction_rate(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    test1 = np.array([ 0., 0., 0., 0., 0., 0., 0., 0.])
    np.testing.assert_allclose(rate, test1, 1e-06)

# =========================
# Reaction rate (input)
# =========================

def test_reaction_rate__input_01():
    """Test reaction rate input checks: Incorrect concentration array dimension."""
    rc = chemkin.ReactionRate()
    try:
        rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([0, 0, 0]))
        return rate
    except ValueError as err:
        assert(type(err) == ValueError)


def test_reaction_rate__input_02():
    """Test reaction rate input checks: Negative temperature."""
    rc = chemkin.ReactionRate()
    try:
        rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([1, 1, 1, 1, 1]))
        return rate
    except ValueError as err:
        assert(type(err) == ValueError)


def test_reaction_rate__input_03():
    """Test reaction rate input checks: Negative concentrations."""
    rc = chemkin.ReactionRate()
    try:
        rate = rc.read_XML('./data/rxns_hw5.xml').set_temp(1500).get_reaction_rate(np.array([-0.5, 1, 1, 1, 1]))
        return rate
    except ValueError as err:
        assert(type(err) == ValueError)

def test_reaction_rate__input_04():
    """Test reaction rate input checks: Negative concentrations."""
    rc = chemkin.ReactionRate()
    try:
        rate = rc.read_XML('./data/rxns_reversible.xml').set_temp(150).get_reaction_rate(np.array([-0.5, 1, 1, 1, 1]))
        return rate
    except ValueError as err:
        assert(type(err) == ValueError)
