import helper


wait_for_the_end = True
goodbyes = ("good bye", "close", "exit", "end", "bye")

def main_move(func):
    def inner(operator):
        try:
            func(operator)
        except AttributeError:
            print('Check twice or type the "commands" to print the list of commands!')
        except Exception as e:
            message = str(e)
            print(message)
    
    return inner

@main_move
def main(operator) -> str:
    handler = helper.get_handler(operator)
    
    print(handler(operator))


if __name__ == '__main__':
    while wait_for_the_end == True:
        operator = input(":")
        if operator in goodbyes:
            main('goodbye')
            break 
        else: 
            main(operator)