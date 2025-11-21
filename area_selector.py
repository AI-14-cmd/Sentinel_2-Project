import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser

def get_coordinates_from_user():
    """Get coordinates from user - no default location allowed"""
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    while True:
        # Ask user for input method
        choice = messagebox.askyesno(
            "Area Selection", 
            "Choose input method:\n\nYES - Enter coordinates manually\nNO - Use Google Maps to find coordinates"
        )
        
        if choice:  # Manual input
            try:
                lat = float(simpledialog.askstring("Latitude", "Enter latitude (-90 to 90):"))
                lon = float(simpledialog.askstring("Longitude", "Enter longitude (-180 to 180):"))
                
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    return lat, lon
                else:
                    messagebox.showerror("Error", "Invalid coordinates! Please try again.")
                    
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid input! Please try again.")
                
        else:  # Google Maps
            messagebox.showinfo(
                "Google Maps Instructions", 
                "1. Google Maps will open\n2. Right-click on your area of interest\n3. Copy the coordinates (first number is latitude, second is longitude)\n4. Come back and enter them"
            )
            webbrowser.open("https://maps.google.com")
            
            try:
                coords = simpledialog.askstring("Coordinates", "Enter coordinates (lat, lon) separated by comma:")
                if coords:
                    lat, lon = map(float, coords.split(','))
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        return lat, lon
                    else:
                        messagebox.showerror("Error", "Invalid coordinates! Please try again.")
                else:
                    messagebox.showerror("Error", "No coordinates entered! Please try again.")
            except:
                messagebox.showerror("Error", "Invalid format! Please try again.")

def get_date_range():
    """Get date range from user"""
    root = tk.Tk()
    root.withdraw()
    
    while True:
        start_date = simpledialog.askstring("Start Date", "Enter start date (YYYY-MM-DD):", initialvalue="2023-06-01")
        end_date = simpledialog.askstring("End Date", "Enter end date (YYYY-MM-DD):", initialvalue="2023-08-31")
        
        if start_date and end_date:
            return start_date, end_date
        else:
            messagebox.showerror("Error", "Both dates are required! Please try again.")