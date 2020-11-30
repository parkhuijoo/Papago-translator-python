import sys
import requests
import apikey
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QTextEdit

class Translator(QWidget):

    def __init__(self):
        super().__init__()
        self.inputText = QTextEdit()
        self.translationButton = QPushButton('번역')
        self.clearButton = QPushButton('초기화')

        self.koToEn = QTextEdit()
        self.koToFr = QTextEdit()
        self.koToEs = QTextEdit()
        self.koToCn = QTextEdit()
        self.koToVi = QTextEdit()
        self.outputTextList = [self.koToEn, self.koToFr, self.koToEs, self.koToCn, self.koToVi]

        self.enToKo = QTextEdit()
        self.frToKo = QTextEdit()
        self.esToKo = QTextEdit()
        self.cnToKo = QTextEdit()
        self.viToKo = QTextEdit()
        self.verifyTextList = [self.enToKo, self.frToKo, self.esToKo, self.cnToKo, self.viToKo]
        self.initUI()

    def initUI(self):
        self.setLayout(
            self.setVLayout(
                self.setLogo('logo.png'),
                self.setHLayout(
                    self.setInputBox(self.inputText, self.translationButton, self.clearButton),
                    self.setOutputBox(self.outputTextList),
                    self.setOutputBox(self.verifyTextList)
                )
            )
        )

        self.translationButton.clicked.connect(self.translationClicked)
        self.clearButton.clicked.connect(self.clearClicked)

        self.setWindowTitle('Papago Translator')
        self.resize(1000, 700)
        self.show()

    def setLogo(self, logoPath):
        pixmap = QPixmap(logoPath)
        img = QLabel()
        img.setPixmap(pixmap)
        return img

    def setInputBox(self, inputText, translationButton, clearButton):
        inputLayout = QVBoxLayout()
        inputLayout.addWidget(inputText)
        buttons = QHBoxLayout()
        buttons.addWidget(translationButton)
        buttons.addWidget(clearButton)
        inputLayout.addLayout(buttons)
        return inputLayout

    def setOutputBox(self, outputTextList):
        outputLayout = QVBoxLayout()
        outputLayout.addWidget(outputTextList[0])
        outputLayout.addWidget(outputTextList[1])
        outputLayout.addWidget(outputTextList[2])
        outputLayout.addWidget(outputTextList[3])
        outputLayout.addWidget(outputTextList[4])
        return outputLayout

    def setVLayout(self, logo, hLayout):
        vLayout = QVBoxLayout()
        vLayout.addWidget(logo)
        vLayout.addLayout(hLayout)
        return vLayout

    def setHLayout(self, inputBox, fromEnBox, toEnBox):
        hLayout = QHBoxLayout()
        hLayout.addLayout(inputBox)
        hLayout.addLayout(fromEnBox)
        hLayout.addLayout(toEnBox)
        return hLayout

    def getDataFromPapago(self, departure, arrive, query):
        data = {'text': query,
                'source': departure,
                'target': arrive}
        header = {"X-Naver-Client-Id": apikey.client_id,
                  "X-Naver-Client-Secret": apikey.client_secret}
        url = "https://openapi.naver.com/v1/papago/n2mt"
        response = requests.post(url, headers=header, data=data)
        rescode = response.status_code
        if (rescode == 200):
            response_body = response.json()
            return response_body['message']['result']['translatedText']
        return 'error'

    def translationClicked(self):
        self.translate('ko', 'en', self.inputText, self.koToEn, '한국어 -> 영어')
        self.translate('en', 'ko', self.koToEn, self.enToKo, '영어 -> 한국어')
        self.translate('ko', 'fr', self.inputText, self.koToFr, '한국어 -> 프랑스어')
        self.translate('fr', 'ko', self.koToFr, self.frToKo, '프랑스어 -> 한국어')
        self.translate('ko', 'es', self.inputText, self.koToEs, '한국어 -> 스페인어')
        self.translate('es', 'ko', self.koToEs, self.esToKo, '스페인어 -> 한국어')
        self.translate('ko', 'zh-CN', self.inputText, self.koToCn, '한국어 -> 중국어')
        self.translate('zh-CN', 'ko', self.koToCn, self.cnToKo, '중국어 -> 한국어')
        self.translate('ko', 'vi', self.inputText, self.koToVi, '한국어 -> 베트남어')
        self.translate('vi', 'ko', self.koToVi, self.viToKo, '베트남어 -> 한국어')

    def translate(self, departure, arrive, inputBox, outputBox, hint=''):
        query = inputBox.toPlainText()
        if query == '':
            return
        split_query = query.split('\n')
        if '->' in split_query[0]:
            query = '\n'.join(split_query[1:])
        outputBox.setText('[' + hint + ']\n' + self.getDataFromPapago(departure, arrive, query))
        outputBox.repaint()

    def clearClicked(self):
        self.clear(self.inputText)
        self.clear(self.koToEn)
        self.clear(self.koToFr)
        self.clear(self.koToEs)
        self.clear(self.koToCn)
        self.clear(self.koToVi)
        self.clear(self.enToKo)
        self.clear(self.frToKo)
        self.clear(self.esToKo)
        self.clear(self.cnToKo)
        self.clear(self.viToKo)

    def clear(self, box):
        box.clear()
        box.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Translator()
    sys.exit(app.exec_())