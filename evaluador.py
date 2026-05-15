import math


def namespace(modo_grados: bool) -> dict:
    if modo_grados:
        sin_fn = lambda x: math.sin(math.radians(x))
        cos_fn = lambda x: math.cos(math.radians(x))
        tan_fn = lambda x: math.tan(math.radians(x))
    else:
        sin_fn, cos_fn, tan_fn = math.sin, math.cos, math.tan
    return {
        "__builtins__": {},
        "sin": sin_fn, "cos": cos_fn, "tan": tan_fn,
        "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
        "π": math.pi, "e": math.e, "abs": abs,
    }


def normalizar(expr: str) -> str:
    return (expr
            .replace("÷", "/")
            .replace("×", "*")
            .replace("−", "-")
            .replace("^", "**"))


def evaluar(expresion: str, modo_grados: bool):
    """Devuelve (resultado, None) o (None, mensaje_error)."""
    try:
        resultado = eval(normalizar(expresion), namespace(modo_grados))
        resultado = int(resultado) if resultado == int(resultado) else round(resultado, 10)
        return resultado, None
    except Exception as exc:
        return None, str(exc)
