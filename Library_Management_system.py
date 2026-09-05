import mysql.connector

try:
    con = mysql.connector.connect(
        host="localhost",
        password="1234",
        user="root",
        database="library_db",
        charset="utf8",
        autocommit=True
    )
except mysql.connector.Error as err:
    print(f"\n✘ Could not connect to MySQL: {err}\n")
    exit()

c = con.cursor(buffered=True)  # buffered cursor avoids lazy-loaded results

c.execute("create database if not exists library_db")
c.execute("use library_db")
c.execute("""create table if not exists books(
    b_id varchar(5) primary key,
    b_name varchar(50),
    author varchar(50),
    available varchar(5) default 'yes')""")
c.execute("""create table if not exists issue_details(
    b_id varchar(5),
    student_id varchar(10),
    student_Name varchar(50) not null,
    foreign key(b_id) references books(b_id))""")


def add_book():
    print()
    bid = input("Enter BOOK ID: ")
    title = input("Enter BOOK Name: ")
    author = input("Author name: ")
    try:
        c.execute(
            "insert into books(b_id, b_name, author) values (%s, %s, %s)",
            (bid, title, author)
        )
        print(f"\n✔ Book '{title}' (ID: {bid}) added successfully.\n")
    except mysql.connector.Error as err:
        print(f"\n✘ Could not add book: {err}\n")


def delete_book():
    print()
    bid = input("Enter BOOK ID: ")

    c.execute("select * from books where b_id=%s", (bid,))
    if c.fetchone() is None:
        print(f"\n✘ No book found with ID {bid}. Nothing was deleted.\n")
        return

    try:
        c.execute("delete from books where b_id=%s", (bid,))
        print(f"\n✔ Book ID {bid} deleted.\n")
    except mysql.connector.Error as err:
        print(f"\n✘ Could not delete book (it may currently be issued): {err}\n")
        return

    display_books()


def issue_book():
    print()
    s_name = input("Enter your Name: ")
    s_id = input("Enter Reg No: ")
    book = input("Enter Book name: ")

    c.execute("select b_id from books where b_name=%s and available='yes'", (book,))
    result = c.fetchone()

    if result is None:
        print("\n✘ Sorry, that book is not available or doesn't exist.\n")
        return

    bid = result[0]
    c.execute(
        "insert into issue_details(b_id, student_id, student_Name) values (%s, %s, %s)",
        (bid, s_id, s_name)
    )
    c.execute("update books set available='no' where b_id=%s", (bid,))
    print(f"\n✔ '{book}' issued to {s_name}.\n")


def return_book():
    print()
    name = input("Enter your name: ")
    bid = input("Enter book id: ")

    # Check the book was actually issued before claiming success
    c.execute("select * from issue_details where b_id=%s", (bid,))
    if c.fetchone() is None:
        print(f"\n✘ Book ID {bid} was not found in issued records. Nothing to return.\n")
        return

    c.execute("update books set available='yes' where b_id=%s", (bid,))
    c.execute("delete from issue_details where b_id=%s", (bid,))
    print(f"\n✔ Book ID {bid} returned by {name}.\n")


def display_books():
    c.execute("select * from books")
    results = c.fetchall()
    print()
    print(f"{'Book ID':<10}{'Book Title':<25}{'Author':<20}{'Available':<10}")
    print("-" * 65)
    if not results:
        print("No books in the system yet.")
    for row in results:
        print(f"{row[0]:<10}{row[1]:<25}{row[2]:<20}{row[3]:<10}")
    print()


def select_book():
    print()
    book = input("Enter the name of the book: ")
    c.execute("select * from books where b_name=%s", (book,))
    results = c.fetchall()
    print()
    if not results:
        print(f"No book found with the name '{book}'.\n")
        return
    print(f"{'Book ID':<10}{'Book Title':<25}{'Author':<20}{'Available':<10}")
    print("-" * 65)
    for row in results:
        print(f"{row[0]:<10}{row[1]:<25}{row[2]:<20}{row[3]:<10}")
    print()


def display_issued_books():
    c.execute("""select issue_details.*, books.b_name
                 from issue_details join books on issue_details.b_id = books.b_id""")
    results = c.fetchall()
    print()
    if not results:
        print("No books are currently issued.\n")
        return
    print(f"{'Book ID':<10}{'Book Name':<25}{'Reg No':<12}{'Student Name':<20}")
    print("-" * 67)
    for row in results:
        print(f"{row[0]:<10}{row[3]:<25}{row[1]:<12}{row[2]:<20}")
    print()


def main():
    print("=" * 50)
    print("   WELCOME TO THE LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)
    user_name = input("\nEnter username: ")
    ps = input("Enter password: ")

    if user_name == 'admin' and ps == 'library123':
        print("\n✔ Welcome Admin\n")
        while True:
            print("=" * 50)
            print(" LIBRARY MANAGEMENT SYSTEM")
            print("=" * 50)
            print(" 1. Add book        2. Issue book     3. Return book")
            print(" 4. Display books   5. Delete book    6. Exit")
            print("-" * 50)
            ch = input("Enter your choice: ")

            if ch == '1':
                add_book()
            elif ch == '2':
                issue_book()
            elif ch == '3':
                return_book()
            elif ch == '4':
                print()
                print(" 1. All books   2. Issued books   3. Particular book")
                sub_choice = input("Choose one: ")
                if sub_choice == '1':
                    display_books()
                elif sub_choice == '2':
                    display_issued_books()
                elif sub_choice == '3':
                    select_book()
                else:
                    print("\n✘ Wrong choice\n")
            elif ch == '5':
                delete_book()
            elif ch == '6':
                print("\nGoodbye!\n")
                break
            else:
                print("\n✘ Invalid choice, try again\n")
    else:
        print("\n✘ Wrong username or password, try again\n")


if __name__ == "__main__":
    main()
