appointments = {}

def book_appointment():
    apt_id = input("Enter appointment ID: ")
    if apt_id in appointments:
        print("Appointment ID already exists!")
    else:
        name   = input("Enter patient name: ")
        age    = input("Enter patient age: ")
        doctor = input("Enter doctor name: ")
        date   = input("Enter date (YYYY-MM-DD): ")
        time   = input("Enter time (e.g. 10:00 AM): ")
        reason = input("Enter reason: ")
        appointments[apt_id] = {
            "name": name, "age": age, "doctor": doctor,
            "date": date, "time": time, "reason": reason, "status": "Scheduled"
        }
        print("Appointment booked successfully!")

def view_appointments():
    if not appointments:
        print("No appointments found.")
    else:
        for apt_id, info in appointments.items():
            print(f"\nID: {apt_id} | {info['name']} (Age: {info['age']}) | "
                  f"Dr. {info['doctor']} | {info['date']} at {info['time']} | "
                  f"Reason: {info['reason']} | Status: {info['status']}")

def search_appointment():
    apt_id = input("Enter appointment ID to search: ")
    if apt_id in appointments:
        info = appointments[apt_id]
        print(f"Found -> Patient: {info['name']}, Doctor: {info['doctor']}, "
              f"Date: {info['date']}, Time: {info['time']}, Status: {info['status']}")
    else:
        print("Appointment not found.")

def cancel_appointment():
    apt_id = input("Enter appointment ID to cancel: ")
    if apt_id in appointments:
        appointments[apt_id]["status"] = "Cancelled"
        print("Appointment cancelled.")
    else:
        print("Appointment not found.")

def complete_appointment():
    apt_id = input("Enter appointment ID to mark complete: ")
    if apt_id in appointments:
        appointments[apt_id]["status"] = "Completed"
        print("Appointment marked as completed.")
    else:
        print("Appointment not found.")

# Main Menu
while True:
    print("--- DOCTOR APPOINTMENT SYSTEM ---")
    print("1. Book Appointment")
    print("2. View All Appointments")
    print("3. Search Appointment")
    print("4. Cancel Appointment")
    print("5. Mark as Completed")
    print("6. Exit")
    choice = input("Enter choice: ")
    if choice == '1':
        book_appointment()
    elif choice == '2':
        view_appointments()
    elif choice == '3':
        search_appointment()
    elif choice == '4':
        cancel_appointment()
    elif choice == '5':
        complete_appointment()
    elif choice == '6':
        print("Exiting system...")
        break
    else:
        print("Invalid choice")
