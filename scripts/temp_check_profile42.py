import os

p = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max\Profile 42"
print(f"Path exists: {os.path.exists(p)}")
if os.path.exists(p):
    files = os.listdir(p)[:10]
    print("Files in Profile 42:", files)
