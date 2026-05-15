from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QColor, QIcon, QPixmap


def _dibujar(p: QPainter, scale: float) -> None:
    """Dibuja la calculadora en el QPainter dado a la escala indicada."""

    def r(x, y, w, h, rx=0):
        p.drawRoundedRect(
            int(x * scale), int(y * scale),
            int(w * scale), int(h * scale),
            rx * scale, rx * scale,
        )

    p.setPen(Qt.PenStyle.NoPen)

    # Cuerpo gris oscuro
    p.setBrush(QBrush(QColor("#546e7a")))
    r(0, 0, 64, 64, 12)

    # Display LCD oscuro
    p.setBrush(QBrush(QColor("#1b2a1b")))
    r(5, 6, 54, 14, 4)

    # Dígitos LCD (verde)
    p.setBrush(QBrush(QColor("#00e676")))
    r(29, 9, 26, 4, 1)
    r(29, 14, 26, 3, 1)

    # Cuadrícula de botones
    BW, BH, GX, GY, SX, SY = 12, 7, 3, 3, 5, 25
    filas = [
        ["#ef5350", "#b0bec5", "#b0bec5", "#ff9800"],  # C, ±, %, ÷
        ["#eceff1", "#eceff1", "#eceff1", "#ff9800"],  # 7,8,9,×
        ["#eceff1", "#eceff1", "#eceff1", "#ff9800"],  # 4,5,6,−
    ]
    for ri, fila in enumerate(filas):
        y = SY + ri * (BH + GY)
        for ci, color in enumerate(fila):
            p.setBrush(QBrush(QColor(color)))
            r(SX + ci * (BW + GX), y, BW, BH, 2)

    # Última fila: 0 ancho + . + =
    y = SY + 3 * (BH + GY)
    p.setBrush(QBrush(QColor("#eceff1")))
    r(SX,                    y, BW * 2 + GX, BH, 2)
    r(SX + BW * 2 + GX * 2, y, BW,           BH, 2)
    p.setBrush(QBrush(QColor("#00c853")))
    r(SX + BW * 3 + GX * 3, y, BW,           BH, 2)


def crear_icono(size: int = 64) -> QIcon:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    _dibujar(p, size / 64)
    p.end()
    return QIcon(pix)


def guardar_png(ruta: str, size: int = 256) -> None:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    _dibujar(p, size / 64)
    p.end()
    pix.save(ruta)
