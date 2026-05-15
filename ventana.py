from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame, QLineEdit, QSizePolicy,
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent, QFont

from evaluador import evaluar
from historial import PanelHistorial
from icono import crear_icono
from temas import TEMAS


class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setWindowIcon(crear_icono())
        self.setMinimumSize(560, 520)

        self.expresion = ""
        self.modo_grados = True
        self.tema = "oscuro"
        self.sci_visible = True

        self._construir_ui()

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Panel historial
        self.historial = PanelHistorial()
        self.historial.resultado_seleccionado.connect(self._cargar_resultado)
        root.addWidget(self.historial)

        # Panel calculadora
        panel = QWidget()
        col = QVBoxLayout(panel)
        col.setContentsMargins(16, 12, 16, 16)
        col.setSpacing(5)

        # Indicador de paréntesis / historial
        self.lbl_histlinea = QLabel("")
        self.lbl_histlinea.setObjectName("lbl_histlinea")
        self.lbl_histlinea.setAlignment(Qt.AlignmentFlag.AlignRight)
        col.addWidget(self.lbl_histlinea)

        # Display
        self.lbl_display = QLineEdit("0")
        self.lbl_display.setObjectName("lbl_display")
        self.lbl_display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_display.setMinimumHeight(54)
        self.lbl_display.setFrame(False)
        self.lbl_display.setFont(QFont("SF Pro Display", 36, QFont.Weight.Bold))
        self.lbl_display.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.lbl_display.installEventFilter(self)
        col.addWidget(self.lbl_display)

        # Fila de controles: tema + DEG/RAD
        ctrl = QHBoxLayout()
        ctrl.setContentsMargins(0, 0, 0, 0)
        ctrl.setSpacing(6)
        self.btn_tema = self._ctrl_btn("☀", "btn_tema", self._toggle_tema)
        self.btn_modo = self._ctrl_btn("DEG", "btn_modo", self._toggle_modo)
        ctrl.addStretch()
        ctrl.addWidget(self.btn_tema)
        ctrl.addWidget(self.btn_modo)
        col.addLayout(ctrl)

        # ── Panel científico (colapsable) ──────────────────────────────────────
        self.panel_sci = QWidget()
        sci_layout = QVBoxLayout(self.panel_sci)
        sci_layout.setContentsMargins(0, 0, 0, 0)
        sci_layout.setSpacing(5)

        for fila in [
            [("sin","btn_sci"),("cos","btn_sci"),("tan","btn_sci"),("x²","btn_sci"),("√","btn_sci")],
            [("log","btn_sci"),("ln","btn_sci"), ("π","btn_sci"), ("e","btn_sci"), ("^","btn_sci")],
        ]:
            hl = QHBoxLayout()
            hl.setSpacing(4)
            for txt, cls in fila:
                b = QPushButton(txt)
                b.setProperty("class", cls)
                b.setStyle(b.style())
                b.setMinimumHeight(40)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                b.clicked.connect(lambda _, t=txt: self._pulsar(t))
                hl.addWidget(b)
            sci_layout.addLayout(hl)

        sep_sci = QFrame()
        sep_sci.setObjectName("sep2")
        sep_sci.setFrameShape(QFrame.Shape.HLine)
        sep_sci.setFixedHeight(1)
        sci_layout.addWidget(sep_sci)

        col.addWidget(self.panel_sci)

        # ── Botones principales ────────────────────────────────────────────────
        #
        # Fila 0:  C    ⌫    %   SCI▲
        # Fila 1:  (    )    ±    ÷
        # Fila 2:  7    8    9    ×
        # Fila 3:  4    5    6    −
        # Fila 4:  1    2    3    +
        # Fila 5:  [0   ]   .    =

        grid = QGridLayout()
        grid.setSpacing(6)
        for c in range(4):
            grid.setColumnStretch(c, 1)
        for r in range(6):
            grid.setRowStretch(r, 1)

        # Fila 0: C, ⌫, %, SCI▲
        grid.addWidget(self._make_btn("C",  "btn_clear"), 0, 0)
        grid.addWidget(self._make_btn("⌫", "btn_back"),  0, 1)
        grid.addWidget(self._make_btn("%",  "btn_func"),  0, 2)
        self.btn_sci_toggle = self._make_btn("SCI ▲", "btn_func",
                                              callback=self._toggle_sci)
        grid.addWidget(self.btn_sci_toggle, 0, 3)

        # Filas 1–4: numéricos + operadores (col 3 sube una fila)
        for ri, fila in enumerate([
            [("(","btn_paren"),(")",  "btn_paren"),("±","btn_func"),("÷","btn_op")],
            [("7","btn_num"),  ("8",  "btn_num"),  ("9","btn_num"), ("×","btn_op")],
            [("4","btn_num"),  ("5",  "btn_num"),  ("6","btn_num"), ("−","btn_op")],
            [("1","btn_num"),  ("2",  "btn_num"),  ("3","btn_num"), ("+","btn_op")],
        ], start=1):
            for ci, (t, c) in enumerate(fila):
                grid.addWidget(self._make_btn(t, c), ri, ci)

        # Fila 5: 0 (doble ancho), ., =
        grid.addWidget(self._make_btn("0", "btn_num"),   5, 0, 1, 2)
        grid.addWidget(self._make_btn(".", "btn_num"),   5, 2)
        grid.addWidget(self._make_btn("=", "btn_igual"), 5, 3)

        col.addLayout(grid)

        root.addWidget(panel)
        self.lbl_display.setFocus()

    # ── Helpers de botones ─────────────────────────────────────────────────────

    def _ctrl_btn(self, texto, clase, callback):
        btn = QPushButton(texto)
        btn.setProperty("class", clase)
        btn.setStyle(btn.style())
        btn.setFixedHeight(26)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(callback)
        return btn

    def _make_btn(self, texto, clase, callback=None):
        btn = QPushButton(texto)
        btn.setProperty("class", clase)
        btn.setStyle(btn.style())
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cb = callback if callback else (lambda _, t=texto: self._pulsar(t))
        btn.clicked.connect(cb)
        return btn

    # ── Display ────────────────────────────────────────────────────────────────

    def _actualizar_display(self, texto: str, cursor_pos: int | None = None):
        n = len(texto)
        size = 18 if n > 14 else 26 if n > 10 else 36
        self.lbl_display.setFont(QFont("SF Pro Display", size, QFont.Weight.Bold))
        self.lbl_display.setText(texto)
        self.lbl_display.setCursorPosition(
            cursor_pos if cursor_pos is not None else len(texto))

    def _cursor(self) -> int:
        return min(self.lbl_display.cursorPosition(), len(self.expresion))

    def _cargar_resultado(self, resultado: str):
        self.expresion = resultado
        self._actualizar_display(resultado)
        self.lbl_display.setFocus()

    # ── Inserción en el cursor ─────────────────────────────────────────────────

    def _insertar(self, texto: str):
        if self.lbl_display.text() in ("0", "Error"):
            self.expresion = ""
        pos = self._cursor()
        self.expresion = self.expresion[:pos] + texto + self.expresion[pos:]
        self._actualizar_display(self.expresion, pos + len(texto))

    def _insertar_funcion(self, nombre: str):
        if self.lbl_display.text() == "Error":
            self.expresion = ""
        pos = self._cursor()
        prefix = "×" if pos > 0 and self.expresion[pos - 1] in "0123456789)π" else ""
        ins = prefix + nombre + "("
        self.expresion = self.expresion[:pos] + ins + self.expresion[pos:]
        self._actualizar_display(self.expresion, pos + len(ins))
        self._actualizar_indicador()

    # ── Paréntesis ─────────────────────────────────────────────────────────────

    def _parentesis_abiertos(self) -> int:
        return self.expresion.count("(") - self.expresion.count(")")

    def _actualizar_indicador(self):
        n = self._parentesis_abiertos()
        if n > 0:
            self.lbl_histlinea.setText(f"{'(' * n}  ←sin cerrar")
        elif self.lbl_histlinea.text().endswith("←sin cerrar"):
            self.lbl_histlinea.setText("")

    # ── Toggles ────────────────────────────────────────────────────────────────

    def _toggle_modo(self):
        self.modo_grados = not self.modo_grados
        self.btn_modo.setText("DEG" if self.modo_grados else "RAD")
        self.lbl_display.setFocus()

    def _toggle_tema(self):
        self.tema = "claro" if self.tema == "oscuro" else "oscuro"
        self.btn_tema.setText("☀" if self.tema == "oscuro" else "☾")
        QApplication.instance().setStyleSheet(TEMAS[self.tema])
        self.lbl_display.setFocus()

    def _toggle_sci(self):
        self.sci_visible = not self.sci_visible
        self.panel_sci.setVisible(self.sci_visible)
        self.btn_sci_toggle.setText("SCI ▲" if self.sci_visible else "SCI ▼")
        self.lbl_display.setFocus()

    # ── Lógica de cada botón ───────────────────────────────────────────────────

    def _pulsar(self, tecla: str):
        if tecla in ("sin", "cos", "tan", "log", "ln"):
            self._insertar_funcion(tecla)

        elif tecla == "√":
            self._insertar_funcion("sqrt")

        elif tecla == "x²":
            if self.expresion:
                self.expresion = f"({self.expresion})^2"
                self._actualizar_display(self.expresion)

        elif tecla in ("π", "e"):
            if self.lbl_display.text() == "Error":
                self.expresion = ""
            pos = self._cursor()
            prefix = "×" if pos > 0 and self.expresion[pos - 1] in "0123456789)" else ""
            ins = prefix + tecla
            self.expresion = self.expresion[:pos] + ins + self.expresion[pos:]
            self._actualizar_display(self.expresion, pos + len(ins))

        elif tecla == "^":
            if self.expresion:
                pos = self._cursor()
                self.expresion = self.expresion[:pos] + "^" + self.expresion[pos:]
                self._actualizar_display(self.expresion, pos + 1)

        elif tecla == "C":
            self.expresion = ""
            self._actualizar_display("0")
            self.lbl_histlinea.setText("")

        elif tecla == "⌫":
            pos = self._cursor()
            if pos > 0:
                self.expresion = self.expresion[:pos - 1] + self.expresion[pos:]
                self._actualizar_display(
                    self.expresion if self.expresion else "0",
                    max(0, pos - 1) if self.expresion else 0,
                )
                self._actualizar_indicador()

        elif tecla == "(":
            if self.lbl_display.text() == "Error":
                self.expresion = ""
            pos = self._cursor()
            prefix = "×" if pos > 0 and self.expresion[pos - 1] in "0123456789)π" else ""
            ins = prefix + "("
            self.expresion = self.expresion[:pos] + ins + self.expresion[pos:]
            self._actualizar_display(self.expresion, pos + len(ins))
            self._actualizar_indicador()

        elif tecla == ")":
            pos = self._cursor()
            antes = self.expresion[:pos]
            if antes.count("(") - antes.count(")") > 0:
                self.expresion = self.expresion[:pos] + ")" + self.expresion[pos:]
                self._actualizar_display(self.expresion, pos + 1)
                self._actualizar_indicador()

        elif tecla == "=":
            cerrada = self.expresion + ")" * self._parentesis_abiertos()
            res, err = evaluar(cerrada, self.modo_grados)
            if err:
                self._actualizar_display("Error")
                self.expresion = ""
            else:
                self.lbl_histlinea.setText(cerrada + " =")
                self.historial.agregar(cerrada, res)
                self.expresion = str(res)
                self._actualizar_display(self.expresion)

        elif tecla == "±":
            res, err = evaluar(self.expresion, self.modo_grados)
            if not err:
                val = -float(res)
                self.expresion = str(int(val) if val == int(val) else val)
                self._actualizar_display(self.expresion)

        elif tecla == "%":
            res, err = evaluar(self.expresion, self.modo_grados)
            if not err:
                val = float(res) / 100
                self.expresion = str(int(val) if val == int(val) else val)
                self._actualizar_display(self.expresion)

        else:
            self._insertar(tecla)

        self.lbl_display.setFocus()

    # ── Teclado ────────────────────────────────────────────────────────────────

    def eventFilter(self, obj, event):
        if obj is self.lbl_display and event.type() == QEvent.Type.KeyPress:
            if (event.key() == Qt.Key.Key_C and
                    event.modifiers() == Qt.KeyboardModifier.ControlModifier):
                return False
            self.keyPressEvent(event)
            return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event: QKeyEvent):
        nav = {
            Qt.Key.Key_Left:  lambda: self.lbl_display.setCursorPosition(
                max(0, self.lbl_display.cursorPosition() - 1)),
            Qt.Key.Key_Right: lambda: self.lbl_display.setCursorPosition(
                min(len(self.expresion), self.lbl_display.cursorPosition() + 1)),
            Qt.Key.Key_Home:  lambda: self.lbl_display.setCursorPosition(0),
            Qt.Key.Key_End:   lambda: self.lbl_display.setCursorPosition(len(self.expresion)),
        }
        if event.key() in nav:
            nav[event.key()]()
            return

        mapa = {
            Qt.Key.Key_0: "0", Qt.Key.Key_1: "1", Qt.Key.Key_2: "2",
            Qt.Key.Key_3: "3", Qt.Key.Key_4: "4", Qt.Key.Key_5: "5",
            Qt.Key.Key_6: "6", Qt.Key.Key_7: "7", Qt.Key.Key_8: "8",
            Qt.Key.Key_9: "9", Qt.Key.Key_Period: ".",
            Qt.Key.Key_Plus: "+",      Qt.Key.Key_Minus: "−",
            Qt.Key.Key_Asterisk: "×",  Qt.Key.Key_Slash: "÷",
            Qt.Key.Key_Percent: "%",   Qt.Key.Key_AsciiCircum: "^",
            Qt.Key.Key_ParenLeft: "(", Qt.Key.Key_ParenRight: ")",
            Qt.Key.Key_Return: "=",    Qt.Key.Key_Enter: "=",
            Qt.Key.Key_Backspace: "⌫", Qt.Key.Key_Escape: "C",
            Qt.Key.Key_Delete: "C",
        }
        tecla = mapa.get(event.key())
        if tecla:
            self._pulsar(tecla)
            self._animar_boton(tecla)
        else:
            super().keyPressEvent(event)

    def _animar_boton(self, tecla: str):
        for btn in self.findChildren(QPushButton):
            if btn.text() == tecla:
                btn.setDown(True)
                btn.repaint()
                QApplication.processEvents()
                btn.setDown(False)
                break
