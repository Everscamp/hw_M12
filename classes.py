from collections import UserDict
from datetime import date, datetime
from random import randint
import re 


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.__value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 0:
            self.__value = value
        else:
            raise ValueError

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_val = datetime.strptime(re.sub(r'[.-/]', ' ', value), '%d %m %Y')

        if isinstance(new_val, date):
            self.__value = new_val
        else:
            raise ValueError
            
class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)    
        except ValueError:
            print('Wrong phone format!')
    
    def add_birthday(self, birthday):
        if birthday != None:
            try:
                self.birthday = Birthday(birthday)  
            except ValueError:
                print('Wrong date format! Enter the date in format day-month-year or day.month.year.')

    def remove_phone(self, phone):
        phone_num = Phone(phone)

        for i in filter(lambda i: i.value == phone_num.value, self.phones):
            self.phones.remove(i)
    
    def edit_phone(self, old_phone, new_phone):
        try:
            old, new = Phone(old_phone), Phone(new_phone)

            for i in self.phones:
                if i.value == old.value:
                    self.phones.remove(i)
                    self.phones.append(new)
        except ValueError:
                print('Failed to edit the number! Wrong phone format or no phone existed.')

    def find_phone(self, phone):
        try:
            phone_num = Phone(phone)
            for i in filter(lambda i: i.value == phone_num.value, self.phones):
                return phone_num.value
        except ValueError:
                print('Failed to find the number! Wrong phone format or no phone existed.')

    def days_to_birthday(self):
        modified_date = self.birthday.value.replace(year=date.today().year + 1) \
            if self.birthday.value.month == 1 \
            else self.birthday.value.replace(year=date.today().year)
        
        result = modified_date.date() - date.today()

        return result

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    min_len = 0

    def add_record(self, record: Record):
        try:
            self.data[record.name.value] = record   
        except ValueError:
            print('Failed to add the record!')

    def find(self, name):
        return self.data[name] if name in self.data else None

    def delete(self, name):
        self.data.pop(name) if name in self.data else None

    def __iter__(self):
        return self

    # виводить увесь список
    def __next__(self):
        if self.min_len == len(self.data.values()):
            raise StopIteration
        else:
            value = list(self.data.values())[self.min_len]
            self.min_len += 1

            return value

    # посторінкове виведення списку
    def custom_iterator(self, end):
        while end+self.min_len <= len(self.data.values()):
            string_view = ''
            result = list(self.data.values())[self.min_len:end+self.min_len]
            for i in result:
                string_view += f'{i}\n'
            
            yield string_view
            
            self.min_len += end+self.min_len

        raise StopIteration

# тут додала ту перевірку з LMS з минулих ДЗ
if __name__ == '__main__':
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("20/01/1994")
    print(john_record)

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value}: {found_phone}")

    # Видалення запису Jane
    book.delete("Jane")

    # Перевірки для модуля 11
    
    # Кількість днів до наступного дня народження контакту
    found_date = john.days_to_birthday()
    print(found_date)
   
    # Додаю 20 рандомних записів
    for i in range(20):
        new_record = Record(f"John Dou_{i}")
        new_record.add_phone(str(randint(1000000000, 9000000000)))
        book.add_record(new_record)

    # Посторінковий висновок, виведення записів через ітератор по 5 записів
    newiter = book.custom_iterator(5)
    
    print(next(newiter))
    print(next(newiter))