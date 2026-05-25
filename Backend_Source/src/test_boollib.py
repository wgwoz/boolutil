import pytest
import sympy as sp
from sympy.logic.boolalg import And, Or, Not, Nand

try:
    from boollib import text_to_logic, logic_to_nand_style
except ImportError:
    from src.boollib import text_to_logic, logic_to_nand_style

# ==============================================================================
# SEKCJA 1: TESTY FUNKCJI text_to_logic()
# ==============================================================================

def test_text_to_logic_basic_and():
    """Test podstawowej koniunkcji (AND) dla różnych formatów zapisu."""
    expected = And(sp.Symbol('A'), sp.Symbol('B'))
    
    assert text_to_logic("A AND B") == expected
    assert text_to_logic("A * B") == expected
    assert text_to_logic("A n B") == expected
    assert text_to_logic("A & B") == expected
    
def test_text_to_logic_basic_or():
    """Test podstawowej alternatywy (OR) dla różnych formatów zapisu."""
    expected = Or(sp.Symbol('A'), sp.Symbol('B'))
    
    assert text_to_logic("A OR B") == expected
    assert text_to_logic("A + B") == expected
    assert text_to_logic("A v B") == expected
    assert text_to_logic("A u B") == expected
    assert text_to_logic("A | B") == expected

def test_text_to_logic_basic_not():
    """Test negacji (NOT) dla różnych formatów zapisu."""
    expected = Not(sp.Symbol('A'))
    
    assert text_to_logic("NOT A") == expected
    assert text_to_logic("!A") == expected
    assert text_to_logic("~A") == expected


def test_text_to_logic_basic_xor():
    """Test operacji XOR."""
    expected = sp.logic.boolalg.Xor(sp.Symbol('A'), sp.Symbol('B'))
    
    assert text_to_logic("A XOR B") == expected
