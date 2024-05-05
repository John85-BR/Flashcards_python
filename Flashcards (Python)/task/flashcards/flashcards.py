import builtins
from io import StringIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i1", "--import_from")
parser.add_argument("-e1", "--export_to")
args = parser.parse_args()

term_data = {}

f = StringIO()
definition_temp = []


def input(string):
    f.write(string)
    return builtins.input(string)


def print(string):
    f.write(string)
    builtins.print(string)


if args.import_from:
    counter = 0
    try:
        with open(args.import_from, 'r') as file_reader:

            for line in file_reader:
                key, value = line.split(":")

                name, error = str(value[:len(value) - 2]).strip('[').strip('\n').split(',')
                term_data[key] = [value,int(error)]
                counter += 1

        print(f"{counter} cards have been loaded.")


    except FileNotFoundError as error:
        print("File not found.\n")

while True:

    action = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
    if action == "add":
        term_add = input(f"The card:\n")

        while True:
            if term_add in term_data:
                term_add = input(f'The card \"{term_add}\" already exists. Try again:\n')
            else:
                break
        definition = input(f"The definition of the card:\n")

        while True:

            if definition in definition_temp:
                definition = input(f'The definition\"{definition}\" already exists. Try again:\n')

            else:
                term_data[term_add] = [definition, 0]
                definition_temp.append(definition)
                break

        print(f"The pair (\"{term_add}\":\"{definition}\") has been added.")

    if action == "remove":
        term_remove = input("Which card?\n")

        if term_remove not in term_data:
            print(f"Can't remove \"{term_remove}\": there is no such card.")
        else:
            term_data.pop(term_remove)
            print("The card has been removed.")

    if action == "ask":
        times_ask = int(input("How many times to ask?\n"))
        cont = 0

        while True:

            for term, defin in term_data.items():

                answer = input(f"Print the definition of \"{term}\":\n")

                if answer == defin[0]:
                    print("Correct!")
                else:
                    temp = list(filter(lambda x: term_data[x][0] == answer, term_data))
                    print(
                        f"Wrong. The right answer is \"{defin[0]}\", but your definition is correct for \"{str(*temp)}\"")
                    term_data[term][1] += 1

                cont += 1

                if cont >= times_ask:
                    break
            if cont >= times_ask:
                break

    if action == "import":
        import_data = input("File name:\n")
        cont = 0
        try:
            with open(import_data, 'r') as file_reader:
                for line in file_reader:
                    key, value, error = line.split(":")
                    term_data[key] = [value, int(error)]
                    cont += 1
            print(f"{cont} cards have been loaded.")
        except FileNotFoundError as error:
            print("File not found.\n")

    if action == "export":
        export_data = input("File name:\n")
        with open(export_data, 'w') as file_writer:
            for term, defin in term_data.items():
                file_writer.write(f"{term}:{defin[0]}:{defin[1]}\n")
        print(f"{len(term_data)} cards have been saved.")

    if action == "log":
        log_file = input("File name:\n")
        with open(log_file, 'w') as file:
            file.write(f.getvalue())

        builtins.print("The log has been saved.")

    if action == "hardest card":
        temp = 0
        maximum = {}
        temp_list = []
        for term, defin in term_data.items():
            if term_data[term][1] >= temp:
                maximum = {term: defin}
                temp = term_data[term][1]

        for term in term_data.keys():
            if term_data[term][1] == temp:
                temp_list.append(term)

        if len(temp_list) == 1 and temp != 0:

            builtins.print(f"The hardest card is \"{maximum}\". You have  errors "
                           f"answering it")
        elif len(temp_list) > 1 and temp != 0:
            builtins.print(f"The hardest cards are {', '.join(temp_list)}")

        else:
            builtins.print("There are no cards with errors.")

        temp_list.clear()

    if action == "reset stats":
        for term in term_data.keys():
            term_data[term][1] = 0
        print("Card statistics have been reset.")

    if action == "exit":

        if args.export_to:
            with open(args.export_to, 'w') as file_writer:
                for term, defin in term_data.items():
                    file_writer.write(f"{term}:{defin}\n")
            print(f"{len(term_data)} cards have been saved.")
        print("Bye bye")
        break
