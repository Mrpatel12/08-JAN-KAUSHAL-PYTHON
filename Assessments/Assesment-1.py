import datetime

users = []
posts = []

def register():
    print("\n----- Register -----")
    
    username = input("Enter username: ").strip()
    
    if username == "":
        print("Username cannot be empty!")
        return
    
    for user in users:
        if user["username"] == username:
            print("Username already exists!")
            return
    
    password = input("Enter password: ").strip()
    
    if password == "":
        print("Password cannot be empty!")
        return
    
    users.append({
        "username": username,
        "password": password
    })
    
    print("Registration successful!")

def login():
    print("\n----- Login -----")
    
    username = input("Username: ")
    password = input("Password: ")
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return username
    
    print("Invalid username or password")
    return None

def create_post(current_user):
    print("\n----- Create Post -----")
    
    title = input("Enter Post Title: ").strip()
    if title == "":
        print("Title cannot be empty")
        return
    
    description = input("Enter Description: ").strip()
    if description == "":
        print("Description cannot be empty")
        return
    
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    
    post = {
        "author": current_user,
        "title": title,
        "description": description,
        "date": date
    }
    
    posts.append(post)
    
    print("Post created successfully!")

def view_posts():
    
    print("\n----- All Posts -----")
    
    if len(posts) == 0:
        print("No posts available.")
        return
    
    for p in posts:
        print("\n-----------------------")
        print("Author :", p["author"])
        print("Title  :", p["title"])
        print("Date   :", p["date"])
        print("Description :", p["description"])
        print("-----------------------")

def search_post():
    
    username = input("Enter username to search posts: ")
    
    found = False
    
    for p in posts:
        if p["author"] == username:
            print("\n-----------------------")
            print("Author :", p["author"])
            print("Title  :", p["title"])
            print("Date   :", p["date"])
            print("Description :", p["description"])
            print("-----------------------")
            found = True
    
    if not found:
        print("No posts found for this user.")

def dashboard(current_user):
    
    while True:
        print("\n--- PostBoard Dashboard ---")
        print("1. Create Post")
        print("2. View All Posts")
        print("3. Search Posts by Username")
        print("4. Logout")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            create_post(current_user)
        
        elif choice == "2":
            view_posts()
        
        elif choice == "3":
            search_post()
        
        elif choice == "4":
            print("Logged out successfully.")
            break
        
        else:
            print("Invalid choice!")

def main():
    
    while True:
        print("\n===== PostBoard =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            register()
        
        elif choice == "2":
            user = login()
            if user:
                dashboard(user)
        
        elif choice == "3":
            print("Exiting PostBoard...")
            break
        
        else:
            print("Invalid choice!")

main()