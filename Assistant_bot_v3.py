from address_book import Record, AddressBook


# Function to parse user input into a command and its arguments
def parse_input(user_input):
    # Split the user input into command and arguments
    cmd, *args = user_input.split()
    # Remove leading and trailing spaces from the command, and convert it to lowercase for consistency
    cmd = cmd.strip().lower()
    return cmd, *args


# Decorator that handles possible errors during execution of functions
def contacts_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input. Enter name and numeric phone number that has 10 digits."
        except IndexError:
            return "Invalid number of arguments. Please try again."
        except KeyError:
            return "Contact was not found. Ensure that you enter the right name and try again."
    return inner

# Decorator that handles the error when the user enter birthday in wrong format


def birthday_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return ("Birthday should be in the following format: dd.mm.yyyy")
    return inner


# Decorator that handles possible errors during execution of show_all function
def show_all_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "The list of contacts is empty! Add the contact first."
    return inner


# adds name and number to the dict contats
@contacts_error
def add_contact(args, contacts):
    name, phone = args
    if name == "username" or not phone.isnumeric() or len(phone) != 10:
        raise ValueError
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        print(contacts)
        return "Contact added."


# overwrites existed phone number to the new one if user approves that, If contact is not on the
# the list, it raises the error
@contacts_error
def change_phone(args, contacts):
    name, new_phone = args
    user = contacts.find(name)
    print(user)
    if user:
        user_input = str(input(
            "Existing contact will be overwritten. If you want to continue enter 'Yes', if not enter 'No' >>> "))
        if user_input.lower() == "yes":
            user.edit_phone(new_phone)
            return "Contact changed."
        elif user_input.lower() == "no":
            return "Contact not changed."
        else:
            return "Invalid input. Enter yes or no."
    else:
        raise KeyError


# show the phone number for a specific user name. It will inform user if pnone number is not found
@contacts_error
def show_phone(args, contacts):
    name = args[0]
    user = contacts.find(name)
    if user:
        return ', '.join(str(phone) for phone in user.phones)
    else:
        raise KeyError


# shows all numbers in the list. It will inform user if the contact list is empty
@show_all_error
def show_all(contacts):
    if len(contacts.data) >= 1:
        contact_list_str = "\n".join(
            f"Phone: {', '.join(str(phone) for phone in record.phones)}" for record in contacts.data.values())
        return contact_list_str
    else:
        raise ValueError


# Add birthday to the record
@birthday_error
def add_birthday(args, contacts):
    name, birthday = args
    user = contacts.find(name)
    if user:
        user.add_birthday(birthday)
        return "Birthday added."
    else:
        raise ValueError


# Show birthday of a specific contact if this contact exists in address book
@contacts_error
def show_birthday(args, contacts):
    name = args[0]
    user = contacts.find(name)
    if user:
        return str(user.birthday)
    else:
        raise KeyError


# show contacts who has birthday in the following week
def birthdays(contacts):
    return contacts.get_birthday_per_week()


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    # Start an infinite loop to continuously prompt the user for commands
    while True:
        # Prompt the user to enter a command and parse the input
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello" or command == "hi":
            print("How can I help you?")
        # Add a new contact to the list
        elif command == "add":
            print(add_contact(args, contacts))
        # Change the phone number of an existing contact
        elif command == "change":
            print(change_phone(args, contacts))
        # Show the phone number of a specific contact
        elif command == "phone":
            print(show_phone(args, contacts))
        # Show all phone numbers in the list of contacts
        elif command == "all":
            print(show_all(contacts))
        # Add birthday to the contact
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        # Show birthday of an existing contact
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        # Show bisthday info for all contacts
        elif command == "birthdays":
            print(birthdays(contacts))
        # Handle invalid commands
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
