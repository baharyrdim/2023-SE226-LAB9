import sqlite3
from datetime import datetime
import tkinter as tk
from logging import root
from tkinter import messagebox

conn = sqlite3.connect('marvel.db')
cursor = conn.cursor()

def select_all_entries():
    cursor.execute("SELECT * FROM marvel_movies")
    entries = cursor.fetchall()
    return entries

with open('marvel.txt', 'r') as file:
    for line in file:
        line = line.strip().split('\t')
        movie_id = int(line[0])
        movie = line[1]
        date = datetime.strptime(line[2], '%B%d,%Y').date()
        mcu_phase = line[3]
        cursor.execute('INSERT INTO movies VALUES (?, ?, ?, ?)', (movie_id, movie, date, mcu_phase))

conn.commit()
conn.close()

def add_button_clicked():
    def ok_button_clicked():
        movie = movie_entry.get()
        date = date_entry.get()
        phase = phase_entry.get()

        try:
            date = datetime.strptime(date, '%B%d,%Y').date()
            cursor.execute('INSERT INTO movies (movie, date, mcu_phase) VALUES (?, ?, ?)', (movie, date, phase))
            conn.commit()
            messagebox.showinfo("Success", "Data added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format!")

        popup.destroy()

    def cancel_button_clicked():
        popup.destroy()

    popup = tk.Toplevel(root)

    movie_label = tk.Label(popup, text="Movie:")
    movie_label.pack()
    movie_entry = tk.Entry(popup)
    movie_entry.pack()

    date_label = tk.Label(popup, text="Date:")
    date_label.pack()
    date_entry = tk.Entry(popup)
    date_entry.pack()

    phase_label = tk.Label(popup, text="MCU Phase:")
    phase_label.pack()
    phase_entry = tk.Entry(popup)
    phase_entry.pack()

    # Add OK and Cancel buttons
    ok_button = tk.Button(popup, text="OK", command=ok_button_clicked)
    ok_button.pack()
    cancel_button = tk.Button(popup, text="Cancel", command=cancel_button_clicked)
    cancel_button.pack()

    text_box = tk.Text(root)
    text_box.pack()

    def list_all_button_clicked():
        text_box.delete("1.0", tk.END)
        entries = select_all_entries()

        for entry in entries:
            text_box.insert(tk.END, f"ID: {entry[0]}\n")
            text_box.insert(tk.END, f"Movie: {entry[1]}\n")
            text_box.insert(tk.END, f"Date: {entry[2]}\n")
            text_box.insert(tk.END, f"MCU Phase: {entry[3]}\n")
            text_box.insert(tk.END, "\n")

    list_all_button = tk.Button(root, text="LIST ALL", command=list_all_button_clicked)
    list_all_button.pack()
