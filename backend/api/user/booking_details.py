from flask_restful import Resource, reqparse

from flask_security import current_user, auth_required, roles_required
from application.data_access import get_booking_details
from application.validation import  UnAuthorizedError






class User_Booking_Details(Resource):
    @auth_required('token')
    @roles_required('user')

    def get(self, user_id):

        b_details = get_booking_details(user_id)

        if user_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')

        return [{
            "id":booking_details.id,
            "num_of_tickets":booking_details.num_of_tickets,
            "tot_cost":booking_details.tot_cost,
            "show_booked":booking_details.show_booked.show_name,
            "theater_booked":booking_details.show_booked.theater.theater_name,
            "theater_place":booking_details.show_booked.theater.t_place,
            "theater_location":booking_details.show_booked.theater.location,
            "user_id":current_user.id,
            "theater_id":booking_details.theater_id,
            "show_id":booking_details.show_id
        } for booking_details in b_details],200