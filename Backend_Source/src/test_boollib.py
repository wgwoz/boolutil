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

def test_text_to_logic_complex_expression():
    """Test złożonego wyrażenia logicznego z nawiasami i priorytetami operatorów."""
    expr1 = "A AND (B OR NOT C)"
    expr2 = "A * (B + !C)"
    
    A, B, C = sp.symbols('A B C')
    expected = And(A, Or(B, Not(C)))
    
    assert text_to_logic(expr1) == expected
    assert text_to_logic(expr2) == expected

def test_text_to_logic_variable_naming():
    """Test akceptacji poprawnych nazw zmiennych (litera + liczby)."""
    expr = "A1 AND b123"
    expected = And(sp.Symbol('A1'), sp.Symbol('b123'))
    assert text_to_logic(expr) == expected


def test_text_to_logic_whitespace_handling():
    """Test odporności parsera na nieregularne odstępy i tabulacje."""
    expr = "  A    AND\tB  "
    expected = And(sp.Symbol('A'), sp.Symbol('B'))
    assert text_to_logic(expr) == expected

# ==============================================================================
# SEKCJA 2: TESTY FUNKCJI logic_to_nand_style()
# ==============================================================================

def test_logic_to_nand_style_atom():
    """Baza rekurencji: pojedyncza zmienna powinna zostać niezmieniona."""
    A = sp.Symbol('A')
    assert logic_to_nand_style(A) == A


def test_logic_to_nand_style_double_negation():
    """Test eliminacji podwójnej negacji: ~(~A) powinno uprościć się do A."""
    A = sp.Symbol('A')
    double_not = Not(Not(A))
    assert logic_to_nand_style(double_not) == A
