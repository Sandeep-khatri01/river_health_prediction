import tkinter as tk
from tkinter import ttk, messagebox
from river_health_backend import best_model, X_columns, predict_do

class ModernRiverHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoStream: River Health Monitor")
        self.root.geometry("950x750")
        self.root.configure(bg="#f0f4f8")  # Soft light blue-gray background

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define Colors
        self.bg_color = "#f0f4f8"
        self.card_color = "#ffffff"
        self.primary_blue = "#2980b9"
        self.accent_blue = "#3498db"
        self.text_dark = "#2c3e50"

        # Labels for layout
        self.pollutants = ['O2', 'NH4', 'NO2', 'NO3', 'BOD5']
        self.days = [f"Day {i}" for i in range(1, 8)]
        self.entries = {}

        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = tk.Frame(self.root, bg=self.primary_blue, height=100)
        header_frame.pack(fill='x', side='top')
        
        title_lbl = tk.Label(
            header_frame, 
            text="🌊 EcoStream River Health", 
            font=('Segoe UI', 24, 'bold'), 
            bg=self.primary_blue, 
            fg="white",
            pady=20
        )
        title_lbl.pack()

        # Main Content Container
        container = tk.Frame(self.root, bg=self.bg_color, padx=40, pady=20)
        container.pack(fill='both', expand=True)

        # Input Card
        input_card = tk.LabelFrame(
            container, 
            text=" Sensor Readings (Last 7 Days) ", 
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_color, 
            fg=self.text_dark,
            padx=20, 
            pady=20,
            relief='flat',
            highlightbackground="#d1d8e0",
            highlightthickness=1
        )
        input_card.pack(fill='x')

        # Create Grid
        # Day Headers
        for col_idx, day in enumerate(self.days):
            lbl = tk.Label(input_card, text=day, font=('Segoe UI', 10, 'bold'), bg=self.card_color, fg=self.primary_blue)
            lbl.grid(row=0, column=col_idx + 1, padx=10, pady=10)

        # Pollutant Rows
        for row_idx, p in enumerate(self.pollutants):
            lbl = tk.Label(input_card, text=p, font=('Segoe UI', 11, 'bold'), bg=self.card_color, fg=self.text_dark)
            lbl.grid(row=row_idx + 1, column=0, padx=15, pady=8, sticky='e')

            for col_idx in range(1, 8):
                entry = tk.Entry(
                    input_card, 
                    width=8, 
                    font=('Segoe UI', 10), 
                    justify='center',
                    relief='solid',
                    highlightthickness=1,
                    highlightbackground="#ecf0f1",
                    bd=0
                )
                entry.grid(row=row_idx + 1, column=col_idx, padx=5, pady=8, ipady=3)
                self.entries[f"{p}_{col_idx}"] = entry

        # Action Area
        btn_frame = tk.Frame(container, bg=self.bg_color, pady=30)
        btn_frame.pack(fill='x')

        self.predict_btn = tk.Button(
            btn_frame, 
            text="ANALYZE RIVER HEALTH", 
            command=self.on_predict,
            bg=self.primary_blue, 
            fg='white', 
            font=('Segoe UI', 13, 'bold'),
            activebackground=self.accent_blue,
            activeforeground="white",
            relief='flat',
            cursor="hand2",
            padx=40,
            pady=12
        )
        self.predict_btn.pack()

        # Results Dashboard
        self.res_card = tk.Frame(
            container, 
            bg=self.card_color, 
            padx=30, 
            pady=25,
            highlightbackground="#d1d8e0",
            highlightthickness=1
        )
        self.res_card.pack(fill='x')
        self.res_card.pack_forget() # Hide initially

        self.do_val = tk.Label(self.res_card, text="", font=('Segoe UI', 16), bg=self.card_color, fg=self.text_dark)
        self.do_val.pack()

        self.status_lbl = tk.Label(self.res_card, text="", font=('Segoe UI', 22, 'bold'), bg=self.card_color)
        self.status_lbl.pack(pady=10)

    def on_predict(self):
        try:
            data = {}
            for key, entry in self.entries.items():
                val = entry.get()
                if not val:
                    messagebox.showwarning("Missing Data", f"Please fill in the value for {key}")
                    return
                data[key] = float(val)

            # Backend Logic
            do_pred, health = predict_do(data, best_model, X_columns)

            # Show and Update Result Card
            self.res_card.pack(fill='x', pady=10)
            self.do_val.config(text=f"Estimated Dissolved Oxygen Level: {do_pred:.2f} mg/L")
            self.status_lbl.config(text=f"Health Status: {health}")
            
            # Dynamic coloring based on health
            if "Excellent" in health or "Good" in health:
                self.status_lbl.config(fg="#27ae60")
            elif "Fair" in health:
                self.status_lbl.config(fg="#f39c12")
            else:
                self.status_lbl.config(fg="#e74c3c")

        except ValueError:
            messagebox.showerror("Format Error", "All sensor readings must be numerical values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRiverHealthApp(root)
    root.mainloop()
