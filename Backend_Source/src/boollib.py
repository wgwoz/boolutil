import sympy as sp
from sympy.logic.boolalg import simplify_logic, And, Or, Not, Nand, truth_table
import re


class Expression:
    def __init__(self, plaintext = None, ttable_readable = None, sympy_expr = None, vars = None):
        '''
        Creates expression object and creates three basic representations to later be used to create different representations.
        self.plaintext: string written by user or generated from expression. 
        self.sympy_expr: sympy compatible expression, basic for operations
        self.vars: Sympy compatible list of variables
        self.ttable_readable: tuple of two lists, minterm indices and dontcare indices
        '''
        if plaintext is not None:
            self.plaintext = plaintext
            self.sympy_expr = self.text_to_logic(plaintext)
            self.vars = sorted(self.sympy_expr.atoms(sp.Symbol), key=lambda s: str(s))
            self.ttable_readable = self.get_minterms_and_dontcares(self.vars, self.sympy_expr)
            self.Nand_form = None
        elif sympy_expr is not None:
            self.sympy_expr = sympy_expr
            self.vars = sorted(self.sympy_expr.atoms(sp.Symbol), key=lambda s: str(s))
            self.plaintext = str(sympy_expr)
            self.ttable_readable = self.get_minterms_and_dontcares(self.vars, self.sympy_expr)
            self.Nand_form = None
        elif ttable_readable is not None and vars is not None:
            self.ttable_readable = ttable_readable
            self.vars = vars

            def row_to_index(row_bits):
                if isinstance(row_bits, (list, tuple)):
                    return int(''.join(str(int(b)) for b in row_bits), 2)
                return int(row_bits)

            minterms = [row_to_index(row) for row in ttable_readable[0]]
            dontcares = [row_to_index(row) for row in ttable_readable[1]]
            self.sympy_expr = sp.logic.boolalg.SOPform(vars, minterms, dontcares)
            self.plaintext = str(self.sympy_expr)
            self.Nand_form = None
        else:
            raise ValueError("Invalid input: Provide either plaintext, sympy_expr, or ttable_readable with vars.")
            
    def logic_to_nand_style(self):
        '''
        converts normal sympy expression to one in format, that only uses Nand and Not
        result is still numpy expressoin
        '''
        expr = self.sympy_expr

        def convert(e):
            # Atom (variable or constant)
            if getattr(e, "is_Atom", False):
                return e

            # NOT: ~A -> NAND(A, A)
            if isinstance(e, Not):
                child = convert(e.args[0])
                return Nand(child, child)

            # AND: A & B -> NAND(NAND(A,B), NAND(A,B))
            if isinstance(e, And):
                conv_args = [convert(a) for a in e.args]
                nand_all = Nand(*conv_args)
                return Nand(nand_all, nand_all)

            # OR: A | B -> NAND(NAND(A,A), NAND(B,B))  (generalized)
            if isinstance(e, Or):
                conv_args = [convert(a) for a in e.args]
                not_args = [Nand(a, a) for a in conv_args]
                return Nand(*not_args)

            # Fallback: try to recursively convert args and apply Nand on them
            if hasattr(e, "args") and e.args:
                conv_args = [convert(a) for a in e.args]
                return Nand(*conv_args)

            return e

        result = convert(expr)
        # store the converted form on the instance for later use
        self.Nand_form = result
        return result

    
    def get_minterms_and_dontcares(self, vars=None, expr=None):
        """
        Evaluates a sympy expression to find combination of variables that result in True (minterms) and None (don't cares).
        Returns a tuple of two lists: (minterms, dontcares). Accepts optional `vars` and `expr` to support external calls.
        """

        expr = expr if expr is not None else getattr(self, "sympy_expr", None)
        vars = vars if vars is not None else getattr(self, "vars", None)

        if expr is None or vars is None:
            raise ValueError("Expression and vars must be provided to evaluate truth table")

        # Debug: print types
        # Create a truth table: returns rows as bit-vectors paired with output values.
        table = list(truth_table(expr, list(vars)))

        def row_to_list(row_bits):
            if isinstance(row_bits, (list, tuple)):
                return [int(b) for b in row_bits]
            return [int(row_bits)]

        minterms = [row_to_list(row) for row, value in table if value == True]
        dontcares = [row_to_list(row) for row, value in table if value is None]

        self.ttable_readable = (minterms, dontcares)
        return self.ttable_readable



    def text_to_logic(self, plaintext=None):

        """
        onverts plaintext logic expressions into a format that can be processed by sympy, and extracts symbols as sympy Symbols.

        Inputs:
        - plaintext_expression: A string containing the logic expression in plaintext format.
        - Allowed symbols for logic operations include:
            - OR: +, v, u, OR, |
            - AND: *, n, AND, & 
            - NOT: !, NOT, ~
            - True: 1, True (trailing 1 will be treated as a symbol unsless explicid logic operator is used before it)
            - False: 0, False (trailing 1 will be treated as a symbol unsless explicid logic operator is used before it)
        -Allowed variable names:
            - 1 large or small letter followed by any amount of numbers
            - expection, names starting with v, u, n ;
             and logic operaotrs
        Outputs:
        - processed: A string with the logic expression converted to sympy format.
        """

        plaintext_expression = plaintext if plaintext is not None else getattr(self, "plaintext", None)
        if plaintext_expression is None:
            raise ValueError("No plaintext expression provided to text_to_logic")
        # Change different logic symbols to format accepted by sympy
        substitutions = {
            '+': '|',
            'v': '|',
            'u': '|',
            'OR': '|',
            '*': '&',
            'n': '&',
            'AND': '&',
            '!': '~',
            'NOT': '~',
            'XOR': '^'
        }

        processed = plaintext_expression
        for old, new in substitutions.items():
            processed = processed.replace(old, new)


        # Pre process leading 1 and 0 to custom tags to later change to True and False
        # If changed right to True and False, it would treat each letter as a symbol

        processed = re.sub(r'\b1', ' T213769 &', processed)
        processed = re.sub(r'\b0', ' F213769 &', processed)

        # Split symbols directly next to each other and add an implicit AND between them
        processed = re.sub(r'([a-zA-Z0-9])(?=[a-zA-Z(~])', r'\1 & ', processed)
        #Handle parentheses
        processed = re.sub(r'\)(?=\s*[a-zA-Z0-9])', r') & ', processed)
        processed = re.sub(r'\)(?=\s*\()', r') & ', processed)

        # Replace the custom tags with True and False
        processed = re.sub(r'\bT213769\b', 'True ', processed)
        processed = re.sub(r'\bF213769\b', 'False ', processed)

        # Handle double and trailing operators
        processed = re.sub(r'&&', '&', processed)
        processed = re.sub(r'&\|', '|', processed)
        processed = processed.strip().rstrip('&|').strip()


        # Detect symbols (variables) in the processed expression
        symbols_found = set(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', processed))
        keywords = {'AND', 'OR', 'NOT', 'XOR', 'v', 'True', 'False'}
        symbols_found = {s for s in symbols_found if s not in keywords}
        sym_dict = {s: sp.Symbol(s) for s in symbols_found}

        sympy_expr = sp.sympify(processed, locals=sym_dict)

        self.sympy_expr = sympy_expr
        return sympy_expr
   

if __name__ == "__main__":

    while True:
        test_input = input("Enter equation (or 'stop' to exit): ")
        if test_input == "stop":
            break
        processed = text_to_logic(test_input)
        a = Expression(plaintext=test_input)
        print(a.ttable_readable)


        print(f"Processed: {processed}")
        processed = simplify_expression(processed)
        print(f"Simplified: {processed}")
        processed = logic_to_nand_style(processed)
        print(f"Nandified: {processed}")