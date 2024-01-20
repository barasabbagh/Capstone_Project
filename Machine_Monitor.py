#this code was made by bara sabbagh 
import pandas as pd
import customtkinter as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import tkinter as tk
import sv_ttk as sv_ttk
from tkinter import filedialog
from tkinter import ttk
from CTkMessagebox import *
import time 
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import subprocess
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from scipy.interpolate import make_interp_spline
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QHBoxLayout,\
    QFileDialog, QLabel, QListWidget, QListWidgetItem, QSplashScreen, QMainWindow, QMessageBox, QComboBox, QInputDialog,\
    QDialog, QLineEdit, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import sys

# splash_app = QApplication(sys.argv)
# # Create a splash screen
# splash = QSplashScreen()
# pic_path = r"C:\Users\bsabagh\Downloads\pixlr-image-generator-8b71ee97-22ac-42b4-af12-8106fe5789ea.png"
# splash.setPixmap(QPixmap(pic_path))  # Set the path to your logo image

# # Create and configure a loading progress bar (you can adjust the appearance)
# loading_bar = QProgressBar(splash)
# loading_bar.setTextVisible(False)  # Hide the text
# loading_bar.setGeometry(150, splash.height() - 40, splash.width() - 300, 20)  # Adjust the position and size

# # Use a stylesheet to change the color of the progress bar
# loading_bar.setStyleSheet('QProgressBar {background-color: #2b2d42; border: 1px solid #FFFFFF; border-radius: 3px;}'
#                           'QProgressBar::chunk {background-color: #0077b6;}'
#                           'QProgressBar::text {color: #000000;}'
#                           'text-visible: false;')
# splash.show()
# timer = QTimer()
# timer.timeout.connect(splash.close)  # Connect the timer to close the splash screen
# timer.start(3000)
# # Show the splash screen
# # Simulate some loading process
# for i in range(4):
#     loading_bar.setValue((i + 1) * 25)  # Update the loading progress (you can adjust as needed)
#     QApplication.processEvents()  # Process events to keep the UI responsive
#     time.sleep(1)  # Simulate loading (adjust as needed)




def starter():
    update_treeview()
    plot_data()
    reload_and_refresh()
    tree.place(x=0, y=0, width=600, height=450)
    checkbox()
    update_timer()
    controlframe.place(x= 15 , y = 570 )
    controlframe.propagate(False)
    controlframe2.place(x= 410 , y = 570 )
    controlframe2.propagate(False)
    last_Values.place( x= 320 , y = 570 )
    last_Values.propagate(False)
    static_labels()
    last_values()
    control_header.place(x =10  , y =530 )
    info_header.place(x= 410 , y = 530 )
    createreportbtn.place(x = 150 , y= 3)
    exportbtn.place(x = 310 ,y= 3)
    wattage()
    energy()

app = ct.CTk()
app.attributes('-fullscreen', True)
app.title("Hydorgen Production Monitor")
app.resizable(width=False, height=False)

# initialize the tab view 

tabview = ct.CTkTabview(master=app , width= 1920 , 
                        height= 1080 ,
                        border_width= 1 ,
                        segmented_button_selected_color= "#1b8658",
                        segmented_button_unselected_hover_color = "#1b8658"
                        )
tabview.pack(padx=20, pady=20)

# Add tabs

tab1 =tabview.add("Monitor")
tab2 =tabview.add("Ai Optimization Model")  # add tab at the end
tab2 =tabview.add("unkonwn")  # add tab at the end

# Set main tab
tabview.set("Monitor")  

# Add frames
treeframe = ct.CTkFrame(tab1, width=600, height=450 , fg_color="#2b2b2b" , bg_color= "#2b2b2b")
treeframe.place(x=10, y=70)

uploadatarame = ct.CTkFrame(tab1, width=600, height=50)
uploadatarame.place(x=10, y=1)



middleframe = ct.CTkFrame(tab1, width=1190, height=970)
middleframe.place(x=650, y=0)

timer_label = ct.CTkLabel(app, text="Timer: 00:00", width=100, height=30, fg_color="#ff6801", font=("calibri light", 18),  corner_radius = 50)

controlframe = ct.CTkFrame(tab1, width= 300 , height= 400 , border_width= 2 , border_color="#1b8658")
controlframe2 = ct.CTkFrame(tab1, width= 200 , height= 400 , border_width= 2 , border_color="#1b8658")

control_header = ct.CTkLabel(tab1,text= "Sensor control" , width= 400-5 , height= 30 , fg_color="#1b8658",corner_radius = 15 , font=("calibri light", 18))
info_header = ct.CTkLabel(tab1,text= "Info" , width= 200 , height= 30 , fg_color="#1b8658",corner_radius = 15 , font=("calibri light", 18))

last_Values = ct.CTkFrame(tab1, width= 85 , height= 400 , border_width= 0 , border_color="#1b8658")

# initial variables
file_path = None
parameters = []
data = []
parameter_states = {}
timer_seconds = 0

# Create a style
style = ttk.Style()
style.configure("Treeview",
                background = "silver",
                foreground = "#2b2b2b",
                fieldbackground = "#2b2b2b",
                font = ("calibri light", 2)

)
# Create a ttk.Treeview widget

tree = ttk.Treeview(treeframe, style="Treeview")
tree["columns"] = tuple()
tree["show"] = "headings"


#intialize the plot

fig, ax = plt.subplots(figsize=(12, 10))
canvas = FigureCanvasTkAgg(fig, master=middleframe)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(padx = 5 , pady= 5)

 
def read_file():
    global csv, file_path, parameters
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    # Show some positive message with the checkmark icon
    CTkMessagebox(message="CTkMessagebox is successfully installed.",
                  icon="check", option_1="Thanks")
    return file_path


def reload_and_refresh():
    global data, file_path, parameters, column_name_to_drop
    if file_path:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')
        column_name_to_drop = 'Date'
        if column_name_to_drop in data.columns:
            data = data.drop(columns=[column_name_to_drop])
        # data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S.%f').dt.strftime('%H:%M:%S')
        parameters = list(data.columns)

    tab1.after(1000, reload_and_refresh)

    return parameters


def update_treeview():
    # print("tree refresh data")
    global data, parameters, column_name_to_drop 
    if parameters:
        # Configure columns in the Treeview based on the dataframe columns
        tree["columns"] = tuple(parameters)
        column_width = int(599 / len(parameters))
        # Create headings for each column
        for col in parameters:
            # Adjust column width based on the content
            tree.column(col, width=column_width, stretch=False)
            tree.heading(col, text=col)
        tree.delete(*tree.get_children())

        # Insert the last 20 rows into the Treeview
        for index, row in data.tail(19).iterrows():
            tree.insert("", "end", values=list(row))
    tab1.after(1000, update_treeview)



def plot_data():
    global data, parameters, parameter_states
    # print("plot refresh data")
    if data is not None and parameters:
        # Plot Time against selected parameters based on checkbox states
        ax.clear()
        selected_params = [param for param in parameters if param != 'Time' and parameter_states[param].get()]
        for param in selected_params:
            ax.plot(data['Time'].tail(50), data[param].tail(50), label=param)
        
        ax.legend()
        plt.xticks(rotation=70)
        ax.set_xlabel('Time')
        ax.set_ylabel('Parameter Values')
        ax.set_title('Time vs Parameters')
        ax.grid(True)

        # Update canvas
        canvas.draw()
    
    tab1.after(1000, plot_data)


def checkbox():
    for param in parameters:
        if param != "Time":
            # Create a Tkinter variable to store the state (checked or unchecked)
            parameter_states[param] = tk.BooleanVar()
            # Initialize the checkbox state to True (checked)
            parameter_states[param].set(True)
            
            # Create a checkbox for the parameter
            switch = ct.CTkCheckBox(
                controlframe,
                text=param,
                variable=parameter_states[param],
                font=("calibri light", 21),
                width= 30 , corner_radius=15 , hover_color="#1b8658"
                
                
            )
            switch.pack(side="top", pady=12 , padx = 10,anchor="w")


def update_timer():
    global timer_seconds
    timer_seconds += 1
    minutes = timer_seconds // 60
    seconds = timer_seconds % 60
    timer_label.configure(text=f"Timer: {minutes:02d}:{seconds:02d}")
    timer_label.place(x=20, y=3)
    timer_label.destroy
    app.after(1000, update_timer)



def generate():
    with PdfPages('output_plots.pdf') as pdf:
        # Create correlation matrix once
        plt.figure(figsize=(18, 10))# , facecolor="red")
        cols_to_exclude = ['Time']
        corr_matrix = data.drop(columns=cols_to_exclude).corr()  # Exclude 'Time' column from correlation matrix
        # print(corr_matrix)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title(f'Correlation Matrix')
        plt.tight_layout()
        # Save the correlation matrix figure into the same pdf page
        pdf.savefig()
        plt.close()

        for param in parameters:
            # Skip the "Time vs Time" plot
            if param == 'Time':
                continue
            
            plt.figure(figsize=(18, 10))
            
            # Plot the data
            plt.plot(data['Time'], data[param],  label=param)
            
            # Calculate statistics
            mean_val = data[param].mean()
            std_val = data[param].std()
            var_val = data[param].var()
            min_val = data[param].min()
            max_val = data[param].max()


            
            # Plot the mean as a dashed line
            plt.axhline(y=mean_val, color='black', linestyle='--')
            
            # Add statistics to the legend
            plt.legend([f'{param} \nMean: {mean_val:.2f}\nStd: {std_val:.2f}\nVar: {var_val:.2f}\nMin: {min_val}\nMax: {max_val}'])
            
            # Other plot settings
            plt.xlabel('Time')
            plt.ylabel(param)
            plt.title(f'Time vs {param}')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.xticks(ticks=range(0, len(data), 15))  # Adjust the number of ticks to plot

            # Save the current figure into a pdf page
            pdf.savefig()
            
            # Close the current figure to free up memory
            plt.close()

    # Open the PDF file after finishing
    if file_path:
        subprocess.Popen(['start', 'output_plots.pdf'], shell=True)



def static_labels():
    num_Sensors = int(len(parameters) ) -1
    # print(num_Sensors) # Print
    num_Sensors_label = ct.CTkLabel(controlframe2 , text = "Number of Sensors : " f"{num_Sensors}" ,width= 190 , height= 30 ,corner_radius = 0 , font=("calibri light", 18) , fg_color="#1f6aa5")
    num_Sensors_label.place( x = 5 , y = 5)

def wattage():
    # Calculate wattage
    global wattage_value
    wattage_value = int(data["Current [A]"].iloc[-1] * data["Voltage [V]"].iloc[-1])
    # print(wattage_value, "w")

    # Create a new label with the updated wattage value
    wattage_label = ct.CTkLabel(controlframe2, text=f"Wattage: {wattage_value} w", width=190, height=30, corner_radius=0, font=("calibri light", 18), fg_color="#1f6aa5")
    wattage_label.place(x=5, y=40)
    wattage_label.destroy

    # Schedule the label to be destroyed after one second
    app.after(1000, wattage)
    return(wattage_value)
def energy():
    energy_value = wattage_value * len(data)
    print(len(data))
    energy_label = ct.CTkLabel(controlframe2, text=f"Energy: {energy_value} Wh", width=190, height=30, corner_radius=0, font=("calibri light", 18), fg_color="#1f6aa5")
    energy_label.place(x=5, y=75)
    energy_label.destroy
    app.after(1000, energy)
    
def last_values():
    last_values_dict = {param: data[param].iloc[-1] for param in data.columns if param != "Time"}

    # Clear previous labels
    for widget in last_Values.winfo_children():
        widget.destroy()

    # Print or use the last values as needed
    # print("Last values:")
    for param, value in last_values_dict.items():
        # print(f"{param}: {value}")
        lastvalue_label = ct.CTkLabel(last_Values, text=f"{value}", width=75, corner_radius=5, font=("calibri light", 14), fg_color="#1f6aa5")
        lastvalue_label.pack(side="top", pady=11 , padx = 5,anchor="w")
    app.after(1000, last_values)

def quitapp():
    msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                        icon="question", option_1="No", option_2="Yes", width= 250 , height= 160 , button_width= 30 )
    
    response = msg.get()
    
    if response=="Yes":
        app.destroy()
    else:
        print("Click 'Yes' to exit!")

def export_csv():
    global data
    if data.empty:
        CTkMessagebox(message="No data to export.", icon="warning", option_1="OK")
        return

    # Open a file dialog for selecting the export location
    export_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    # Check if a file path was selected
    if export_path:
        try:
            # Export the DataFrame to CSV
            data.to_csv(export_path, index=False)
            CTkMessagebox(message=f"CSV file has been exported to:\n{export_path}",
                                        icon="check", option_1="OK")
        except Exception as e:
            CTkMessagebox(message=f"Error exporting CSV file:\n{str(e)}", icon="error", option_1="OK")

quitbtn = ct.CTkButton(app, text="Quit", command=quitapp, width=60, height=30, 
                           font=("calibri light", 18) ,fg_color="red" , hover_color="#1b8658" , corner_radius=50)
quitbtn.place(x=1830, y=3)

# Creating buttons
readbutton = ct.CTkButton(uploadatarame, text="Read CSV",command=lambda: [read_file(), starter()], width=600, height=50,
                          font=("calibri light", 20 , "bold") , fg_color="#1b8658",  hover_color="green")
readbutton.place(x=0, y=0)

createreportbtn = ct.CTkButton(app , width= 120 , height= 30 , command=generate, text = "Generate Report" ,
                               font=("calibri light", 18) ,fg_color="#1b8658" , hover_color="green" , corner_radius=50)

exportbtn = ct.CTkButton(app , width= 120 , height= 30 , command=export_csv, text = "Export CSV" ,
                               font=("calibri light", 18) ,fg_color="#5a352a" , hover_color="green" , corner_radius=50)
sv_ttk.set_theme("dark")
app.mainloop()



