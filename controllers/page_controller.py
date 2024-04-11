# app/controllers/page_controller.py version 2
from flask import redirect, url_for, request, render_template, flash
from flask import session, flash
from flask import jsonify
from flask import send_from_directory
import json
import uuid
from pages.login_page import LoginPage
# from pages.registration_page import RegisterPage
# from pages.home_page import HomePage
# from pages.booking_page import BookingPage
# from pages.extend_parking_page import ExtendParkingPage
# from pages.payment_page import PaymentPage
# from pages.profit_loss_page import ProfitLossPage
from controllers.data_service_controller import UserController
from models.user_model import UserModel
from models.time_model import TimeModel
from models.payment_model import PaymentModel
from models.parking_slots_available_model import ParkingSlotAvailableModel
from models.Parking_slots_assignment_model import SlotAssignmentModel
import datetime
# import user_data
class PageController:
    def __init__(self, app):
        self.app = app
        self.user_controller = UserController()
        # self.user_controller = UserController(username, password, name, phone, car_plate, email)
        self.login_page = LoginPage(self)
        # self.registration_page = RegisterPage(self)
        # self.home_page = HomePage(    self)
        # self.booking_page = BookingPage(self)
        # self.extend_parking_page = ExtendParkingPage(self)
        # self.payment_page = PaymentPage(self)
        # self.profit_loss_page = ProfitLossPage(self)
        # self.payment_model = PaymentModel()

        # Initial route

        @app.route('/static/<path:filename>')
        def serve_static(filename):
            return send_from_directory('static', filename)

        @app.route('/static_css/<path:filename>')
        def static_css(filename):
            return send_from_directory('static', filename)
        
        
        @app.route('/')
        def default():
            # return render_template('home_page.html')
            return render_template('login_page.html')
        
            self.home_page.show()
            page_controller = PageController(app)
            page_controller.show_home_page()

        @app.route('/profit_loss')
        def profit_loss():
            profit_loss_data = UserController.calculate_profit_loss(self.user_controller)
            return render_template('profit_loss.html', profit_loss_data=profit_loss_data)
        
        @app.route('/slot_management',methods=['GET', 'POST'])
        def slot_management():
            if request.method == 'POST':
                pass
            # Load existing slot data for display
            all_parking_slots = UserController.get_all_parking_slots_available_data(self.user_controller)
            print(all_parking_slots)
            return render_template('slot_management.html',  all_parking_slots=all_parking_slots)  
        
        @app.route('/slot_managementt')
        def slot_managementt():
            # Load existing slot data for display
            all_parking_slots = UserController.get_all_parking_slots_available_data(self.user_controller)
            print(f"Hello there! Here is the current all_parking_slots data in the database: {all_parking_slots}")
            return jsonify(all_parking_slots)
        
        @app.route('/parking_slot_id/<parking_slot_id>/<current_user_session_id>', methods=['GET'])
        def slot_history(parking_slot_id, current_user_session_id):
            if current_user_session_id == "all":
                parking_slot_id_key = parking_slot_id
                print(f'Target parking_slot_id_key ID is as follows: {parking_slot_id_key}') 
                selected_slot_data = UserController.get_selected_slot_history_data(self.user_controller, parking_slot_id_key)
                if selected_slot_data is not None:
                    return render_template('all_slot_history.html', selected_id_data = selected_slot_data['parking_slot_id'], time_occupied_data=selected_slot_data['time_occupied_data'])
                else:
                    return render_template('all_slot_history.html', selected_id_data = [], time_occupied_data = [])
            else:
                current_user_slot_data = UserController.get_current_user_slot_history_data(self.user_controller, parking_slot_id, current_user_session_id)
                # if current_user_slot_data:
                return render_template('current_user_slot_history.html', selected_id_data=parking_slot_id, current_user_session_id=current_user_session_id, time_occupied_data=current_user_slot_data)
                
        @app.route('/generate_slot_id')
        def generate_slot_id():
            parking_slot_id = UserController.generate_parking_slot_id(self.user_controller)
            slot_status = 'Good'
            available_for_use = True
            
            # Create parking_slots_available_data instance
            parking_slots_available_data_model = ParkingSlotAvailableModel(parking_slot_id, slot_status, available_for_use)
            # Register the slot
            add_parking_slot_successful = UserController.save_admin_added_parking_slots_available_data(self.user_controller, parking_slots_available_data_model)  
            if add_parking_slot_successful:
                slot_data = {
                    "parking_slot_id": parking_slot_id,
                    "slot_status": slot_status,
                    "available_for_use": available_for_use
                }
                return jsonify(slot_data)  # Return the slot data as JSON response                
                # flash('Slot added successfully!', 'success')
            else:
                # flash('Failed to add slot.', 'error')
                return jsonify({"error": "Failed to add slot."}), 500  # Return error response with status code
                   

        @app.route('/slot_management_editing/<slot_id>', methods=['GET','POST'])
        def slot_management_editing(slot_id):
            selected_slot_data = UserController.get_selected_slot_data(self.user_controller, slot_id)
            print(f"Hey here is the selected_slot_data for the selected slot id {slot_id}. Its data: {selected_slot_data}")
            if selected_slot_data:
                return render_template('slot_details.html', slot_data=selected_slot_data)
            else:
                # return render_template('error.html', message='Slot not found'), 404
                return redirect(url_for('success', message='Slot Not Found!', redirect_url=url_for('slot_management')))
        
        @app.route('/update_slot/<slot_id>', methods=['POST'])
        def update_slot(slot_id):
            updated_status = request.form['slot_status']
            print(f"here is the updated_status: {updated_status}")
            updated_available = True if 'available_for_use' in request.form else False
            print(f"here is the updated_available: {updated_available}")

            UserController.update_slot_data(self.user_controller, slot_id, updated_status, updated_available)

            return redirect(url_for('slot_management'))
        
        # @app.route('/slot_management/<slot_id>/delete', methods=['POST'])
        @app.route('/slot_management_delete/<slot_id>', methods=['GET','POST'])
        def slot_management_delete(slot_id):
            selected_slot_data = UserController.get_selected_slot_data(self.user_controller, slot_id)
            print(f"Hey here is the selected_slot_data for the selected slot id {slot_id}. Its data: {selected_slot_data}")
            if request.method == 'POST':
                confirmed = request.form.get('confirmed') 
                if confirmed:
                    if UserController.delete_slot_data(self.user_controller, slot_id):
                        message = request.args.get('message', 'Slot deleted successfully!')
                        redirect_url = request.args.get('redirect_url', url_for('slot_management'))
                        return render_template('success_page.html', message=message, redirect_url=redirect_url)
                    else:
                        message = request.args.get('message', 'Slot not found!')
                        redirect_url = request.args.get('redirect_url', url_for('slot_management'))
                        return render_template('success_page.html', message=message, redirect_url=redirect_url)
                else:
                    flash('Deletion canceled', 'info')
                    return redirect(url_for('slot_management'))  
            else:
                return render_template('slot_delete.html')

        @app.route('/admin', methods=['GET'])
        def admin_page():
            # Check if the user is logged in and has admin role
            if 'user_id' in session and 'username' in session:
                user = UserController.get_user_registration_data(self.user_controller, session['user_id'])
                # if user.role == 'admin':
                # if user['role'] == 'admin':
                # if user.get('phone') == 'm':
                if user.get('role') == 'admin':
                    # Get a list of all users (you need to implement this method)
                    all_users = self.user_controller.get_all_users()
                    all_booking_time_data = self.user_controller.get_all_time_data()
                    all_payment_data = self.user_controller.get_all_payment_data()
                    all_pparking_slots_available_data = self.user_controller.get_all_parking_slots_available_data()

                    # Render the admin page with the list of users
                    return render_template('admin_page.html', all_users=all_users,all_booking_time_data =all_booking_time_data, all_payment_data =all_payment_data, all_pparking_slots_available_data = all_pparking_slots_available_data )

            # If not an admin or not logged in, redirect to login
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('login'))
                    
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                # Authenticate  user
                user_authenticated, user_id, user_role   = UserController.authenticate_user(self.user_controller, username, password)
                if user_authenticated:
                    session['user_id'] = user_id
                    session['username'] = username 
                    # admin_user = self.user_controller.get_user_registration_data(session['user_id'])
                    # if admin_user.role == 'admin':
                    print(user_role)
                    if user_role == 'admin':
                        # return render_template('admin_page.html')
                        return redirect(url_for('admin_page'))
                    else:
                        # flash('Login Successful', 'success')
                        return redirect(url_for('home'))
                else:
                    flash('Invalid username or password. Please try again.', 'error')
            return render_template('login_page.html')
        
        # @app.route('/login')
        # def login():
        #     return render_template('login_page.html')
        #     self.login_page.show()


        # @app.route('/register/<session_id>', methods=['GET', 'POST'])
        # def registration(session_id):

        # @app.route('/register/<session_id>')
        @app.route('/register/<place_holder_user_id>', methods=['GET', 'POST'])
        def registration(place_holder_user_id):
            
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                phone = request.form.get('phone')
                email = request.form.get('email')
                carmanufacturer = request.form.get('carmanufacturer')
                carmodel = request.form.get('carmodel')
                car_plate = request.form.get('car_plate')
                role = request.form.get('role')
                user_id = str(uuid.uuid4())
                # Create UserModel instance
                user_model = UserModel(user_id, None, username, password, phone, email, carmanufacturer, carmodel, car_plate, role)
                # Register the user
                registration_successful = UserController.register_user(self.user_controller, user_model)
                # registration_successful = self.page_controller.user_controller.register_user(user_model)

                if registration_successful:
                    # Setingt the user_id in the session for future reference
                    session['user_id'] = user_id
                    session['username'] = username
                    flash('Registration Successful! You can now log in.', 'success')
                    return redirect(url_for('success', message='Registration Successful!', redirect_url=url_for('login')))

                    return redirect(url_for('home'))
                    return redirect(url_for('registration_success'))
            if request.method == 'GET':
                if place_holder_user_id == "new_user":
                    print(f'A newbie here about to create an account')
                    return render_template('registration_page.html')
                else:
                    user_registration_data =  self.user_controller.get_user_registration_data(place_holder_user_id)
                    print(f'This is the data that the user is to edit for him/herself {user_registration_data}')
                    return render_template('registration_page.html', user_registration_data = user_registration_data)
        
        @app.route('/success')
        def success():
            message = request.args.get('message', 'Operation Successful!')
            # duration = request.args.get('d\uration') 
            redirect_url = request.args.get('redirect_url', url_for('home'))
            return render_template('success_page.html', message=message, redirect_url=redirect_url)

        @app.route('/registration-success')
        def registration_success():
            message = request.args.get('message', 'Registration Successful!')
            return render_template('registration_success.html', message=message)

        # @app.route('/registration-success')
        # def registration_success():
        #     return 'Registration Successful!'

        # @app.route('/register')
        # def registration():
        #     return render_template('registration_page.html')

        @app.route('/home')
        def home():        
            try:
                user_id = session['user_id']
                user_registration_data =  self.user_controller.get_user_registration_data(session['user_id'])
                user, user_bookings, calculate_amount  =  self.user_controller.get_user_booking_data(session['user_id'])
                latest_booking_id  = "available_tickets"
                # Sample parking slots data (will be replaced by dynamic data later)
                parking_slots = parking_slots = UserController.get_all_parking_slots_available_data(self.user_controller)
                print(f'These is user_registration_data accessed when home is loaded  {user_registration_data}')

                # Rearranginh tume model to fing the duration difference
                # user_bookings = [TimeModel(**booking) for booking in user_bookings]
                return render_template('home_page.html', user_registration_data=user_registration_data, user=user, user_bookings=user_bookings, calculate_amount=calculate_amount, latest_booking_id=latest_booking_id, parking_slots=parking_slots)
            except KeyError:
                # If KeyError occurs (no 'user_id' in session), redirect to registration or login
                flash('Please log in or register to access the home page.', 'error')
                return redirect(url_for('login')) 
        
        # @app.route('/book', methods=['GET', 'POST'])
        # def booking():
        #     if request.method == 'POST':
        #         return redirect(url_for('success', message='Booking Successful!', redirect_url=url_for('home')))
        #     return render_template('booking_page.html')
        
        
        @app.route('/book', methods=['GET', 'POST'])
        def booking():
            if request.method == 'POST':
                user_id = session.get('user_id')  # storeD the userID in the session
                customer_number = UserController.get_customer_number(self.user_controller, user_id)

                # Get booking details from form
                arrival_date = request.form.get('arrival_date')
                arrival_time = request.form.get('arrival_time')
                departure_date = request.form.get('departure_date')
                departure_time= request.form.get('departure_time')

                # Create a TimeModel instance and filling details
                time_model = TimeModel(user_id, customer_number, None, arrival_date, arrival_time, departure_date, departure_time, None)

                 # Calculate duration before saving
                duration = time_model.calculate_duration()
                # duration = 0
                print(duration)
                duration_minutes = int(duration.total_seconds() / 60)
                print(f"Duration in minutes: {duration_minutes} minutes")

                if duration_minutes < 0:
                    flash('Invalid booking: Departure should be after arrival', 'error')
                    return redirect(url_for('booking'))
                
                # Create a TimeModel instance and filling details
                time_model = TimeModel(user_id, customer_number, None, arrival_date, arrival_time, departure_date, departure_time, duration_minutes)

                # Save the time entry to the data service controller
                specific_bookin_id = UserController.save_user_time_data(self.user_controller, time_model)
                
                flash('Booking Successful!', 'success')
                
                # Generate parking slot assignments
                all_booking_time_data = self.user_controller.get_all_time_data()
                # Load data from JSON file
                # with open('user_data/global_users_data/time_data.json', 'r') as file:
                #     all_booking_time_data = json.load(file)
                # parking_assignments  = UserController.assign_parking_slot(self.user_controller, all_booking_time_data)

                def convert_to_unix(self, date_str, time_str):
                    dt = datetime.datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
                    return int(dt.timestamp())

                def convert_to_datetime( unix_timestamp):
                    return datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M')
                latest_mod_ticket_details = UserController.get_selected_ticket_details(self.user_controller, specific_bookin_id)
                
                # parking_assignments  = UserController.assign_parking_slot(self.user_controller, latest_mod_ticket_details)
                parking_assignments, booking_message, error_message  = UserController.assign_parking_slot(self.user_controller, latest_mod_ticket_details)

                if parking_assignments == None:
                    error_message =  "Sorry, for the selected time range, all available slots are already booked. Kindly select another time range"


                if error_message:
                    flash(error_message, 'error')
                    return redirect(url_for('booking'))         

                def parking_assignments_to_json(self, assignments):
                    json_assignments = []
                    for assignment in assignments:
                        print("Assignment:", assignment)  
                        json_assignment = {
                            # "parking_slot_id": assignment['parking_slot_id'],
                            "parking_slot_id": assignment['parking_slot_id'],
                            "time_occupied_data": [
                                {"from": convert_to_datetime(time_range[0]), 
                                 "to": convert_to_datetime(time_range[1]), 
                                 "customer_number": time_range[2],
                                 "user_id":time_range[3],}
                                for time_range in assignment['time_occupied_data']
                            ]
                        }
                        json_assignments.append(json_assignment)
                    return json_assignments                       
                
                def append_parking_assignments_to_json(self, new_assignments):
                    # Load existing data from the JSON file
                    with open('user_data/global_users_data/slots_history_db.json', 'r') as json_file:
                        existing_assignments = json.load(json_file)

                    # Update existing data with new assignments
                    for new_assignment in new_assignments:
                        # Check if the parking slot exists in the existing data
                        slot_exists = False
                        for existing_assignment in existing_assignments:
                            if existing_assignment['parking_slot_id'] == new_assignment['parking_slot_id']:
                                # Append new time occupied data to the existing assignment
                                existing_assignment['time_occupied_data'].extend(new_assignment['time_occupied_data'])
                                slot_exists = True
                                break
                        if not slot_exists:
                            # If the parking slot doesn't exist, add it to the existing data
                            existing_assignments.append(new_assignment)

                    # Write the updated data back to the JSON file
                    with open('user_data/global_users_data/slots_history_db.json', 'w') as json_file:
                        json.dump(existing_assignments, json_file, indent=4)
                    # UserController.save_parking_slots_useage_history_json_data(self)
                    
                        
                # Save parking slot assignments to JSON file
                append_parking_assignments_to_json(self, parking_assignments_to_json (self, parking_assignments))


                # with open('user_data/global_users_data/slots.txt', 'w') as txt_file:
                #     for assignment in parking_assignments:
                #         txt_file.write(f"Parking Slot ID: {assignment['parking_slot_id']}\n")
                #         txt_file.write("Time_occupied_data:\n")
                #         for time_range in assignment['time_occupied_data']:
                #             txt_file.write(f"  - From: {convert_to_datetime(time_range[0])}, To: {convert_to_datetime(time_range[1])}, Customer Number: {time_range[2]}\n")
                #         txt_file.write("\n")
                    
            
                # return redirect(url_for('success', message='Booking SuIsiah Maxwell & ccessful!', duration=duration, redirect_url=url_for('home')))
                return render_template('booking_page.html', duration=duration, booking_successful=True, latest_booking_id=time_model.booking_id, booking_message= booking_message )
            
                return render_template('booking_page.html', duration=duration, booking=time_model.to_dict())
            return render_template('booking_page.html')
        

        @app.route('/extendbook', methods=['GET', 'POST'])
        def extendbook():
            user_id = session['user_id']
            # usercontroller = UserController()
            user_booked_ticket_ids = UserController.html_retrieve_user_ticket_ids(self.user_controller, user_id)
            if request.method == 'POST':
                # Retrieve form data
                extension_time = int(request.form.get('extension_time'))
                if extension_time > 300:
                    flash('Extension time cannot be greater than 300 minutes.', 'error')
                    return redirect(url_for('extendbook'))
                selected_ticket_id = request.form.get('ticket_id')
                # # Retrieve ticket details
                ticket_details = UserController.html_get_selected_ticket_details(self.user_controller, selected_ticket_id)
                print(ticket_details)

                # departure_time= request.form.get('departure_time')
                departure_time = ticket_details['departure_time']
                new_departure_time = UserController.calculate_new_departure_time(self.user_controller, departure_time, extension_time)
                print(new_departure_time)

                # Update the booking and capture the modified booking ID
                modified_booking_id = UserController.update_booking(self.user_controller, selected_ticket_id, new_departure_time, extension_time)

                if modified_booking_id:
                    flash('Booking Extended Successfully!', 'success')
                    return render_template('extend_booking_page.html', duration=extension_time, extended_booking_successful=True, latest_booking_id=modified_booking_id["booking_id"])
                else:
                    flash('Failed to extend booking.', 'error')
                    return redirect(url_for('extendbook'))
            return render_template('extend_booking_page.html', user_booked_ticket_ids=user_booked_ticket_ids)
        
        # # @app.route('/payment')
        # # @app.route('/payment/<latest_booking_id>')
        # @app.route('/payment/<latest_booking_id>')
        # def payment(latest_booking_id):
        #     # latest_ticket = self.user_controller.get_latest_modified_ticket()
        #     # return render_template('payment_page.html', latest_ticket=latest_ticket)
        #     latest_mod_ticket_details = self.user_controller.html_get_selected_ticket_details(latest_booking_id)
        #     return render_template('payment_page.html', latest_mod_ticket_details=latest_mod_ticket_details)

        # @app.route('/payment/<latestBookingId>', defaults={'latestBookingId': None})
        @app.route('/payment/<latest_booking_id>')
        def payment(latest_booking_id):
            print(latest_booking_id + " -this is the value of latest_booking_id") 
            if latest_booking_id != "available_tickets":
                print(latest_booking_id + " this should be executed if latest_booking_id has a value  -->(@app.route('/payment/<latest_booking_id>'))") 
                # If latestBookingId is provided, fetch details for that specific ticket
                latest_mod_ticket_details = UserController.html_get_selected_ticket_details(self.user_controller, latest_booking_id)
                return render_template('payment_page.html', latest_mod_ticket_details=latest_mod_ticket_details,selected_payment_data=None)
            else:
                print(latest_booking_id + " this should be executed if latest_booking_id has no value -->(@app.route('/payment/<latest_booking_id>'))") 
                # try:
                # If latestBookingId is not provided, fetch details for all tickets
                user_id = session['user_id']
                user_registration_data =  UserController.get_user_registration_data(self.user_controller, session['user_id'])
                user, user_bookings, calculate_amount  =  UserController.get_user_booking_data(self.user_controller, session['user_id'])
                return render_template('payment_page.html', user_registration_data=user_registration_data, user=user, user_bookings=user_bookings, calculate_amount=calculate_amount)
            
        @app.route('/get_selected_ticket_details', methods=['GET'])
        def get_selected_ticket_details():
            selected_ticket_id = request.args.get('ticket_id')
            details = UserController.html_get_selected_ticket_details(self.user_controller, selected_ticket_id)
            if details:
                return jsonify(details)
            else:
                return jsonify({"error": "Ticket ID not found"}), 404
            # details = {"arrival_date": "2024-02-15", "arrival_time": "12:30", "departure_date": "2024-02-16", "departure_time": "14:45"}
            # return jsonify(details)

        @app.route('/make_payment', methods=['GET', 'POST'])
        def make_payment():
            # Extract form data
            booking_id = request.form.get('booking_id')
            customer_number = request.form.get('customer_number')
            payment_type = request.form.get('payment_type', 'mpesa')  # Default to mpesa if not provided
            duration_minutes =  UserController.get_duration_by_booking_id(self.user_controller, booking_id)

            # Perform payment logic using the PaymentModel
            if duration_minutes is not None:      
                # amount = PaymentModel.calculate_amount(self, duration_minutes)
                amount = 0.8 * duration_minutes
                amount = round(amount, 2)
                payment_date = datetime.datetime.now().isoformat()
                payment_id = UserController.generate_payment_id(self.user_controller, booking_id)
                # payment_id = self.generate_parking_id(payment_data_collec_model.booking_id)
                payment_data_collec_model = PaymentModel(payment_id=payment_id, booking_id=booking_id, customer_number=customer_number, payment_date = payment_date, duration_minutes = duration_minutes, amount = amount, is_paid = True, payment_type=payment_type)

                # Set other payment details such as amount, payment_date, etc.
                payment_d_collect_successful = UserController.payment_data_collec_save(self.user_controller, payment_data_collec_model)

            if payment_d_collect_successful:
                # Payment data collection successful, redirect to a payment page with fillled data
                print("successfull")
                # fetch details for that specific ticket
                latest_mod_ticket_details = UserController.html_get_selected_ticket_details(self.user_controller,booking_id)
                payment_data = UserController.get_payment_data_by_payment_id(self.user_controller, payment_id)
                return render_template('payment_page.html', latest_mod_ticket_details=latest_mod_ticket_details, selected_payment_data=payment_data, payment_successful=True)
            else:
                print("operation failed")
                return render_template('booking_page.html')
                # Handle error scenario, maybe display an error message
                # return render_template('error.html', message='Payment data collection failed')
            
                
            # Save the payment details to your database or perform any other necessary actions

            # Redirect to a success page or back to home
            # return redirect('/success_page')
            # flash('Booking Successful!', 'success')

        # @app.route('/extend_parking')
        # def extend_parking():
        #     return self.extend_parking_page.show()

    def redirect_to(self, page_name):
        return redirect(url_for(page_name))

    def show_login_page(self):
        return self.redirect_to('login')

    # def show_registration_page(self):
    #     return self.redirect_to('registration')

    # def show_home_page(self):
    #     return self.redirect_to('home')
