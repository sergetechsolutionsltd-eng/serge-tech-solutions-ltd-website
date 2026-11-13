
from werkzeug.security import generate_password_hash

password = input("Enter your admin password: ")
print(generate_password_hash(password))
