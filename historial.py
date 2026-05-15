from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal


class PanelHistorial(QWidget):
    """Panel lateral que muestra el historial de operaciones.

    Emite `resultado_seleccionado(str)` cuando el usuario hace clic
    en una entrada para reutilizar su resultado.
    """

    resultado_seleccionado = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel_hist")
        self.setFixedWidth(200)
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(0)

        # Cabecera
        cabecera = QHBoxLayout()
        cabecera.setContentsMargins(12, 0, 12, 8)
        titulo = QLabel("Historial")
        titulo.setObjectName("titulo_hist")
        btn_borrar = QPushButton("Borrar")
        btn_borrar.setObjectName("btn_borrar")
        btn_borrar.setFlat(True)
        btn_borrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_borrar.clicked.connect(self.limpiar)
        cabecera.addWidget(titulo)
        cabecera.addStretch()
        cabecera.addWidget(btn_borrar)
        layout.addLayout(cabecera)

        sep = QFrame()
        sep.setObjectName("sep")
        sep.setFixedHeight(1)
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        self._lista = QListWidget()
        self._lista.setObjectName("lista_hist")
        self._lista.setCursor(Qt.CursorShape.PointingHandCursor)
        self._lista.itemClicked.connect(self._on_item_click)
        layout.addWidget(self._lista)

        hint = QLabel("↑ clic para reusar")
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

    def agregar(self, expresion: str, resultado) -> None:
        self._lista.insertItem(0, QListWidgetItem(f"  {expresion} = {resultado}"))

    def limpiar(self) -> None:
        self._lista.clear()

    def _on_item_click(self, item: QListWidgetItem) -> None:
        resultado = item.text().strip().split("=")[-1].strip()
        self._lista.clearSelection()
        self.resultado_seleccionado.emit(resultado)
