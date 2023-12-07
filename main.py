import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, lambdify, sympify, S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class Calc(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', ')', '(',
            '**', 'x', '+', '=',
            'C', 'Graph'
        ]
        self.display = QLineEdit()
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(40)
        grid.addWidget(self.display, 0, 0, 1, 5)
        row, col = 1, 0
        for button in buttons:
            button_obj = QPushButton(button)
            grid.addWidget(button_obj, row, col, 1, 1)
            button_obj.clicked.connect(self.add_to_expression)
            if col < 4:
                col += 1
            else:
                col = 0
                row += 1
        self.setLayout(grid)
        self.setWindowTitle('Calculator Graph')

    def add_to_expression(self):
        sender = self.sender()
        self.display.setText(self.display.text() + sender.text())
        if sender.text() == '=':
            self.calculate()
        elif sender.text() == 'C':
            self.display.clear()
        elif sender.text() == 'Graph':
            self.graph_display()

    def calculate(self):
        try:
            x = symbols('x')
            str_expr = self.display.text().replace('=', '')
            expr = parse_expr(str_expr, transformations=(standard_transformations + (implicit_multiplication_application,)))
            if 'x' in str_expr:
                result = expr.evalf(subs={x:1})
            else:
                result = sympify(str_expr)
            self.display.setText(str(result))
        except ZeroDivisionError:
            self.display.setText("Error: Division by zero")
        except Exception as e:
            logging.error(str(e))
            self.display.setText("Calculation Error")

    def graph_display(self):
        try:
            x = symbols('x')
            str_expr = self.display.text()
            expr = parse_expr(str_expr, transformations=(standard_transformations + (implicit_multiplication_application,)))
            if 'x' in str_expr:
                f = lambdify(x, expr, "numpy")
                xs = np.linspace(-10, 10, 400)
                ys = np.empty_like(xs)
                for i, val in enumerate(xs):
                    try:
                        ys[i] = f(val)
                    except (TypeError, ValueError):
                        ys[i] = S.NaN
                plt.figure(figsize=(8, 6))
                plt.plot(xs, ys)
                plt.title(f"Graph of {str_expr}")
                plt.xlabel("x")
                plt.ylabel("y")
                plt.grid(True)
                plt.show()
            else:
                self.display.setText("Expression is not a function of 'x'")
        except Exception as e:
            logging.error(str(e))
            self.display.setText("Graph Error")

def main():
    app = QApplication(sys.argv)
    calc = Calc()
    calc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()