"""Kivy based version of Registration_Form.py for iPad or desktop use."""

import os
import sys
from datetime import datetime
import pickle
import pandas as pd
import numpy as np
import phonenumbers
import pyqrcode
from PIL import Image, ImageDraw, ImageFont

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class RegistrationLayout(BoxLayout):
    """Main layout containing all form widgets."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)
        self.team_data = {
            'control_number': [], 'first name': [], 'last name': [], 'number': [],
            'grade': [], 'sport': [], 'school': [], 'team': [],
            'parent_first_name': [], 'parent_last_name': [], 'parent_phone_number': [],
            'parent_email': [], 'eight_by_ten': [], 'team_photo': [],
            'silver_package': [], 'digital_copy': [], 'banner': [], 'flex': [],
            'frame': [], 'payment_type': [], 'payment_amount': [], 'notes': [],
            'date': [], 'full name': [], 'resize-first name': [], 'resize-last name': [],
            'resize-full name': [], 'rename': [], 'left_number': [], 'right_number': []}

        self.control_number = 0
        self.today = datetime.date(datetime.now())
        self.save_path = os.getcwd()
        self.backup_save_path = os.getcwd()

        # Basic entries
        self.fname = TextInput(hint_text='First Name', multiline=False)
        self.lname = TextInput(hint_text='Last Name', multiline=False)
        self.number = TextInput(hint_text='Number', multiline=False)
        self.grade = TextInput(hint_text='Grade', multiline=False)
        self.sport = TextInput(hint_text='Sport', multiline=False)
        self.school = TextInput(hint_text='School', multiline=False)
        self.team = TextInput(hint_text='Team', multiline=False)

        self.parent_fname = TextInput(hint_text='Parent First Name', multiline=False)
        self.parent_lname = TextInput(hint_text='Parent Last Name', multiline=False)
        self.parent_phone = TextInput(hint_text='Parent Phone Number', multiline=False)
        self.email = TextInput(hint_text='Parent Email', multiline=False)

        self.eight_by_ten = TextInput(text='0', hint_text='8x10', multiline=False)
        self.team_photo = TextInput(text='0', hint_text='Team Photo', multiline=False)
        self.silver_package = TextInput(text='0', hint_text='Silver Package', multiline=False)
        self.digital_copy = TextInput(text='0', hint_text='Digital Copy', multiline=False)
        self.banner = TextInput(text='0', hint_text='Banner', multiline=False)
        self.flex = TextInput(text='0', hint_text='Flex', multiline=False)
        self.frame = TextInput(text='0', hint_text='Frame', multiline=False)

        self.payment_type = Spinner(text='Did not pay', values=('Cash', 'Card', 'Check', 'Did not pay'))
        self.payment_amount = TextInput(text='0', hint_text='Payment Amount', multiline=False)
        self.notes = TextInput(hint_text='Notes', multiline=False)

        # Build layout
        fields = [self.fname, self.lname, self.number, self.grade, self.sport, self.school,
                  self.team, self.parent_fname, self.parent_lname, self.parent_phone,
                  self.email, self.eight_by_ten, self.team_photo, self.silver_package,
                  self.digital_copy, self.banner, self.flex, self.frame,
                  self.payment_type, self.payment_amount, self.notes]

        scroll = ScrollView()
        form_box = BoxLayout(orientation='vertical', size_hint_y=None)
        form_box.bind(minimum_height=form_box.setter('height'))
        for widget in fields:
            form_box.add_widget(widget)
        scroll.add_widget(form_box)
        self.add_widget(scroll)

        # Buttons
        btn_box = BoxLayout(size_hint_y=None, height=50)
        submit_btn = Button(text='Submit', on_press=self.generate)
        total_btn = Button(text='Total Up', on_press=self.total_up)
        export_num = Button(text='Export Team - Number', on_press=self.export_team_by_number)
        export_grade = Button(text='Export Team - Grade', on_press=self.export_team_by_grade)
        btn_box.add_widget(submit_btn)
        btn_box.add_widget(total_btn)
        btn_box.add_widget(export_num)
        btn_box.add_widget(export_grade)
        self.add_widget(btn_box)

    def _add_record(self):
        extracted_number = str(self.number.text)
        leftnumber = extracted_number[:1] if len(extracted_number) == 2 else ''
        rightnumber = extracted_number[-1:] if extracted_number else ''
        self.team_data['first name'].append(self.fname.text)
        self.team_data['last name'].append(self.lname.text)
        self.team_data['number'].append(self.number.text)
        self.team_data['grade'].append(self.grade.text)
        self.team_data['sport'].append(self.sport.text)
        self.team_data['school'].append(self.school.text)
        self.team_data['control_number'].append(self.control_number)
        self.team_data['team'].append(self.team.text)
        self.team_data['parent_first_name'].append(self.parent_fname.text)
        self.team_data['parent_last_name'].append(self.parent_lname.text)
        self.team_data['parent_phone_number'].append(self.parent_phone.text)
        self.team_data['parent_email'].append(self.email.text)
        self.team_data['eight_by_ten'].append(self.eight_by_ten.text)
        self.team_data['team_photo'].append(self.team_photo.text)
        self.team_data['silver_package'].append(self.silver_package.text)
        self.team_data['digital_copy'].append(self.digital_copy.text)
        self.team_data['banner'].append(self.banner.text)
        self.team_data['flex'].append(self.flex.text)
        self.team_data['frame'].append(self.frame.text)
        self.team_data['payment_type'].append(self.payment_type.text)
        self.team_data['payment_amount'].append(self.payment_amount.text)
        self.team_data['notes'].append(self.notes.text)
        self.team_data['date'].append(self.today)
        self.team_data['full name'].append(f"{self.fname.text} {self.lname.text}")
        self.team_data['resize-first name'].append('XM')
        self.team_data['resize-last name'].append('XM')
        self.team_data['resize-full name'].append('XM')
        self.team_data['rename'].append(f"{self.control_number}_{self.fname.text} {self.lname.text}")
        self.team_data['left_number'].append(leftnumber)
        self.team_data['right_number'].append(rightnumber)

    def _save_files(self, name):
        df = pd.DataFrame(self.team_data)
        df.to_csv(os.path.join(self.save_path, f"{name}.csv"), index=False)
        with open(os.path.join(self.save_path, f"{name}.pickle"), 'wb') as f:
            pickle.dump(self.team_data, f)
        # backup
        try:
            df.to_csv(os.path.join(self.backup_save_path, f"{name}.csv"), index=False)
            with open(os.path.join(self.backup_save_path, f"{name}.pickle"), 'wb') as f:
                pickle.dump(self.team_data, f)
        except Exception:
            pass

    def generate_card(self):
        font_path = '/System/Library/Fonts/Helvetica' if sys.platform == 'darwin' else r'C:\\Windows\\Fonts\\arial.ttf'
        control_text = str(self.control_number)
        data = f"{control_text}_{self.fname.text}_{self.lname.text}_{self.grade.text}_{self.number.text}_{self.sport.text}_{self.school.text}_{self.payment_amount.text}_{self.payment_type.text}"
        qr = pyqrcode.create(data)
        qr.png('qrcode.png')
        paperwidth, paperheight = 2550, 3300
        font = ImageFont.truetype(font=font_path, size=200)
        background = Image.new('RGBA', (paperwidth, paperheight), (255, 255, 255, 255))
        draw = ImageDraw.Draw(background)
        qr_img = Image.open('qrcode.png').resize((1000, 1000), Image.LANCZOS)
        background.paste(qr_img, (paperwidth // 2, 20))
        center = (paperwidth/2)-(paperwidth/3)
        interval, height = 250, 800
        draw.text((center, height + interval), control_text, (0, 0, 0), font=ImageFont.truetype(font=font_path, size=300))
        draw.text((center, height + interval*2), f"FName - {self.fname.text}", (0, 0, 0), font=font)
        draw.text((center, height + interval*3), f"LName - {self.lname.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval*4), f"Grade - {self.grade.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval*5), f"Number - {self.number.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval*6), f"Sport - {self.sport.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval*7), f"School - {self.school.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval*8), f"Team - {self.team.text}", (25, 25, 25), font=font)
        background.save(os.path.join(self.save_path, f"{control_text}_{self.fname.text}_{self.lname.text}.png"))

    def generate(self, instance):
        # simplistic password check
        password = 'a'
        parsed = phonenumbers.parse(self.parent_phone.text, 'US')
        if not phonenumbers.is_valid_number(parsed):
            return
        self.control_number += 1
        self.generate_card()
        self._add_record()
        self._save_files('registration')
        # clear entries
        for widget in [self.fname, self.lname, self.number, self.parent_fname, self.parent_lname,
                       self.parent_phone, self.email, self.eight_by_ten, self.team_photo,
                       self.silver_package, self.digital_copy, self.banner, self.flex,
                       self.frame, self.payment_amount, self.notes]:
            widget.text = ''
        self.payment_type.text = 'Did not pay'

    def total_up(self, instance):
        df = pd.DataFrame(self.team_data)
        df['payment_amount'] = df['payment_amount'].astype(int)
        cards = df[df['payment_type'] == 'Card'].payment_amount.sum()
        cash = df[df['payment_type'] == 'Cash'].payment_amount.sum()
        checks = df[df['payment_type'] == 'Check'].payment_amount.sum()
        total = df.payment_amount.sum()
        print(f"Card: {cards} Cash: {cash} Check: {checks} Total: {total}")

    def _export_sorted(self, key, filename):
        df = pd.DataFrame(self.team_data)
        try:
            sorted_list_pivot = pd.pivot_table(df, index=['sport', key, 'full name'])
            sorted_list = sorted_list_pivot.reset_index()
            sorted_list = sorted_list.sort_values(by=['sport', key, 'full name'], ascending=True)
            sorted_list = sorted_list[['sport', key, 'full name']]
        except Exception:
            sorted_list_pivot = pd.pivot_table(df, index=[key, 'full name'])
            sorted_list = sorted_list_pivot.reset_index()
            sorted_list = sorted_list.sort_values(by=[key, 'full name'], ascending=True)
            sorted_list = sorted_list[[key, 'full name']]
        sorted_list.to_csv(os.path.join(self.save_path, filename), index=False)

    def export_team_by_number(self, instance):
        self._export_sorted('number', 'Roster By Number.csv')

    def export_team_by_grade(self, instance):
        self._export_sorted('grade', 'Roster By Grade.csv')


class RegistrationApp(App):
    def build(self):
        return RegistrationLayout()


if __name__ == '__main__':
    RegistrationApp().run()
