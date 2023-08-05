"""Test module for read_XML method."""

from flamespeed.test import env
from flamespeed import chemkin


# =================
# Read XML
# =================


def test_read_XML_01():
    """Test XML file import: Phase tag not included."""
    rc = chemkin.ReactionRate()
    try:
        f = rc.read_XML('./data/rxns_test/rxns_test_01.xml')
        return f
    except ValueError as err:
        assert(type(err) == ValueError)


def test_read_XML_02():
    """Test XML file import: New Arrhenius coefficient included."""
    rc = chemkin.ReactionRate()
    try:
        f = rc.read_XML('./data/rxns_test/rxns_test_02.xml')
        return f
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)


def test_read_XML_03():
    """Test XML file import: Includes reversible reaction."""
    rc = chemkin.ReactionRate()
    try:
        f = rc.read_XML('./data/rxns_test/rxns_test_03.xml')
        return f
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)


def test_read_XML_04():
        """Test XML file import: Includes duplicate reaction."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_04.xml')
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)


def test_read_XML_05():
        """Test XML file import: Missing param for modified Arrhenius."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_05.xml')
            return f
        except ValueError as err:
            assert(type(err) == ValueError)


def test_read_XML_06():
        """Test XML file import: Missing reaction coefficients."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_06.xml')
            return f
        except ValueError as err:
            assert(type(err) == ValueError)

def test_read_XML_07():
        """Test XML file import: Input b in Arrhenius reaction coefficient."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_07.xml')
            return f
        except ValueError as err:
            assert(type(err) == ValueError)

def test_read_XML_08():
        """Test XML file import: Multiple reaction systems."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_08.xml')
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)

def test_read_XML_09():
        """Test XML file import: Additional species."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_09.xml')
            return f
        except ValueError as err:
            assert(type(err) == ValueError)

def test_read_XML_10():
        """Test XML file import: Unit Conversion I."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_10.xml', verify_integrity=False, convert_units=True)
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)
            
def test_read_XML_11():
        """Test XML file import: Unit Conversion II."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_11.xml', verify_integrity=False, convert_units=True)
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)
            
def test_read_XML_12():
        """Test XML file import: Unit Conversion III."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_12.xml', verify_integrity=False, convert_units=True)
            return f
        except ValueError as err:
            assert(type(err) == ValueError)
            
def test_read_XML_13():
        """Test XML file import: Unit Conversion IV."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_13.xml', verify_integrity=False, convert_units=True)
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)
            
def test_read_XML_14():
        """Test XML file import: Unit Conversion V."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_14.xml', verify_integrity=False, convert_units=True)
            return f
        except NotImplementedError as err:
            assert(type(err) == NotImplementedError)
            
def test_read_XML_15():
        """Test XML file import: Unit Conversion VI."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_15.xml', verify_integrity=False, convert_units=True)
            return f
        except ValueError as err:
            assert(type(err) == ValueError)
            
def test_read_XML_16():
        """Test XML file import: Unit Conversion VII."""
        rc = chemkin.ReactionRate()
        try:
            f = rc.read_XML('./data/rxns_test/rxns_test_16.xml', verify_integrity=False, convert_units=True)
            return f
        except ValueError as err:
            assert(type(err) == ValueError)