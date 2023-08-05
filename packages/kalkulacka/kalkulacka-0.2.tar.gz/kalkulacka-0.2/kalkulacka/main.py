from PyQt5 import QtWidgets, uic
import importlib_resources


def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QDialog()

    with importlib_resources.open('kalkulacka.resources', 'kalkulacka.ui') as f:
        uic.loadUi(f, window)

    window.show()

    sb_operand1 = window.findChild(QtWidgets.QDoubleSpinBox, 'sb_operand1')
    sb_operand2 = window.findChild(QtWidgets.QDoubleSpinBox, 'sb_operand2')
    cb_operator = window.findChild(QtWidgets.QComboBox, 'cb_operator')
    sb_result = window.findChild(QtWidgets.QDoubleSpinBox, 'sb_result')

    def calculate(new_value):
        op1 = sb_operand1.value()
        op2 = sb_operand2.value()
        operator = cb_operator.currentText()
        try:
            if operator == '+':
                result = op1 + op2
            elif operator == '-':
                result = op1 - op2
            elif operator == '×':
                result = op1 * op2
            elif operator == '÷':
                result = op1 / op2
            else:
                raise ValueError('bad operator')
        except Exception:
            sb_result.setPrefix('ERR! ')
            sb_result.setValue(0)
        else:
            sb_result.setPrefix('')
            sb_result.setValue(result)

    sb_operand1.valueChanged.connect(calculate)
    sb_operand2.valueChanged.connect(calculate)
    cb_operator.currentTextChanged.connect(calculate)

    return app.exec()
