# CSC480_Project

------------------CSC480 Ticketing System Demo for Contra Costa County---------------------------

------Description-------
This web-app functions as a ticketing system for a User class to create tickets, and a responder class Employee to view all tickets in a ticket hub that 
belong to their department, grab the ticket, and move them to their personal ticket hub.
The ticket class will be visible for both active participants, and will allow both participants to enter comments, provide updates, and change the status of the active ticket.
All changes will be based to the database with a POST request, whether it be account creation, ticket creation, ticket deletion, etc. 
All Users, Employees, and tickets are stored in instance/database.db

Designed to run on the local machine as a server, nothing is currently being uploaded. 

------- requirements ---------
Required dependencies are:
- python 3.4 or newer
- pip (optional but recommended)
- install flask
- install flask-login
- install sqlalchemy
- jinja2
- install flask_sqlalchemy
- DBBrowser for SQLite (optional but recommended)

To Check, use the following commands:
- pip --version
- py --version
- pip list


TODO:
- develop Employee class
  - develop employee view/endpoint... how will it work?
  
- Department view where all unclaimed tickets for a department can be seen
- Users view add a side panel? 
  
