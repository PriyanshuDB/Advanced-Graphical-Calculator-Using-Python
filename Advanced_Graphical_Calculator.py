import tkinter as tk
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAggclass MyExpression:
    def __init__(self,expr):
        self.expr=sp.sympify(expr)
    def __add__(self,other):
        return MyExpression(self.expr+other.expr)
    def __sub__(self,other):
        return MyExpression(self.expr-other.expr)
    def __mul__(self,other):
        return MyExpression(self.expr*other.expr)
    def __truediv__(self,other):
        return MyExpression(self.expr/other.expr)
    def evaluate(self):
        return self.expr.evalf()
    def __str__(self):
        return str(self.expr)
class CustomButton(ttk.Button):
    def __init__(self,master,text,command,*args,**kwargs):
        super().__init__(master,text=text,*args,**kwargs)
        self.custom_command=command
        self.configure(command=self.on_click)
    def on_click(self):
        self.custom_command(self['text'])
class AdvancedCalculator:
    def __init__(self,master):
        self.master=master
        self.master.title("ADVANCED GRAPHICAL CALCULATOR")
        self.master.configure(bg="black")
        self.main_frame=ttk.Frame(self.master,padding="10")
        self.main_frame.grid(row=0,column=0,sticky="nsew")
        self.current_frame=None
        self.create_frames()
        self.create_entry()
        self.create_buttons()
        self.show_frame("normal")
        # Configure columns to expand equally
        self.main_frame.grid_columnconfigure((0,1,2,3),weight=1)
        self.adjust_window_size()
    def create_frames(self):
        self.frames={}
        for mode in ["normal","sci","trig","calc"]:
            frame=ttk.Frame(self.main_frame,padding="5")
            frame.grid_columnconfigure((0,1,2,3),weight=1)
            self.frames[mode]=frame
    def create_entry(self):
        self.entry_var=tk.StringVar()
        self.entry = ttk.Entry(self.main_frame, textvariable=self.entry_var, font=("default", 20), justify="right",width=30)
        self.entry.grid(row=0,column=0,columnspan=4,pady=10,padx=10,sticky="nsew")
    def create_buttons(self):
        button_config ={
            "normal":[
                ("NORM","SCI","TRIG","CALC"),
                ("AC","DEL","%","÷"),
                ("7","8","9","×"),
                ("4","5","6","-"),
                ("1","2","3","+"),
                ("j","0",".","=")
            ],
            "sci":[
                ("NORM","SCI","TRIG","CALC"),
                ("AC","DEL","(",")"),
                ("x²","x³","xⁿ","√"),
                ("ln","log₁₀","log₂","³√"),
                ("π","e","eⁿ","1/x")
            ],
            "trig":[
                ("NORM","SCI","TRIG","CALC"),
                ("AC","DEL","(", ")"),
                ("sin","cos","tan","sinh"),
                ("csc","sec","cot","cosh"),
                ("asin","acos","atan","tanh")
            ],
            "calc":[
                ("NORM","SCI","TRIG","CALC"),
                ("AC","DEL","2D","3D"),
                ("x","y","d/dx","d²/dx²"),
                ("d/dy","d²/dy²","∂/∂x","∂²/∂x²"),
                ("∂/∂y","∂²/∂y²","∫ dx","∫ dy")
            ]
        }
        style=ttk.Style()
        style.configure('TButton',font=('Arial',10))
        for mode, layout in button_config.items():
            for i, row in enumerate(layout):
                for j, text in enumerate(row):
                    btn=CustomButton(self.frames[mode],text=text,command=self.button_click,style='TButton')
                    btn.grid(row=i,column=j,sticky="nsew",padx=2,pady=2)
    def show_frame(self,mode):
        if self.current_frame:
            self.current_frame.grid_forget()
        self.frames[mode].grid(row=1,column=0,columnspan=4,sticky="nsew")
        self.current_frame=self.frames[mode]
        self.adjust_window_size()
    def button_click(self,key):
        if key in ["NORM","SCI","TRIG","CALC"]:
            mode_map = {"NORM":"normal","SCI":"sci","TRIG":"trig","CALC":"calc"}
            self.show_frame(mode_map[key])
        elif key=="=":
            self.calculate()
        elif key=="AC":
            self.entry_var.set("")
        elif key=="DEL":
            current=self.entry_var.get()
            self.entry_var.set(current[:-1])
        elif key in ["2D","3D"]:
            self.plot(key)
        else:
            current=self.entry_var.get()
            self.entry_var.set(current+key)
    def calculate(self):
        try:
            expr=self.entry_var.get()
            expr=expr.replace("×","*").replace("÷" "/").replace("^","**")
            expr = expr.replace("log₁₀","log10").replace("log₂","log2")
            expr = expr.replace("³√","cbrt").replace("√","sqrt")

            result=MyExpression(expr).evaluate()
            self.entry_var.set(str(result))
        except Exception as e:
            self.entry_var.set("Error")
            print(f"Calculation error:{e}")
    def plot(self,plot_type):
        try:
            expr=self.entry_var.get()
            x,y=sp.symbols('x y')
            if plot_type=="2D":
                self.plot_2d(MyExpression(expr).expr,x)
            elif plot_type=="3D":
                self.plot_3d(MyExpression(expr).expr,x,y)
        except Exception as e:
            print(f"Plotting error: {e}")
    def plot_2d(self,expr,x):
        fig,ax =plt.subplots()
        f=sp.lambdify(x,expr,'numpy')
        x_vals=np.linspace(-10,10,400)
        y_vals=f(x_vals)
        ax.plot(x_vals,y_vals)
        ax.set_title(f'2D Plot: {expr}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.show_plot(fig)
    def plot_3d(self,expr,x,y):
        fig=plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        f=sp.lambdify((x,y),expr,'numpy')
        x_vals=np.linspace(-10,10,50)
        y_vals=np.linspace(-10,10,50)
        x_vals,y_vals=np.meshgrid(x_vals,y_vals)
        z_vals=f(x_vals,y_vals)
        ax.plot_surface(x_vals,y_vals,z_vals,cmap='viridis')
        ax.set_title(f'3D Plot: {expr}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        self.show_plot(fig)
    def show_plot(self,fig):
        plot_window=tk.Toplevel(self.master)
        plot_window.title("Plot")
        canvas=FigureCanvasTkAgg(fig,master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
    def adjust_window_size(self):
        self.master.update_idletasks()
        self.master.geometry('')  # Reset the geometry
        self.master.geometry(f"{self.master.winfo_reqwidth()}x{self.master.winfo_reqheight()}")
def main():
    root=tk.Tk()
    app=AdvancedCalculator(root)
    root.mainloop()
if __name__=="__main__":
    main()
