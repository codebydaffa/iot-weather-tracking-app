import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from calculate_mse import mse, forecast_temp, actual_temp, forecast_wind, actual_wind
import sys

# Define modern, aesthetic dark theme color palette
current_theme = "dark"

# Returns a dictionary of colors for the selected theme
def get_theme_colors():
    return {
        "bg": "#121212",             # Main background
        "fg": "#FFFFFF",             # Text color
        "frame_bg": "#1E1E2F",       # Plot background
        "label_fg": "#E0E0E0",       # Label text
        "grid_color": "#333A44"      # Grid lines
    }

# Creates temperature and wind plots, embedded in the GUI
# Includes zoom and reset interactions using mouse and keyboard

def plot_weather(parent_frame):
    # Load data and label the columns
    df = pd.read_csv("weather_data.csv", header=None, names=[
        "Timestamp", "Forecast_Temp", "Actual_Temp", "Forecast_Wind", "Actual_Wind"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    plt.style.use('default')
    theme = get_theme_colors()

    # Create figure with 2 vertically stacked plots
    fig, axs = plt.subplots(2, 1, figsize=(20, 6.5), sharex=True, gridspec_kw={'hspace': 0.25})
    fig.patch.set_facecolor(theme["bg"])
    axs[0].set_facecolor(theme["frame_bg"])
    axs[1].set_facecolor(theme["frame_bg"])

    # Format x-axis as date and time
    axs[1].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    axs[1].tick_params(axis='x', labelrotation=60, labelsize=7, colors=theme["label_fg"])
    axs[0].tick_params(axis='y', labelsize=9, colors=theme["label_fg"])
    axs[1].tick_params(axis='y', labelsize=9, colors=theme["label_fg"])

    # Plot temperature data
    axs[0].plot(df["Timestamp"], df["Forecast_Temp"], label="Forecast Temp (°C)",
                color='#4FC3F7', marker='o', markersize=3, linewidth=1)
    axs[0].plot(df["Timestamp"], df["Actual_Temp"], label="Actual Temp (°C)",
                color='#FFA726', marker='x', markersize=4, linewidth=1)
    axs[0].set_title("Temperature Over Time", fontsize=12, color=theme["label_fg"])
    axs[0].set_ylabel("Temperature (°C)", fontsize=10, color=theme["label_fg"])
    axs[0].legend(loc='upper center', fontsize=8)
    axs[0].grid(True, color=theme["grid_color"])

    # Plot wind data
    axs[1].plot(df["Timestamp"], df["Forecast_Wind"], label="Forecast Wind (km/h)",
                color='#66BB6A', marker='o', markersize=3, linewidth=1)
    axs[1].plot(df["Timestamp"], df["Actual_Wind"], label="Actual Wind (km/h)",
                color='#EF5350', marker='x', markersize=4, linewidth=1)
    axs[1].set_title("Wind Speed Over Time", fontsize=12, color=theme["label_fg"])
    axs[1].set_ylabel("Wind Speed (km/h)", fontsize=10, color=theme["label_fg"])
    axs[1].set_xlabel("Date & Time", fontsize=10, color=theme["label_fg"])
    axs[1].legend(loc='upper center', fontsize=8)
    axs[1].grid(True, color=theme["grid_color"])

    fig.subplots_adjust(bottom=0.15, top=0.93)

    # Draw the figure into the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Zoom and reset functions
    def zoom(event):
        if event.state & 0x0004:
            base_scale = 1.1
            direction = 1 if event.delta > 0 else -1
            scale_factor = base_scale if direction > 0 else 1 / base_scale
            for ax in fig.axes:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                xcenter = (xlim[0] + xlim[1]) / 2
                ycenter = (ylim[0] + ylim[1]) / 2
                xsize = (xlim[1] - xlim[0]) * scale_factor
                ysize = (ylim[1] - ylim[0]) * scale_factor
                ax.set_xlim([xcenter - xsize / 2, xcenter + xsize / 2])
                ax.set_ylim([ycenter - ysize / 2, ycenter + ysize / 2])
            canvas.draw()
            
    def reset_zoom(event=None):
        for ax in fig.axes:
            ax.autoscale()
        canvas.draw()

    canvas_widget.bind("<Control-MouseWheel>", zoom)
    canvas_widget.bind("<Double-Button-1>", reset_zoom)

    # Create a frame to hold top-right utilities
    top_util_frame = tk.Frame(parent_frame, bg=theme["bg"])
    top_util_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

    # Reset zoom button at top right of graph
    ttk.Button(top_util_frame, text="Back to Default Zoom", command=reset_zoom, style="Custom.TButton").pack()

# Main application window using Tkinter
class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard Homepage")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.9)}x{int(screen_height * 0.9)}")
        self.configure(bg=get_theme_colors()["bg"])
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", lambda event: self.show_home())  # Escape key shortcut

        # Styling for widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TButton", font=("Segoe UI", 14, "bold"), padding=10)
        style.configure("Custom.Treeview", font=("Segoe UI", 14), rowheight=45)
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 15, "bold"))

        # Create two main views (frames)
        self.home_frame = tk.Frame(self, bg=get_theme_colors()["bg"])
        self.graph_frame = tk.Frame(self, bg=get_theme_colors()["bg"])

        self.build_home()       # Construct homepage
        self.build_graph_page() # Construct graph page
        self.show_home()        # Show homepage by default

    def on_close(self):
        self.destroy()
        sys.exit()

    # Constructs the homepage with project info and team table
    def build_home(self):
        theme = get_theme_colors()

        tk.Label(self.home_frame,
                 text="TFB2093 / TEB2203 - INTERNET OF THINGS\nMAY 2025 SEMESTER\nGROUP PROJECT",
                 bg=theme["bg"], fg=theme["fg"],
                 font=("Segoe UI", 26, "bold"), justify="center").pack(pady=30)

        ttk.Separator(self.home_frame, orient='horizontal').pack(fill='x', padx=100, pady=10)
        
        tk.Label(self.home_frame, text="Weather Homepage", font=("Segoe UI", 22, "bold"),
         bg=theme["bg"], fg=theme["fg"]).pack(pady=(10, 5))

        # Team member table box
        team_box = tk.LabelFrame(self.home_frame, text="TEAM MEMBERS", bg=theme["bg"], fg=theme["fg"],
                                 font=("Segoe UI", 16, "bold"), bd=2, relief="groove", padx=20, pady=10)
        team_box.pack(pady=20)

        table = ttk.Treeview(team_box, columns=("Name", "ID", "Programme"), show="headings",
                             style="Custom.Treeview", height=4)
        table.heading("Name", text="NAME")
        table.heading("ID", text="STUDENT ID")
        table.heading("Programme", text="PROGRAMME")

        table.column("Name", anchor="w", width=600)
        table.column("ID", anchor="center", width=200)
        table.column("Programme", anchor="center", width=200)

        # Insert team members
        members = [
            ("DAFFA WAHYU MAHARDIKA", "22000090", "IT"),
            ("NUR SYAFIQAH EZANY BINTI JOHARDI", "22006315", "IT"),
            ("AHMAD AFIF DANIAL BIN AZHARI", "22009264", "IT"),
            ("DANIELA ADLIN BINTI RAZWAN", "22008820", "IT"),
        ]
        for m in members:
            table.insert("", "end", values=m)
        table.pack()

        # Button to switch to graph view
        ttk.Button(self.home_frame, text="Show Weather Graphs",
                   command=self.show_graph, style="Custom.TButton").pack(pady=25, ipadx=15, ipady=5)

    # Constructs the graph analysis page with plots and stats
    def build_graph_page(self):
        theme = get_theme_colors()

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        container = tk.Frame(self.graph_frame, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Top back button for convenience
        back_button = ttk.Button(container, text="← Back to Homepage (Esc)", command=self.show_home, style="Custom.TButton")
        back_button.pack(anchor="nw", pady=(0, 10))

        # Title and MSE stats
        title_label = tk.Label(container, text="Weather Forecast vs Actual Data",
                               font=("Segoe UI", 22, "bold"), fg=theme["fg"], bg=theme["bg"])
        title_label.pack(pady=(10, 5))

        # Calculate and display error values for forecast vs actual
        temp_mse = mse(forecast_temp, actual_temp)
        wind_mse = mse(forecast_wind, actual_wind)
        mse_text = f"Temperature MSE: {temp_mse:.2f}     |     Wind Speed MSE: {wind_mse:.2f}"

        tk.Label(container, text=mse_text, bg=theme["bg"], fg="lightgray",
                 font=("Segoe UI", 14, "bold"), anchor="center").pack(pady=(5, 15))

        # Plot the weather data graphs
        plot_weather(container)

        # Optional second back button at bottom
        ttk.Button(container, text="← Back to Homepage", command=self.show_home,
                   style="Custom.TButton").pack(pady=30)

    # Display homepage
    def show_home(self):
        self.graph_frame.pack_forget()
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    # Display graph page
    def show_graph(self):
        self.home_frame.pack_forget()
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

# Start the application
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
