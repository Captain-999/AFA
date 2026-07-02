import customtkinter as ctk

# ==============================
# Theme
# ==============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernCalculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Modern Calculator")
        self.geometry("360x520")
        self.resizable(False, False)
        self.configure(fg_color="#0f172a")

        self.new_input = False

        # ==============================
        # Display
        # ==============================
        self.display = ctk.CTkEntry(
            self,
            font=("Segoe UI", 36, "bold"),
            justify="right",
            height=80,
            border_width=0,
            fg_color="#1e293b",
            text_color="#f8fafc",
            corner_radius=15,
        )

        self.display.pack(padx=20, pady=(25, 15), fill="x")
        self.display.insert(0, "0")

        # ==============================
        # Grid Frame
        # ==============================
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        for i in range(4):
            self.grid_frame.columnconfigure(i, weight=1)

        for i in range(5):
            self.grid_frame.rowconfigure(i, weight=1)

        self.create_buttons()

        self.bind("<Key>", self.press_keyboard)

    # ==============================
    # Buttons
    # ==============================
    def create_buttons(self):

        buttons = [
            ("C",0,0,"#ef4444","#dc2626"),
            ("⌫",0,1,"#f59e0b","#d97706"),
            ("%",0,2,"#334155","#475569"),
            ("÷",0,3,"#3b82f6","#2563eb"),

            ("7",1,0,"#1e293b","#334155"),
            ("8",1,1,"#1e293b","#334155"),
            ("9",1,2,"#1e293b","#334155"),
            ("×",1,3,"#3b82f6","#2563eb"),

            ("4",2,0,"#1e293b","#334155"),
            ("5",2,1,"#1e293b","#334155"),
            ("6",2,2,"#1e293b","#334155"),
            ("-",2,3,"#3b82f6","#2563eb"),

            ("1",3,0,"#1e293b","#334155"),
            ("2",3,1,"#1e293b","#334155"),
            ("3",3,2,"#1e293b","#334155"),
            ("+",3,3,"#3b82f6","#2563eb"),

            ("0",4,0,"#1e293b","#334155"),
            (".",4,1,"#1e293b","#334155"),
            ("=",4,2,"#10b981","#059669"),
        ]

        for text,row,col,fg,hover in buttons:

            span = 2 if text == "=" else 1

            btn = ctk.CTkButton(
                self.grid_frame,
                text=text,
                font=("Segoe UI",20,"bold"),
                fg_color=fg,
                hover_color=hover,
                text_color="white",
                corner_radius=15,
                command=lambda t=text:self.button_click(t)
            )

            btn.grid(
                row=row,
                column=col,
                columnspan=span,
                padx=5,
                pady=5,
                sticky="nsew"
            )

    # ==============================
    # Button Click
    # ==============================
    def button_click(self, char):

        current = self.display.get()

        if char == "C":
            self.display.delete(0,"end")
            self.display.insert(0,"0")
            self.new_input = False
            return

        if char == "⌫":

            if self.new_input:
                return

            if len(current) <= 1:
                self.display.delete(0,"end")
                self.display.insert(0,"0")
            else:
                self.display.delete(len(current)-1,"end")

            return

        if char == "=":
            self.calculate()
            return

        if self.new_input:
            self.display.delete(0,"end")
            self.new_input = False

        if self.display.get() == "0":
            self.display.delete(0,"end")

        if char == "×":
            char="*"

        elif char == "÷":
            char="/"

        self.display.insert("end",char)

    # ==============================
    # Calculate
    # ==============================
    def calculate(self):

        expression = self.display.get()

        try:

            result = eval(expression)

            if isinstance(result,float):

                if result.is_integer():
                    result = int(result)

                else:
                    result = round(result,8)

            self.display.delete(0,"end")
            self.display.insert(0,str(result))

            self.new_input = True

        except:

            self.display.delete(0,"end")
            self.display.insert(0,"Error")

            self.new_input = True

    # ==============================
    # Keyboard
    # ==============================
    def press_keyboard(self,event):

        key = event.char

        if key in "0123456789.+-/*%":
            self.button_click(key)

        elif key == "\r":
            self.button_click("=")

        elif event.keysym == "Return":
            self.button_click("=")

        elif event.keysym == "BackSpace":
            self.button_click("⌫")

        elif event.keysym == "Escape":
            self.button_click("C")


# ==============================
# Run
# ==============================
if __name__ == "__main__":
    app = ModernCalculator()
    app.mainloop()