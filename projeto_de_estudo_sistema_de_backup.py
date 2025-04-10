import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import threading
import datetime
import time

class BackupManager:
    def __init__(self, source_path, destination_path, schedule_times, schedule_days, log_table):
        self.source_path = source_path
        self.destination_path = destination_path
        self.schedule_times = schedule_times
        self.schedule_days = schedule_days
        self.is_running = True
        self.backup_thread = None
        self.log_table = log_table
    
    def start_backup(self):
        self.is_running = True
        self.backup_thread = threading.Thread(target=self._backup_thread)
        self.backup_thread.start()
    
    def stop_backup(self):
        self.is_running = False
    
    def _backup_thread(self):
        while self.is_running:
            current_time = datetime.datetime.now().strftime("%H:%M")
            current_day = datetime.datetime.now().strftime("%A").lower()
            
            if current_day in self.schedule_days and current_time == self.schedule_times[current_day]:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"backup_{timestamp}.zip"
                backup_path = f"{self.destination_path}/{backup_filename}"
                
                try:
                    shutil.make_archive(backup_path, "zip", self.source_path)
                    self.log_table.insert("", tk.END, values=(timestamp, backup_path, "Sucesso"))
                except Exception as e:
                    self.log_table.insert("", tk.END, values=(timestamp, backup_path, f"Falha: {e}"))
                
               
                while datetime.datetime.now().strftime("%A").lower() == current_day and self.is_running:
                    time.sleep(1)
            else:
                time.sleep(1)

def select_file():
    file_path = filedialog.askdirectory(title="Selecione a pasta a ser copiada")
    if file_path:
        entry_source.delete(0, tk.END)
        entry_source.insert(0, file_path)

def select_destination():
    destination_path = filedialog.askdirectory(title="Selecione o diretório de destino para o backup")
    if destination_path:
        entry_destination.delete(0, tk.END)
        entry_destination.insert(0, destination_path)

def schedule_backup():
    source_path = entry_source.get()
    destination_path = entry_destination.get()
    
    schedule_times = {}
    schedule_days = []
    
    schedule_days.append("monday")
    schedule_times["monday"] = entry_time_monday.get()
    
    schedule_days.append("tuesday")
    schedule_times["tuesday"] = entry_time_tuesday.get()
    
    schedule_days.append("wednesday")
    schedule_times["wednesday"] = entry_time_wednesday.get()
    
    schedule_days.append("thursday")
    schedule_times["thursday"] = entry_time_thursday.get()
    
    schedule_days.append("friday")
    schedule_times["friday"] = entry_time_friday.get()
    
    schedule_days.append("saturday")
    schedule_times["saturday"] = entry_time_saturday.get()
    
    schedule_days.append("sunday")
    schedule_times["sunday"] = entry_time_sunday.get()
    
    if source_path and destination_path and all(schedule_times.values()):
        backup_manager = BackupManager(source_path, destination_path, schedule_times, schedule_days, log_table)
        backup_manager.start_backup()
    else:
        print("Preencha todos os campos.")


window = tk.Tk()
window.title("Alchemy Backup")
window.geometry("500x400")


def quit_program():
    window.destroy()


footer_frame = ttk.Frame(window, style="TFrame")
footer_frame.pack(side=tk.BOTTOM, pady=10)
footer_label = ttk.Label(footer_frame, text="Hacking Alchemy")
footer_label.pack()

style = ttk.Style(window)
style.theme_use("clam")

tab_control = ttk.Notebook(window)
tab_home = ttk.Frame(tab_control, style="TFrame")
tab_source = ttk.Frame(tab_control, style="TFrame")
tab_destination = ttk.Frame(tab_control, style="TFrame")
tab_schedule = ttk.Frame(tab_control, style="TFrame")
tab_control.add(tab_home, text="Home")
tab_control.add(tab_source, text="Selecionar Arquivo")
tab_control.add(tab_destination, text="Selecionar Destino")
tab_control.add(tab_schedule, text="Agendamento")
tab_control.pack(expand=1, fill="both", padx=20, pady=20)


home_frame = ttk.Frame(tab_home, style="TFrame")
home_frame.pack(pady=50)

home_label = ttk.Label(home_frame, text="Bem-vindo ao Alchemy backup", font=("Arial", 16, "bold"))
home_label.pack(pady=20)

enter_button = ttk.Button(home_frame, text="Entrar", command=lambda: tab_control.select(tab_source))
enter_button.pack()


frame_source = ttk.Frame(tab_source, style="TFrame", height=150)
frame_source.pack(side=tk.LEFT, padx=10)

label_source = ttk.Label(frame_source, text="Diretório de origem:")
label_source.pack(pady=10)
entry_source = ttk.Entry(frame_source, font=("Arial", 14))
entry_source.pack(pady=5)

button_select_file = ttk.Button(frame_source, text="Selecionar", command=select_file)
button_select_file.pack(pady=5)


frame_destination = ttk.Frame(tab_destination, style="TFrame")
frame_destination.pack(side=tk.LEFT, padx=10)

label_destination = ttk.Label(frame_destination, text="Diretório de destino:")
label_destination.pack(pady=10)
entry_destination = ttk.Entry(frame_destination, font=("Arial", 12))
entry_destination.pack(pady=5)

button_select_destination = ttk.Button(frame_destination, text="Selecionar", command=select_destination)
button_select_destination.pack(pady=5)


frame_schedule = ttk.Frame(tab_schedule, style="TFrame")
frame_schedule.pack()

# Segunda-feira
label_time_monday = ttk.Label(frame_schedule, text="Segunda-feira (HH:MM):", font=("Arial", 12))
label_time_monday.grid(row=1, column=0)
entry_time_monday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_monday.grid(row=2, column=0)

# Terça-feira
label_time_tuesday = ttk.Label(frame_schedule, text="Terça-feira (HH:MM):", font=("Arial", 12))
label_time_tuesday.grid(row=1, column=1)
entry_time_tuesday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_tuesday.grid(row=2, column=1)

# Quarta-feira
label_time_wednesday = ttk.Label(frame_schedule, text="Quarta-feira (HH:MM):", font=("Arial", 12))
label_time_wednesday.grid(row=1, column=2)
entry_time_wednesday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_wednesday.grid(row=2, column=2)

# Quinta-feira
label_time_thursday = ttk.Label(frame_schedule, text="Quinta-feira (HH:MM):", font=("Arial", 12))
label_time_thursday.grid(row=1, column=3)
entry_time_thursday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_thursday.grid(row=2, column=3)

# Sexta-feira
label_time_friday = ttk.Label(frame_schedule, text="Sexta-feira (HH:MM):", font=("Arial", 12))
label_time_friday.grid(row=1, column=4)
entry_time_friday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_friday.grid(row=2, column=4)

# Sábado
label_time_saturday = ttk.Label(frame_schedule, text="Sábado (HH:MM):", font=("Arial", 12))
label_time_saturday.grid(row=1, column=5)
entry_time_saturday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_saturday.grid(row=2, column=5)

# Domingo
label_time_sunday = ttk.Label(frame_schedule, text="Domingo (HH:MM):", font=("Arial", 12))
label_time_sunday.grid(row=1, column=6)
entry_time_sunday = ttk.Entry(frame_schedule, font=("Arial", 12))
entry_time_sunday.grid(row=2, column=6)


frame_buttons = ttk.Frame(window, style="TFrame")
frame_buttons.pack(pady=20)

button_start = ttk.Button(frame_buttons, text="Iniciar Backup", command=schedule_backup)
button_start.grid(row=0, column=0, padx=10)

button_stop = ttk.Button(frame_buttons, text="Parar Backup", command=quit_program)
button_stop.grid(row=0, column=1, padx=10)

frame_log = ttk.Frame(window, style="TFrame")
frame_log.pack()

log_table = ttk.Treeview(frame_log, columns=("timestamp", "path", "status"))
log_table.heading("timestamp", text="Data e Hora")
log_table.heading("path", text="Caminho do Backup")
log_table.heading("status", text="Status")
log_table.pack()

window.mainloop()
