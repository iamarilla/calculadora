#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication

from temas import TEMAS
from ventana import Calculadora


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(TEMAS["oscuro"])
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
