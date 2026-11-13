from werkzeug.security import generate_password_hash

password = input("Enter your new admin password: ")

print("\nYour password hash is:\n")
print(generate_password_hash(password))
