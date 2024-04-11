import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTkEntry, CTkButton, CTkLabel, CTkCheckBox
import datetime

# from controllers.page_controller import PageController
# from controllers.user_controller import UserController
from pages.base_page import BasePage
# from pages.login_page import LoginPage
# from pages.registration_page import RegisterPage
# from pages.home_page import HomePage
# from pages.booking_page import BookingPage
# from pages.extend_packing_page import ExtendParkingPage
# from pages.payment_page import PaymentPage
# from pages.profit_loss_page import ProfitLossPage

class LoginPage(BasePage):
    def create_widgets(self):
        # Page-specific widgets for the login page
        label_title = CTkLabel(self, text="Login Page", font=("ar", 15, "bold"))
        label_title.pack(pady=20)

        # Username and Password entry fields
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        username_label = CTkLabel(self, text="Username:")
        username_label.pack(pady=5)
        username_entry = CTkEntry(self, textvariable=self.username_var)
        username_entry.pack(pady=5)

        password_label = CTkLabel(self, text="Password:")
        password_label.pack(pady=5)
        password_entry = CTkEntry(self, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        self.checkvalue = tk.IntVar(value=0)
        checkbtn = CTkCheckBox(self, text="Remember me?", variable=self.checkvalue)
        checkbtn.pack(pady=5)

        login_button = CTkButton(self, text="Login", command=self.getvals_login)
        login_button.pack(pady=10)

        register_button = CTkButton(self, text="Register", command=self.page_controller.show_registration_page)
        register_button.pack(pady=10)



    def getvals_login(self):
        user_name = self.username_var.get()
        password = self.password_var.get()
        # user_authenticated = self.authenticate_user(user_name, password)
        user_authenticated = self.page_controller.user_controller.authenticate_user(user_name, password)

        if user_authenticated:
            messagebox.showinfo("Login Successful", f"Welcome, {user_name}!\nWe missed you.")
            print("Login Successful", f"Welcome, {user_name}!\nWe missed you.")
            self.page_controller.set_authenticated_user(user_name) 
            self.page_controller.show_home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.\n\nHave you resistered an account?\n\nRegister Account if it does not exist or enter the correct credentials\n\nPlease try again.")

    # def authenticate_user(self, username, password):
    #     return username == "a" and password == "b"