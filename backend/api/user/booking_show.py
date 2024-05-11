from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required, roles_required
from application.models import db,  Show, BookingShow
from application.validation import NotFoundError, UnAuthorizedError


book_tik = reqparse.RequestParser()
book_tik.add_argument('no_of_tickets', type=int, required=True)



class Booking_Ticket(Resource):
    @auth_required('token')
    @roles_required('user')
    def post(self,t_id,s_id,u_id):
        s_details = Show.query.get(s_id)

        if u_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')

        if s_details:
            args = book_tik.parse_args()
            no_of_tickets = args.get('no_of_tickets')
            
            seats_available = s_details.theater.seat_capacity - s_details.seat_booked
            if no_of_tickets > seats_available:
                return{
                    "message":"Housefull... Choose another show and enjoy!!"
                },405

            tot_cost = float(s_details.price)*float(no_of_tickets)

            ticket_booked = BookingShow(user_id = current_user.id, show_id = s_id, theater_id = t_id, num_of_tickets = no_of_tickets,
                                        tot_cost=tot_cost)
            
            s_details.seat_booked += int(no_of_tickets)

            # seats_available = s_details.theater.seat_capacity - s_details.seat_booked

            # if seats_available < s_details.seat_booked:
            #     return{
            #         "message":"Housefull... Choose another show and enjoy!!"
            #     },405
            
            db.session.add(ticket_booked)
            db.session.commit()
            print('--------------------------Ticket Booked-------------------------')

            return {
                "message":"Booking Successful"
            },200
        raise NotFoundError(400,'NF1001','Show doest exist')
    
    @auth_required('token')
    @roles_required('user')
    def get(self,u_id,t_id,s_id):
        s_details = Show.query.get(s_id)
        seats_available = s_details.theater.seat_capacity - s_details.seat_booked
        if seats_available > 0:
            return {
                'seats_available':seats_available
            },200
        return{
            'seats_available':'HOUSEFULL'
        }
    

class CancelBooking(Resource):
    @auth_required('token')
    @roles_required('user')
    def delete(self,t_id,s_id,u_id,b_id):
        booked_ticket = BookingShow.query.get(b_id)

        if u_id != current_user.id:
            raise UnAuthorizedError(401,'NA1001','Not allowed to access other users')

        if not booked_ticket:
            return {'message':'Cannot cancel ticket which isnt booked'}

        booked_ticket.show_booked.seat_booked -= booked_ticket.num_of_tickets

        db.session.delete(booked_ticket)
        db.session.commit()
        print('--------------------Ticket Cancelled------------------')
        return {
            'message':'Cancel Successful'
        },200