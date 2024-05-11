# TicketShow v2 

## Description:
    TicketShow is a web-based application made with Vue3 and Python-Flask. It enables multiple 
    admins to create shows in respective theaters. It enables multiple users to browse through 
    the shows and book tickets. It facilitates users to search the shows based on genre and search 
    theaters based on location. It also allows the user to voice their opinions on shows by 
    providing reviews.


## Technologies Used:

-   **Python:** responsible for developing the controllers and serving
    as the host programming language for the app

-   **Vue:** used to develop the front-end of the app

-   **CSS:** responsible for styling the web-pages

-   **Bootstrap:** used to make the front-end appealing and easy to
    navigate

-   **SQLite:** serves as the database for the app

-   **Flask:** serves as the web-framework for the app

-   **Flask-Restful:** used to develop the RESTful API for the app

-    **Flask-Security:** used for authentication and role based access control

-   **Flask-SQLAlchemy:** used to access and modify the apps SQLite database

-   **Flask-Celery**: used for asynchronous background jobs at the backend

-   **Flask-Caching**: used for caching API outputs and increasing
    performance

-   **Redis**: used as an in-memory database for the API cache and as a
    message broker for celery

-   **MailHog**: sed for mailing purpose when the background job is triggered.

## API Design:

A REST API for Ticket show app was made with Flask-RESTful module. It has:
 * Endpoints for basic CRUD operations on theaters, shows only for admin
 * Endpoints for ratings, bookings for users
 * Other endpoints for frontend rendering
Authentication tokens and roles are used for specific requests that requires them. These 
tokens are obtained as json data with query param of include_auth_token in flask-security. 
The role authentication is implicitly handled by Flask-security.

## Architecture and Features:

The architecture of Ticket-Show follows client-server model, where Vue servers as the 
frontend framework and Flask as the backend framework. Vue handles the presentation layer 
and manages the user/admin interactions, while Flask handles the server-side logic, such as 
HTTP requests and responses, async tasks and database interaction

The features of the application are as follows:

-   **User authentication**: Signup and Login

-   **Admin authentication**:  Admin Login

**ADMIN**

-   **Show management**: Create, view, update and delete shows

-   **Theater management**: Create, view, update and delete theaters

-   **Data Export**: : Download theater’s details and stats as CSV file from mail

-   **Data export**: Download user\'s posts and analytics as a CSV file

**USER**
-   **Explore shows**: View shows for booking based on search results of genre

-   **View theaters**: : View theaters based on location searches

-   **Voice Opinions**: : Users can provide review and ratings for the shows booked

-   **Users profile**: : User details and reviews provided by them are shown.

-   **Reminders**: Receive daily reminders to post

-   **Monthly entertainment report**: Receive a report as an email summarizing bookings for the month


## Instructions for running the application


1. Navigate to the root folder of the application.
2. Open two separate terminals and execute the following commands in each:

    * `redis-server`
    * `mailhog`
3. Navigate to the backend folder and open three separate terminals. Execute the following commands in each:

    * `python main.py`
    * `celery -A main.celery worker -l info`
    * `celery -A main.celery beat --max-interval 1 -l info`
4. Navigate to the frontend folder.
5. In the terminal, execute the following command:

    * `npm run serve`

These steps will successfully run the application, allowing you to access it from your web browser at [http://localhost:8080](http://localhost:8080).
