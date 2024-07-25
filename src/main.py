import flet as ft
from flet import colors, TextCapitalization
from datetime import datetime, time as dt_time
from collections import OrderedDict


def main(page: ft.Page):
    def on_click_remove(e):
        """
        Removes medication from system
        """
        med_to_remove = remove_drop.value
        if med_to_remove in medication_diction:
            medication_diction.pop(med_to_remove)
            page.client_storage.set("Medications", {k: v.strftime('%H:%M') for k, v in medication_diction.items()})
            update_medication_list()
            update_remove_dropdown()
            page.update()

    def deactivate_button(name):
        """
        Deactivates buttons indicating medication taken
        :param name: Name of medication
        """
        if name in medication_buttons:
            btn = medication_buttons[name]
            btn.text = f"{name}, Taken at {datetime.now().strftime('%H:%M')}"
            btn.on_click = lambda e, nm=name: reactivate_button(nm)
            btn.color = colors.BLUE_900
            btn.bgcolor = colors.LIGHT_BLUE_50
            page.update()

    def reactivate_button(name):
        """
        Reactivates buttons
        :param name: Name of medication
        """
        if name in medication_buttons:
            med_time = medication_diction[name]
            btn = medication_buttons[name]
            btn.text = f"{name} : {med_time.strftime('%H:%M')}"
            btn.on_click = lambda e, nm=name: deactivate_button(nm)
            btn.disabled = False
            btn.color = colors.BLACK
            btn.bgcolor = colors.LIGHT_BLUE_100
            page.update()

    def reset(e):
        """
        Resets all medication buttons
        """
        for name in medication_diction.keys():
            reactivate_button(name)

    def create_medication(elements):
        """
        Creates buttons for all medication
        :param elements: OrderedDict of medication and times
        :return: A ListView containing all buttons
        """
        medications = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        if not elements:
            home.controls.append(
                ft.Row(controls=[ft.Text("Please add your medication")], alignment=ft.MainAxisAlignment.CENTER))
        for name, med_time in elements.items():
            btn = ft.ElevatedButton(
                f"{name} : {med_time.strftime('%H:%M')}",
                on_click=lambda e, nm=name: deactivate_button(nm)
            )
            medication_buttons[name] = btn
            medications.controls.append(btn)
        return medications

    def update_medication_list():
        """
        Updates the medication list view with current medications
        """
        medication.controls.clear()
        medication.controls.append(create_medication(medication_diction))
        home.controls.clear()
        home.controls.append(medication)

    def update_remove_dropdown():
        """
        Updates the remove dropdown list with current medications
        """
        remove_drop.options.clear()
        for med in medication_diction.keys():
            remove_drop.options.append(ft.dropdown.Option(med))
        page.update()

    def add_new_medication(e):
        """
        Adds new medication to the dictionary and updates the list
        """
        if new_medic_name.value and new_medic_hour.value and new_medic_min:
            try:
                med_time = dt_time(int(new_medic_hour.value), int(new_medic_min.value))
                medication_diction[new_medic_name.value] = med_time
                page.client_storage.set("Medications", {k: v.strftime('%H:%M') for k, v in medication_diction.items()})
                update_medication_list()
                update_remove_dropdown()
                page.update()
            except ValueError:
                error = ft.Text("Invalid input for medication time. Please enter valid hour and minute.")
                add_new.controls.append(error)
                page.update()
        else:
            error2 = ft.Text("Please enter both medication name and time.")
            add_new.controls.append(error2)
            page.update()

    page.bgcolor = colors.WHITE

    if page.client_storage.contains_key("Medications"):
        stored_medications = page.client_storage.get("Medications")
        medication_diction = OrderedDict(
            {k: datetime.strptime(v, '%H:%M').time() for k, v in stored_medications.items()}
        )
    else:
        medication_diction = OrderedDict()

    medication_buttons = {}

    # HEADING
    heading = ft.Row(
        controls=[
            ft.Text(
                "\nMedication Tracker",
                size=20,
                color=colors.BLUE,
                weight=ft.FontWeight.BOLD,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # HOME
    home = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
    medication = create_medication(medication_diction)
    home.controls.append(medication)

    # SETTINGS
    add_new_text = ft.Text("Add New Medication")
    new_medic_name = ft.TextField(label="Name",
                                  hint_text="Please enter name of medication here",
                                  capitalization=TextCapitalization.WORDS)
    hour_op = [ft.dropdown.Option(str(hour)) for hour in range(24)]
    new_medic_hour = ft.Dropdown(options=hour_op, label="Hour")

    min_op = [ft.dropdown.Option(str(min)) for min in range(60)]
    new_medic_min = ft.Dropdown(options=min_op, label="Minute")

    submit_medication = ft.ElevatedButton(text="Submit", on_click=add_new_medication)
    add_new = ft.ListView(expand=1, spacing=10, padding=2, auto_scroll=False)
    add_new.controls.append(add_new_text)
    add_new.controls.append(new_medic_name)
    add_new.controls.append(new_medic_hour)
    add_new.controls.append(new_medic_min)
    add_new.controls.append(submit_medication)

    remove = ft.ListView(expand=1, spacing=10, padding=2, auto_scroll=False)
    remove_m = ft.Text("Remove Medication")
    options = [ft.dropdown.Option(med) for med in medication_diction.keys()]
    remove_drop = ft.Dropdown(options=options)
    submit_remove = ft.ElevatedButton(text="Submit", on_click=on_click_remove)
    remove.controls.append(remove_m)
    remove.controls.append(remove_drop)
    remove.controls.append(submit_remove)

    reset = ft.Row([ft.ElevatedButton("Reset Medication", on_click=reset, color=colors.WHITE, bgcolor=colors.BLUE)],
                   alignment=ft.MainAxisAlignment.CENTER,
                   )

    settings = ft.ListView(expand=1, spacing=10, padding=10, auto_scroll=False)
    settings.controls.append(add_new)
    settings.controls.append(remove)
    settings.controls.append(reset)

    # TABS
    tabs = [
        ft.Tab(text="Home",
               icon=ft.icons.HOME,
               content=home),
        ft.Tab(text="Settings",
               icon=ft.icons.SETTINGS,
               content=settings)
    ]
    tabs_list = ft.Tabs(
        selected_index=0,
        animation_duration=20,
        label_color=ft.colors.LIGHT_BLUE,
        unselected_label_color=ft.colors.BLACK,
        tabs=tabs,
        scrollable=False)

    # PAGE
    page.add(heading)
    page.add(tabs_list)


ft.app(main)
