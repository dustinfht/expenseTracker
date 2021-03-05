import PySimpleGUI as sg


def get_longest(entries):
    max_length = 0
    print(type(entries))
    for entry in entries:
        if type(entry) == str:
            print("Entry is string")
            length = len(entry)
            print("size is " + str(length))
            if max_length < length:
                max_length = length
        else:
            print(f"Entry is not a string. Type: {type(entry)}.")

    print("max length is " + str(max_length))
    return max_length


class Gui:

    def __init__(self, database_connector):
        self.database_connector = database_connector

    def show_main(self, location=(None, None)):
        sg.change_look_and_feel("Dark2")

        # ------ Menu Definition ------ #
        menu_def = [["File", ["Open", "Save", "Exit"]],
                    ["Edit", ["Paste", ["Special", "Normal", ], "Undo"], ],
                    ["Help", "About..."], ]

        # ------ GUI Definition ------ #
        values = self.database_connector.get_expenses()
        values = list(map(lambda exp: exp.to_string(), values))

        width = get_longest(values)

        width = (40 if width < 40 else width)

        print(width)

        left_col = [
            [sg.Text("Ausgaben")],
            [sg.Listbox(values, key="-LIST-", size=(width, 20))],
            [sg.Button("Add Entry", key="-ADD_ENTRY-")],
        ]

        right_col = [
            [sg.Text("Nothing to show", key="-RESULT-")],
            [sg.Button("Delete Entry", key="-DELETE_ENTRY-")]
        ]

        layout = [
            [sg.Menu(menu_def, )],
            [sg.Column(left_col, element_justification="c"), sg.VSeparator(),
             sg.Column(right_col, element_justification="c")]

        ]

        window = sg.Window("Windows-like program", layout, default_element_size=(12, 1),
                           location=location, auto_size_text=False, auto_size_buttons=False,
                           default_button_element_size=(12, 1), finalize=True)

        # ------ Loop & Process button menu choices ------ #
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                window.close()
                break
            print("Button = ", event)
            # ------ Process menu choices ------ #
            if event == "About...":
                sg.popup("About this program", "Version 1.0", "PySimpleGui rocks...")
            elif event == "Open":
                filename = sg.popup_get_file("file to open", no_window=True)
                print(filename)
            elif event == "-ADD_ENTRY-":
                self.__open_add_context()
                old_location = window.current_location()
                window.close()
                self.show_main(location=old_location)
            elif event == "-DELETE_ENTRY-":
                selected = values["-LIST-"][0]
                if not selected:
                    window["-SELECTED-"].update(text="Please select one entry.")
                else:
                    expense_id = selected.split(" ", 1)
                    self.database_connector.delete_expense(expense_id[0])
                    old_location = window.current_location()
                    window.close()
                    self.show_main(location=old_location)

    def __open_add_context(self):

        def TextLabel(text):
            return sg.Text(text + ':', justification='r', size=(15, 1))

        # ------ GUI Definition ------ #
        layout = [
            [sg.Text("Add Entry", font="Any 15"), sg.Text("Invalid entries! Try again.", key="-ERROR-", visible=False)],
            [TextLabel("Amount"), sg.Input(key="-AMOUNT-")],
            [TextLabel("Reason"), sg.Input(key="-REASON-")],
            [TextLabel("Date"), sg.Input(disabled=True, key="-DATE-"), sg.CalendarButton("📅")],
            [sg.Button("Save", key="-SAVE-"), sg.Button("Cancel")],
        ]

        window = sg.Window("Add entry", layout, keep_on_top=True, finalize=True)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Cancel":
                window.close()
                break
            print("Button = ", event)
            # ------ Process save ------ #
            if event == "-SAVE-":
                amount = values["-AMOUNT-"]
                reason = values["-REASON-"]
                date = values["-DATE-"]
                if not amount or not reason or not date:
                    window["-ERROR-"].update(visible=True)
                else:
                    self.database_connector.add_expense(amount, reason, date)
                    window.close()


class GuiDataExpenseEntry:
    def __init__(self, costs, date, reason):
        self.costs = costs
        self.reason = reason
        self.date = date
