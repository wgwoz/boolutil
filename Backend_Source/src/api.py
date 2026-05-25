from typing import List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    # Prefer a local relative import when running as a package.
    from .boollib import Expression
except ImportError:
    # Fallback for direct execution or case-insensitive filesystems.
    try:
        from boollib import Expression
    except Exception:
        from Boollib import Expression

app = FastAPI()


class ExpressionIn(BaseModel):
    plaintext: Optional[str] = None
    sympy_expr: Optional[str] = None
    vars: Optional[List[str]] = None
    ttable_readable: Optional[Tuple[List[List[int]], List[List[int]]]] = None


class ExpressionOut(BaseModel):
    plaintext: str
    sympy_expr: str
    vars: List[str]
    ttable_readable: Optional[Tuple[List[List[int]], List[List[int]]]] = None
    nand_sympy_expr: Optional[str] = None


@app.post("/expression", response_model=ExpressionOut)
def create_expression(payload: ExpressionIn):
    """Create an Expression from plaintext and return a JSON-friendly representation.

    The returned object contains the original plaintext, a stringified sympy expression,
    list of variable names, and the truth-table readable tuple (minterms, dontcares) when available.
    """
    # Build Expression using whichever input variant was provided
    try:
        if payload.plaintext is not None:
            expr = Expression(plaintext=payload.plaintext)
        elif payload.sympy_expr is not None:
            expr = Expression(sympy_expr=payload.sympy_expr)
        elif payload.ttable_readable is not None and payload.vars is not None:
            expr = Expression(ttable_readable=payload.ttable_readable, vars=payload.vars)
        else:
            raise ValueError("Provide one of: plaintext, sympy_expr, or ttable_readable with vars")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    sympy_str = str(expr.sympy_expr) if hasattr(expr, "sympy_expr") and expr.sympy_expr is not None else ""
    vars_list = [str(v) for v in expr.vars] if hasattr(expr, "vars") and expr.vars is not None else []
    ttable = None
    if hasattr(expr, "ttable_readable"):
        # might be None or a tuple
        ttable = expr.ttable_readable

    return ExpressionOut(
        plaintext=expr.plaintext,
        sympy_expr=sympy_str,
        vars=vars_list,
        ttable_readable=ttable,
    )



@app.post("/expression/nand", response_model=ExpressionOut)
def create_expression_nand(payload: ExpressionIn):
    """Create an Expression from plaintext, convert it to NAND-only form, and return JSON-friendly representation including the NAND form."""
    try:
        if payload.plaintext is not None:
            expr = Expression(plaintext=payload.plaintext)
        elif payload.sympy_expr is not None:
            expr = Expression(sympy_expr=payload.sympy_expr)
        elif payload.ttable_readable is not None and payload.vars is not None:
            expr = Expression(ttable_readable=payload.ttable_readable, vars=payload.vars)
        else:
            raise ValueError("Provide one of: plaintext, sympy_expr, or ttable_readable with vars")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        nand_result = expr.logic_to_nand_style()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NAND conversion failed: {e}")

    sympy_str = str(expr.sympy_expr) if hasattr(expr, "sympy_expr") and expr.sympy_expr is not None else ""
    vars_list = [str(v) for v in expr.vars] if hasattr(expr, "vars") and expr.vars is not None else []
    ttable = None
    if hasattr(expr, "ttable_readable"):
        ttable = expr.ttable_readable

    nand_str = str(nand_result) if nand_result is not None else (str(expr.Nand_form) if hasattr(expr, "Nand_form") else "")

    return ExpressionOut(
        plaintext=expr.plaintext,
        sympy_expr=sympy_str,
        vars=vars_list,
        ttable_readable=ttable,
        nand_sympy_expr=nand_str,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
