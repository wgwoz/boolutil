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
    plaintext: str


class ExpressionOut(BaseModel):
    plaintext: str
    sympy_expr: str
    vars: List[str]
    ttable_readable: Optional[Tuple[List[List[int]], List[List[int]]]]


@app.post("/expression", response_model=ExpressionOut)
def create_expression(payload: ExpressionIn):
    """Create an Expression from plaintext and return a JSON-friendly representation.

    The returned object contains the original plaintext, a stringified sympy expression,
    list of variable names, and the truth-table readable tuple (minterms, dontcares) when available.
    """
    try:
        expr = Expression(plaintext=payload.plaintext)
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
