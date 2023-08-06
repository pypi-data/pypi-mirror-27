from tkinter import *
from tkinter import ttk


def main():

    class Calculator:

        calc_value = 0.0

        division_trigger = False
        multiplication_trigger = False
        addition_trigger = False
        subtraction_trigger = False

        def __init__(self, root):

            self.entry_value = StringVar(root, value="")

            root.title("Calculator")

            root.geometry("575x235")

            root.resizable(width=False, height=False)

            style = ttk.Style()
            style.configure("TButton", font="Serif 15", padding=10)
            style.configure("TEntry", font="Serif 18", padding=10)

            self.number_entry = ttk.Entry(root, textvariable=self.entry_value, width=70)
            self.number_entry.grid(row=0, columnspan=4)

            # 1st row

            self.button7 = ttk.Button(root, text="7", command=lambda: self.button_press("7")).grid(row=1, column=0)

            self.button8 = ttk.Button(root, text="8", command=lambda: self.button_press("8")).grid(row=1, column=1)

            self.button9 = ttk.Button(root, text="9", command=lambda: self.button_press("9")).grid(row=1, column=2)

            self.button_div = ttk.Button(root, text="/", command=lambda: self.math_button_press("/")).grid(row=1, column=3)

            # 2nd row

            self.button4 = ttk.Button(root, text="4", command=lambda: self.button_press("4")).grid(row=2, column=0)

            self.button5 = ttk.Button(root, text="5", command=lambda: self.button_press("5")).grid(row=2, column=1)

            self.button6 = ttk.Button(root, text="6", command=lambda: self.button_press("6")).grid(row=2, column=2)

            self.button_mult = ttk.Button(root, text="*", command=lambda: self.math_button_press("*")).grid(row=2, column=3)

            # 3rd row

            self.button1 = ttk.Button(root, text="1", command=lambda: self.button_press("1")).grid(row=3, column=0)

            self.button2 = ttk.Button(root, text="2", command=lambda: self.button_press("2")).grid(row=3, column=1)

            self.button3 = ttk.Button(root, text="3", command=lambda: self.button_press("3")).grid(row=3, column=2)

            self.button_add = ttk.Button(root, text="+", command=lambda: self.math_button_press("+")).grid(row=3, column=3)

            # 4th row

            self.button_clear = ttk.Button(root, text="AC", command=lambda: self.button_press("AC")).grid(row=4, column=0)

            self.button0 = ttk.Button(root, text="0", command=lambda: self.button_press("0")).grid(row=4, column=1)

            self.button_equal = ttk.Button(root, text="=", command=lambda: self.equal_button_press()).grid(row=4, column=2)

            self.button_sub = ttk.Button(root, text="-", command=lambda: self.math_button_press("-")).grid(row=4, column=3)

        def button_press(self, value):

            if self.is_float(value):

                entry_value = self.number_entry.get()

                entry_value += value

                self.number_entry.delete(0, "end")

                self.number_entry.insert(0, entry_value)

            else:

                self.number_entry.delete(0, "end")

        @staticmethod
        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        def math_button_press(self, value):

            if self.is_float(str(self.number_entry.get())):

                self.division_trigger = False
                self.multiplication_trigger = False
                self.addition_trigger = False
                self.subtraction_trigger = False

                self.calc_value = float(self.entry_value.get())

                if value == "/":
                    self.division_trigger = True

                elif value == "*":
                    self.multiplication_trigger = True

                elif value == "+":
                    self.addition_trigger = True

                else:
                    self.subtraction_trigger = True

                self.number_entry.delete(0, "end")

        def equal_button_press(self):
            if self.addition_trigger or self.subtraction_trigger or self.multiplication_trigger or self.division_trigger:

                if self.addition_trigger:
                    result = self.calc_value + float(self.entry_value.get())

                elif self.subtraction_trigger:
                    result = self.calc_value - float(self.entry_value.get())

                elif self.multiplication_trigger:
                    result = self.calc_value * float(self.entry_value.get())

                else:
                    try:
                        result = self.calc_value / float(self.entry_value.get())
                    except ZeroDivisionError:
                        result = "Zero division is not allowed"

                self.number_entry.delete(0, "end")
                self.number_entry.insert(0, result)

    root = Tk()

    calc = Calculator(root)

    root.mainloop()


if __name__ == '__main__':
    main()
