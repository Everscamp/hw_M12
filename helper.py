import re
import classes
import csv


contacts = {}
phone_pattern = r'\d+'
name_pattern = r'[a-zA-Z_]+'
operator_pattern = r'(birthday)|(delete phone)|(show all)|(good bye)|[a-zA-Z_]+\s?'
phone_operator_pattern = r'(add)|(change)|(delete phone)'
book = classes.AddressBook()

# Remove spaces at the beginning and at the end of the string and lower case the string
def operator_handler(operator):
    parced_operator = re.search(operator_pattern, operator)
    return parced_operator.group().lower().strip()

# Defines name and telephone number
def operand_maker(operator):
    operands = []
    trimmedContact = re.sub(phone_operator_pattern, '', operator)
    
    phoneName = re.search(name_pattern, trimmedContact)
    phoneNums = re.findall(phone_pattern, trimmedContact)
    
    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneName.group().capitalize())
    
    if not phoneNums:
        raise Exception('No number? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneNums)

    return operands

#Simple welcome function
def hello(operator):
    return 'How can I help you?'

# Adds a phone number to the contacts list
def add(operator):
    phoneName = operand_maker(operator)[0]
    phoneNum = operand_maker(operator)[1]

    record = book.find(phoneName)
    if record != None:
        record.add_phone(phoneNum[0])

        return f'Phone to contact {phoneName} has been added!'   
    else:
        new_record = classes.Record(phoneName)
        new_record.add_phone(phoneNum[0])

        book.add_record(new_record)

        return f'Contact {phoneName} has been added!' 

# Adds a birthday to the contacts
def birthday(operator):
    trimmed = re.sub('birthday', '', operator)
    phoneName = re.search(name_pattern, trimmed).group().capitalize()
    bDay = re.sub(phoneName.casefold(), '', trimmed).strip()

    record = book.find(phoneName)
    if record != None:
        record.add_birthday(bDay)

        return f'Contact {phoneName} has a birthday now!'   
    else:
        return f'Woopsie no contact with {phoneName} name!' 

# Update the contact number
def change(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = book.find(phoneName)
    contact.edit_phone(phoneNums[0], phoneNums[1])

    return f'Contact {phoneName} has been updated!'

# Delete the contact number for a certain contact
def delete_phone(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = book.find(phoneName)
    contact.remove_phone(phoneNums[0])

    return f'Phone {phoneNums[0]} was deleted fron contact {phoneName}!'

# Delete the contact
def delete(operator):
    phoneName = re.search(name_pattern, operator.replace("delete", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    
    capitalized_name = phoneName.group().capitalize()
    book.delete(capitalized_name)

    return f'Contact {capitalized_name} was deleted!'

# Displays the phone number of the requested contact
def contact(operator):
    phoneName = re.search(name_pattern, operator.replace("contact", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    
    capitalized_name = phoneName.group().capitalize()
    record = book.find(capitalized_name)

    return record

# Shows contact list
def show_all(operator):
    book_view = book.custom_iterator(len(book))
    return f'{next(book_view)}'

# Simple farewell function
def goodbye(operator):
    save(operator)

    return 'Good bye!'

# Start of functions for csv file
# Save your contacts to csv
def save(operator):
    try:
        with open('contacts.csv', 'x', newline='') as fh:
            field_names = ['Name', 'Phones', 'bDay']
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            
            for i in book:
                writer.writerow({'Name': i.name.value, 
                'Phones': '; '.join(p.value for p in i.phones), 
                'bDay' : i.birthday.value if bool(i.birthday) != False else 'None'})
                
        return f'Book formed!'
    except:
        with open('contacts.csv', 'a', newline='') as fh:
            writer = csv.writer(fh)
            for i in book:
                writer.writerow([i.name.value, 
                '; '.join(p.value for p in i.phones), 
                i.birthday.value if bool(i.birthday) != False else 'None'])

        return f'Book updated!'
    
# Opens saved file 
def unfold(operator):
    with open('contacts.csv', newline='') as fh:
        print(fh.read())

# Search contacts by name or number in saved file
def search_contact(operator):
    searcheble = operator.replace("search", "").strip()

    with open('contacts.csv', newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            phoneName = re.search(searcheble, row.get('Name'))
            phoneNum = re.search(searcheble, row.get('Phones'))
            if phoneName or phoneNum:
                return f'Search result:\n' \
                    f'Name: {row.get("Name")}, ' \
                        f'Phone: {row.get("Phones")}, ' \
                            f'bDay: {row.get("bDay")}'

# End of csv related functions

# Shows commad list
def commands(operator):
    return 'The list of commands: \n \
        Type "contact [name of the contact]" to see its phone num.\n \
        Type "phone [phone of the contact]" to see if its exist.\n \
        Type "add [name] [phone number]" to add new contact.\n \
        Type "change [name] [old phone number] [new phone number]" to add new contact.\n \
        Type "birthday [name] [birthday date in date format]" to add bDay to the contact.\n \
        Type "delete phone [name] [phone number]" to delete phone from the contact.\n \
        Type "delete [name]" to delte the contact.\n \
        Type "show all" to see all contacts \n \
        To sava data as csv or work with saved book use next commands: \n \
        Type "save" to save the address book \n \
        Type "search" to search the contact (search is case sensitive) \n \
        Type "unfold" to open saved book \n \
        And the ultimate command: \n \
        Type "end" to exit'

OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'delete phone': delete_phone,
    'delete': delete,
    'contact': contact,
    'search': search_contact,
    'show all': show_all,
    'goodbye': goodbye,
    'save': save,
    'unfold': unfold,
    'birthday': birthday,
    'commands': commands
}

def get_handler(operator):
    operator = operator_handler(operator)
    if operator not in OPERATIONS:
        raise AttributeError
    else:
        return OPERATIONS[operator]

if __name__ == '__main__':
    print('Go to the main file!')