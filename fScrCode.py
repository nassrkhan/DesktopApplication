
import csv
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox

def format_date_time(date_str, time_str):
    date = datetime.strptime(date_str, '%d.%m.%Y').strftime('%d.%m.%Y')
    time = datetime.strptime(time_str, '%H:%M:%S').strftime('%H:%M:%S')
    return date, time

def calculate_elapsed_time(prev_time, current_time):
    prev_datetime = datetime.strptime(prev_time, '%H:%M:%S')
    current_datetime = datetime.strptime(current_time, '%H:%M:%S')
    elapsed_time = current_datetime - prev_datetime
    return str(elapsed_time)

def process_data(input_file, start_datetime, end_datetime):
    data = []

    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter=';')
        next(reader)  # Skip header

        prev_time = None

        for row in reader:
            try:
                date, time = format_date_time(row[1], row[2])
                curr_datetime = datetime.strptime(date + ' ' + time, '%d.%m.%Y %H:%M:%S')

                if start_datetime <= curr_datetime <= end_datetime:
                    if prev_time:
                        elapsed = calculate_elapsed_time(prev_time, time)
                    else:
                        elapsed = '0:00:00'

                    prev_time = time

                    temperature = float(row[3].replace(',', '.'))

                    data.append([row[0], elapsed, date, time, temperature])

            except ValueError as e:
                print(f"Error parsing date on row: {row}")
                continue

    df = pd.DataFrame(data, columns=['#', 'Elapsed', 'Date', 'Time', 'Int T °C'])

    start_time = start_datetime.time()
    end_time = end_datetime.time()

    filtered_df = df[((df['Date'] == start_datetime.strftime('%d.%m.%Y')) & (df['Time'] >= start_time.strftime('%H:%M:%S'))) |
                     ((df['Date'] == end_datetime.strftime('%d.%m.%Y')) & (df['Time'] <= end_time.strftime('%H:%M:%S'))) |
                     ((df['Date'] > start_datetime.strftime('%d.%m.%Y')) & (df['Date'] < end_datetime.strftime('%d.%m.%Y'))) |
                     ((df['Date'] == start_datetime.strftime('%d.%m.%Y')) & (df['Time'] >= start_time.strftime('%H:%M:%S'))) |
                     ((df['Date'] == end_datetime.strftime('%d.%m.%Y')) & (df['Time'] <= end_time.strftime('%H:%M:%S')))].copy()

    filtered_df.loc[:, '#'] = range(1, len(filtered_df) + 1)

    start_time = datetime.strptime('0:00:00', '%H:%M:%S')
    filtered_df.loc[:, 'Elapsed'] = [(start_time + timedelta(minutes=i)).strftime('%H:%M:%S') for i in range(len(filtered_df))]

    return filtered_df


def browse_file():
    filename = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, filename)

def process_and_display():
    input_file = entry_file.get()
    start_date_str = entry_start_date.get()
    start_time_str = entry_start_time.get()
    end_date_str = entry_end_date.get()
    end_time_str = entry_end_time.get()

    try:
        start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%d.%m.%Y %H:%M:%S')
        end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%d.%m.%Y %H:%M:%S')

        df = process_data(input_file, start_datetime, end_datetime)
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, df.to_string(index=False))
        text_output.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Data Processing")

frame_file = tk.Frame(root)
frame_file.pack(padx=10, pady=5, fill=tk.X)

label_file = tk.Label(frame_file, text="Input File:")
label_file.pack(side=tk.LEFT)

entry_file = tk.Entry(frame_file, width=50)
entry_file.pack(side=tk.LEFT, padx=(5, 0))

button_browse = tk.Button(frame_file, text="Browse", command=browse_file)
button_browse.pack(side=tk.LEFT, padx=(5, 0))

frame_start_datetime = tk.Frame(root)
frame_start_datetime.pack(padx=10, pady=5, fill=tk.X)

label_start_date = tk.Label(frame_start_datetime, text="Start Date (DD.MM.YYYY):")
label_start_date.pack(side=tk.LEFT)

entry_start_date = tk.Entry(frame_start_datetime)
entry_start_date.pack(side=tk.LEFT, padx=(5, 0))

label_start_time = tk.Label(frame_start_datetime, text="Start Time (HH:MM:SS):")
label_start_time.pack(side=tk.LEFT, padx=(10, 0))

entry_start_time = tk.Entry(frame_start_datetime)
entry_start_time.pack(side=tk.LEFT, padx=(5, 0))

frame_end_datetime = tk.Frame(root)
frame_end_datetime.pack(padx=10, pady=5, fill=tk.X)

label_end_date = tk.Label(frame_end_datetime, text="End Date (DD.MM.YYYY):")
label_end_date.pack(side=tk.LEFT)

entry_end_date = tk.Entry(frame_end_datetime)
entry_end_date.pack(side=tk.LEFT, padx=(5, 0))

label_end_time = tk.Label(frame_end_datetime, text="End Time (HH:MM:SS):")
label_end_time.pack(side=tk.LEFT, padx=(10, 0))

entry_end_time = tk.Entry(frame_end_datetime)
entry_end_time.pack(side=tk.LEFT, padx=(5, 0))

button_process = tk.Button(root, text="Process and Display", command=process_and_display)
button_process.pack(pady=10)

text_output = tk.Text(root, height=20, width=100)
text_output.pack(padx=10, pady=5)

text_output.config(state=tk.DISABLED)

root.mainloop()
