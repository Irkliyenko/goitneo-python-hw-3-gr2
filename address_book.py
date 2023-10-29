from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 and not value.isnumeric():
            raise ValueError("Phone number must have 10 digits and numeric.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError(
                "Birthday should be in the following format: dd.mm.yyyy")
        self.value = value.date()

    def __str__(self):
        return datetime.strftime(self.value, '%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return self.phones

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
        return self.phones

    def edit_phone(self, new_phone, old_phone=None, index=0):
        new_phone = Phone(new_phone)
        if old_phone:
            for idx, p in enumerate(self.phones):
                if p.value == old_phone:
                    self.phones[idx] = new_phone
            return self.phones
        else:
            if 0 <= index < len(self.phones):
                self.phones[index] = new_phone
            return self.phones

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        else:
            return "This phone is not in the contact list."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return "User was not found."

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return self.data
        else:
            return "User was not found."

    def get_birthday_per_week(self):

        # set up todays date
        today = datetime.today().date()

        birthday_ppl = {}

        # function itterates over each user in users list, check their birthday's date,
        # and change it to type(data).
        for name, record in self.data.items():
            birthday = record.birthday
            if not birthday:
                continue

            birthday_this_year = birthday.value.replace(year=today.year)

            # checks if bithday alr happend this year
            if birthday_this_year < today:
                birthday_next_year = birthday_this_year.replace(
                    year=today.year + 1)
                delta_days = (birthday_next_year - today).days

            # calculate how much days left from today to the birday of the user
            else:
                delta_days = (birthday_this_year - today).days

            # checks if the birday is in less that 7 days and is not today
            if 0 < delta_days < 7:

                # if birthday is during the week day, add it to the dict{day:name}
                if birthday_this_year.weekday() <= 4:
                    day_name = birthday_this_year.strftime('%A')
                    if day_name not in birthday_ppl:
                        birthday_ppl[day_name] = [name]
                    else:
                        birthday_ppl[day_name].append(name)

                # if birthday is on the weekend, add it to the following Monday (dict{following_monday:name})
                elif birthday_this_year.weekday() >= 5:
                    days_until_monday = (7 - today.weekday()) % 7
                    following_monday = today + \
                        timedelta(days=days_until_monday)
                    day_name = following_monday.strftime("%A")
                    if day_name not in birthday_ppl:
                        birthday_ppl[day_name] = [name]
                    else:
                        birthday_ppl[day_name].append(name)

        if birthday_ppl:
            return "\n".join(f'{day}: {", ".join(names)}' for day, names in birthday_ppl.items())
        return "No birthdays this week"

    def __str__(self):
        return "\n".join(str(rec) for rec in self.data.values())


if __name__ == '__main__':
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    print(john_record)

    # Додавання запису John до адресної книги
    book.add_record(john_record)
    a = book.find("John")
    print(f"John record: {a}")

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("30.10.1990")
    book.add_record(jane_record)
    print(jane_record)
    jane_record.edit_phone("9876543210", "0674563434")
    b = book.find("Jane")
    print(f"Jane record: {b}")

    luke_record = Record("Luke")
    luke_record.add_phone("9876543210")
    luke_record.add_birthday("3.11.1990")
    book.add_record(luke_record)
    c = book.find("Luke")
    print(c)
    luke_record.edit_phone("9876543210", "1234567890")
    book.add_record(luke_record)
    d = book.find("Luke")
    print(d)
    print(book.find("Luke"))

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(f"Record: {record}")
    print(book)

    print(book.get_birthday_per_week())
