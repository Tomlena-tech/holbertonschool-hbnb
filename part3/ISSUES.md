# Issues  and solutions for the project

1. Issue 1: Password Hashing and Verification in User Model
   - Solution: Implement password hashing using Flask-Bcrypt for user password storage and verification.
    - File: app/models/user.py
        - Implemented `hash_password` method to hash passwords before storing them.
        - Implemented `verify_password` method to verify provided passwords against stored hashed passwords.



2. Issue 2: importing bcrypt correctly (circular import issue)
   - Solution: Adjusted imports to use `current_app` to access the bcrypt extension within the User model.
    - File: app/models/user.py
        - Changed import statements to use `from flask import current_app`.
        - Accessed bcrypt via `current_app.extensions['bcrypt']` within methods.