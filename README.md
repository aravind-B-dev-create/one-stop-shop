# Blogger
Level 4 Evaluation for Aravind Balasubramanian (instructor: Saisumana Perumalla)
At the home page there are two interactable buttons - register and login which create accounts and can log the user into their homepage
The homepage HTML is found in the account_page.html file. A logout button and a button to add new posts is present here.
The delete button clears the user from the session and brings them back to the index.html page
The create a post button creates posts and stores them in the database (MongoDB). 
There are two collections within the database, one for accounts and one for blogs. Each blog as a user_name attribute that corresponds to an account within the account collection. Every blog by every user is displayed in the index.html page, however user specific blogs are shown depending on which user is logged into the account_page.html page at that time. There is also a delete button on the blog itself which clears the database of the blog and redirects the user back to the account_page.html
