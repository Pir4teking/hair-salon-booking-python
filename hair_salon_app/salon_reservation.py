import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

class SalonReservation:
    def __init__(self):
        self.available_times = {
            "Monday": ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00"],
            "Tuesday": ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00"],
            "Wednesday": ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00"],
            "Thursday": ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00"],
            "Friday": ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00"],
            "Saturday": ["09:00", "10:00", "11:00", "12:00", "13:00"]
        }
        self.reservations = {}

    def make_reservation(self, name, date, time):
        day_of_week = date.strftime('%A')

        if day_of_week in self.available_times and time in self.available_times[day_of_week]:
            if (day_of_week, time) not in self.reservations:
                self.reservations[(day_of_week, time)] = name
                self.available_times[day_of_week].remove(time)
                return True
            return False
        return None


def reserve():
    name = name_entry.get()
    time = time_combobox.get()
    selected_date = calendar.selection_get()

    if not name or not selected_date or not time:
        messagebox.showwarning("Incomplete fields", "Please complete all fields.")
        return

    try:
        date = datetime.strptime(str(selected_date), "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Invalid date", "Please select a valid date.")
        return

    result = salon.make_reservation(name, date, time)
    if result is True:
        messagebox.showinfo("Reservation confirmed", f"Reservation confirmed for {name} on {date.strftime('%d %B')} at {time}!")
    elif result is False:
        messagebox.showwarning("Time unavailable", "This time slot is already reserved.")
    else:
        messagebox.showerror("Error", "Time slot not available.")


def update_times():
    selected_date = calendar.selection_get()
    if selected_date:
        try:
            date = datetime.strptime(str(selected_date), "%Y-%m-%d")
            current_time = datetime.now()

            # Check if the date is before today
            if date.date() < datetime.now().date():
                messagebox.showwarning("Invalid date", "Reservations cannot be made for past dates.")
                time_combobox['values'] = ["Please choose another date"]
                time_combobox.set('')
                return

            # Check if it is Sunday
            if date.strftime('%A') == 'Sunday':
                messagebox.showwarning("Invalid date", "There is no service on Sundays.")
                time_combobox['values'] = ["No service"]
                time_combobox.set('')
                return

            day_of_week = date.strftime('%A')

            # Get all available times for that day
            all_times = salon.available_times.get(day_of_week, []).copy()

            # Filter times already passed if it is today
            if date.date() == datetime.now().date():
                all_times = [time for time in all_times 
                             if datetime.strptime(time, "%H:%M").time() > current_time.time()]

            # Filter the times already reserved
            reserved_times = [time for (day, time) in salon.reservations.keys() 
                              if day == day_of_week]
            available_times = [time for time in all_times 
                               if time not in reserved_times]

            # Update the combobox
            if available_times:
                time_combobox['values'] = sorted(available_times)
            else:
                time_combobox['values'] = ["No available times"]
            time_combobox.set('')
            
        except ValueError:
            time_combobox['values'] = ["Date error"]
            time_combobox.set('')


root = tk.Tk()
root.title("Beauty Salon Reservation")
root.geometry("360x500")
root.configure(bg="#FAF3F3")

salon = SalonReservation()

# Title and labels
tk.Label(root, text="Book your appointment", font=("Helvetica", 16, "bold"), bg="#FAF3F3", fg="#333").pack(pady=10)
tk.Label(root, text="Name:", font=("Helvetica", 10), bg="#FAF3F3", fg="#555").pack(pady=5)

# Name entry field
name_entry = tk.Entry(root, font=("Helvetica", 10), width=25)
name_entry.pack()

# Label and calendar
tk.Label(root, text="Date:", font=("Helvetica", 10), bg="#FAF3F3", fg="#555").pack(pady=5)

# Calendar configuration with custom style
calendar = Calendar(
    root, 
    selectmode="day",
    date_pattern="yyyy-mm-dd",
    background="#FFFFFF",
    foreground="#333333",
    headersbackground="#FFB6C1",
    headersforeground="#FFFFFF",
    selectbackground="#FFB6C1",
    selectforeground="#FFFFFF",
    normalbackground="#FFFFFF",
    normalforeground="#333333",
    weekendbackground="#FFF0F5",
    weekendforeground="#333333",
    firstweekday="sunday",
    locale='en_US',
    mindate=datetime.now(),
    cursor="hand1",
    borderwidth=1,
    relief="solid"
)
calendar.pack(pady=10)
calendar.bind("<<CalendarSelected>>", lambda event: update_times())

# Label and combobox for time
tk.Label(root, text="Time:", font=("Helvetica", 10), bg="#FAF3F3", fg="#555").pack(pady=5)
time_combobox = ttk.Combobox(root, font=("Helvetica", 10), width=22, state="readonly")
time_combobox.pack()

# Book button
book_btn = tk.Button(root, text="Book", command=reserve, font=("Helvetica", 12, "bold"),
                     bg="#FFB6C1", fg="white", width=20, relief="flat", bd=0)
book_btn.pack(pady=20)

root.mainloop()