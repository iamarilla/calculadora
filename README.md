# Calculadora Científica

Calculadora científica de escritorio construida con Python y PyQt6.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green)

## Características

- Operaciones básicas: suma, resta, multiplicación, división
- Funciones científicas: sin, cos, tan, √, log, ln, x², ^
- Soporte para paréntesis con indicador de paréntesis sin cerrar
- Historial de operaciones con reutilización de resultados
- Modo DEG / RAD para funciones trigonométricas
- Tema claro y oscuro (Catppuccin)
- Soporte completo de teclado con navegación por cursor
- Ventana redimensionable

## Requisitos

```
python >= 3.10
python-pyqt6
```

En Arch / CachyOS:

```bash
sudo pacman -S python-pyqt6
```

## Uso

```bash
python main.py
```

## Estructura

```
calculadora/
├── main.py        # Punto de entrada
├── ventana.py     # Ventana principal y lógica de UI
├── evaluador.py   # Evaluación segura de expresiones matemáticas
├── historial.py   # Panel lateral de historial
├── temas.py       # Temas claro y oscuro
└── icono.py       # Generación programática del ícono
```
