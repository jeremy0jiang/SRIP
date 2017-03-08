Server-side Chat

Files to modify/complete :

1) layout.html
	- Make sure to follow the example in class to create your layout template. You can also reference Flask docs for help: http://flask.pocoo.org/docs/0.12/tutorial/templates/
2) index.html
	- Extend the layout and produce the main chat window
3) userprofile.html
	- Extend the layout and produce the user profile
4) style.css
	- Stylize your two pages
5) env.py
	- After creating your database, enter your credentials here
6) models.py
	- Create your database structure here similarly to how we did the example in class. You will have at least two tables in your database, users and messages, but you are free to add more if you think you will need them
	- Your tables can contain whatever fields you need, but at the very least, the messages table ought to be able to contain the chat messages posted by the users
7) chat_app.py
	- Complete the 4 routes to produce the relevant views/data. You may add additional routes as you see fit, but these 4 are mandatory.
	- GET / should query the database and assemble the sidebar with the users list and the main chat window with the list of messages
	- GET /user/user_id should query the database for the user information and render the profile view
	- GET /messages and GET /users simply duplicate those database queries and return the collection (we will use these in the next assignment)
8) requirements.txt
	- Be sure replace this file with your requirements.txt file as demonstrated in class

Note: for now, just populate your database manually. In subsequent assignments, we will be adding layers to submit data to the database from the client-side as well.