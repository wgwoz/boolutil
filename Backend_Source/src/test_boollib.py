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
    
