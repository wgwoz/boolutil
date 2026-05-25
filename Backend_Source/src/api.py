from typing import List, Optional, Tuple
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from .boollib import Expression
except ImportError:
    try:
        from boollib import Expression
    except Exception:
        from Boollib import Expression

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=["*"],
)

class ExpressionIn(BaseModel):
    plaintext: Optional[str] = None
    sympy_expr: Optional[str] = None
    vars: Optional[List[str]] = None
    ttable_readable: Optional[Tuple[List[List[int]], List[List[int]]]] = None  # Przywrócone List[List[int]]


class ExpressionOut(BaseModel):
    plaintext: str
    sympy_expr: str
    vars: List[str]
    ttable_readable: Optional[Tuple[List[List[int]], List[List[int]]]] = None  # Przywrócone List[List[int]]
    nand_sympy_expr: Optional[str] = None
@app.options("/expression")
def options_expression(response: Response):
    """Ręczne zezwolenie na zapytanie OPTIONS dla ścieżki tekstowej."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
@app.post("/expression", response_model=ExpressionOut)
def create_expression(payload: ExpressionIn):
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
    ttable = expr.ttable_readable if hasattr(expr, "ttable_readable") else None

    return ExpressionOut(
        plaintext=expr.plaintext,
        sympy_expr=sympy_str,
        vars=vars_list,
        ttable_readable=ttable,
    )

@app.post("/expression/nand", response_model=ExpressionOut)
def create_expression_nand(payload: ExpressionIn):
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
    ttable = expr.ttable_readable if hasattr(expr, "ttable_readable") else None
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