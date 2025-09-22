import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro")
        self.setGeometry(400, 200, 350, 250)
        self.setWindowIcon(QIcon("recursos_de_imagenes/pomodoro-technique.ico"))

        # Valores por defecto (25 minutos de trabajo y 5 de descanso)
        self.trabajo = 25 * 60
        self.descanso = 5 * 60
        self.tiempo_restante = self.trabajo
        self.en_trabajo = True

        # === Widgets ===
        # Etiquetas (QLabel)
        self.label_estado = QLabel("Estado: Trabajo")
        self.label_tiempo = QLabel(self.formato_tiempo(self.tiempo_restante))
        self.label_tiempo.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Campos de entrada (QLineEdit) para personalizar tiempos
        self.input_trabajo = QLineEdit()
        self.input_trabajo.setPlaceholderText("Minutos de trabajo (ej. 25)")
        self.input_descanso = QLineEdit()
        self.input_descanso.setPlaceholderText("Minutos de descanso (ej. 5)")

        # Botones (QPushButton)
        self.btn_iniciar = QPushButton("Iniciar")
        self.btn_pausar = QPushButton("Pausar")
        self.btn_reiniciar = QPushButton("Reiniciar")
        self.btn_guardar = QPushButton("Guardar tiempos")

        # Layout principal (QVBoxLayout)
        layout = QVBoxLayout()
        layout.addWidget(self.label_estado)
        layout.addWidget(self.label_tiempo)
        layout.addWidget(self.input_trabajo)
        layout.addWidget(self.input_descanso)
        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_iniciar)
        layout.addWidget(self.btn_pausar)
        layout.addWidget(self.btn_reiniciar)
        self.setLayout(layout)

        # Timer (QTimer) para controlar la cuenta regresiva
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        # Conexiones de botones con sus funciones
        self.btn_iniciar.clicked.connect(self.iniciar)
        self.btn_pausar.clicked.connect(self.pausar)
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.btn_guardar.clicked.connect(self.guardar_tiempos)

    def formato_tiempo(self, segundos):
        """Convierte segundos a formato MM:SS"""
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02d}:{segundos:02d}"

    def actualizar_tiempo(self):
        """Disminuye el tiempo restante y cambia entre trabajo/descanso"""
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.setText(self.formato_tiempo(self.tiempo_restante))
        else:
            self.timer.stop()
            if self.en_trabajo:
                QMessageBox.information(self, "Descanso", "¡Tiempo de descanso!")
                self.tiempo_restante = self.descanso
                self.label_estado.setText("Estado: Descanso")
            else:
                QMessageBox.information(self, "Trabajo", "¡Hora de trabajar de nuevo!")
                self.tiempo_restante = self.trabajo
                self.label_estado.setText("Estado: Trabajo")
            self.en_trabajo = not self.en_trabajo
            self.iniciar()

    def iniciar(self):
        """Inicia el temporizador"""
        if not self.timer.isActive():
            self.timer.start(1000)  # cada segundo

    def pausar(self):
        """Pausa el temporizador"""
        if self.timer.isActive():
            self.timer.stop()

    def reiniciar(self):
        """Reinicia el ciclo Pomodoro con los valores actuales"""
        self.timer.stop()
        self.en_trabajo = True
        self.tiempo_restante = self.trabajo
        self.label_estado.setText("Estado: Trabajo")
        self.label_tiempo.setText(self.formato_tiempo(self.tiempo_restante))

    def guardar_tiempos(self):
        """Guarda los tiempos personalizados ingresados en QLineEdit"""
        try:
            trabajo_min = int(self.input_trabajo.text())
            descanso_min = int(self.input_descanso.text())
            self.trabajo = trabajo_min * 60
            self.descanso = descanso_min * 60
            self.reiniciar()
            QMessageBox.information(self, "Configuración", "Tiempos guardados correctamente.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa valores numéricos válidos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PomodoroApp()
    ventana.show()
    sys.exit(app.exec_())