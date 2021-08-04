from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit, 
                                QVBoxLayout, QWidget, QLineEdit, QFileDialog)
from PyQt5.QtCore import QProcess
import sys
from PyQt5 import QtCore
import os

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None
        self.flName = None
        self.fastq = None
        self.btn = QPushButton("Run")
        self.btn.pressed.connect(self.start_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.input_le = QLineEdit()
        self.input_btn = QPushButton("Select fastq file")
        self.input_btn.clicked.connect(self.select_input)

        l = QVBoxLayout()
        l.addWidget(self.input_le)
        l.addWidget(self.input_btn)
        l.addWidget(self.btn)
        l.addWidget(self.text)
        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)
    
    def select_input(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 
            "Open File", 
            QtCore.QDir.homePath()) 
        self.input_le.setText(fileName)
        self.flName = fileName
        print(self.flName)
        flName = str(self.flName)
        qq = r"copy {} .\\generic.fastq".format(flName)  
        qq = qq.replace(r"/", r"\\")
        print(qq)

        os.system(qq)
        #rint("copy {} ./test.fastq".format(flName))
        
    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            print(self.flName)
            naMe = self.flName
            #self.p.start("copy", [naMe, ".\generic.fastq"])
            self.p.start("python3", ['py_script.py'])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)
    def file_name():
        self.filename = self.input_le.text()
        
    def handle_state(self, state):
        states = {   
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None        
    def onInputFileButtonClicked(self):
        filename, filter = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.')

app = QApplication(sys.argv)
w = MainWindow()
w.show()

app.exec_()