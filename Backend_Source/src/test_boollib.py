import pytest
import sympy as sp
from sympy.logic.boolalg import And, Or, Not, Nand

try:
    from boollib import text_to_logic, logic_to_nand_style
except ImportError:
    from src.boollib import text_to_logic, logic_to_nand_style
