"""KivyMD version of Registration_Form.py with a modern look inspired by the ChatGPT app."""

import os
import sys
from datetime import datetime
import pickle

import pandas as pd
import phonenumbers
import pyqrcode
from PIL import Image, ImageDraw, ImageFont

from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.spinner import MDSpinner


class RegistrationLayout(MDBoxLayout):
    """Form layout using KivyMD widgets."""

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

        toolbar = MDToolbar(title="Titensor Registration")
        self.add_widget(toolbar)

        scroll = ScrollView()
        self.form_box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        self.form_box.bind(minimum_height=self.form_box.setter('height'))

        # Text fields
        self.fname = MDTextField(hint_text='First Name')
        self.lname = MDTextField(hint_text='Last Name')
        self.number = MDTextField(hint_text='Number')
        self.grade = MDTextField(hint_text='Grade')
        self.sport = MDTextField(hint_text='Sport')
        self.school = MDTextField(hint_text='School')
        self.team = MDTextField(hint_text='Team')
        self.parent_fname = MDTextField(hint_text='Parent First Name')
        self.parent_lname = MDTextField(hint_text='Parent Last Name')
        self.parent_phone = MDTextField(hint_text='Parent Phone Number')
        self.email = MDTextField(hint_text='Parent Email')
        self.eight_by_ten = MDTextField(text='0', hint_text='8x10')
        self.team_photo = MDTextField(text='0', hint_text='Team Photo')
        self.silver_package = MDTextField(text='0', hint_text='Silver Package')
        self.digital_copy = MDTextField(text='0', hint_text='Digital Copy')
        self.banner = MDTextField(text='0', hint_text='Banner')
        self.flex = MDTextField(text='0', hint_text='Flex')
        self.frame = MDTextField(text='0', hint_text='Frame')
        self.payment_type = MDSpinner(text='Did not pay', values=['Cash', 'Card', 'Check', 'Did not pay'])
        self.payment_amount = MDTextField(text='0', hint_text='Payment Amount')
        self.notes = MDTextField(hint_text='Notes')

        fields = [self.fname, self.lname, self.number, self.grade, self.sport, self.school,
                  self.team, self.parent_fname, self.parent_lname, self.parent_phone,
                  self.email, self.eight_by_ten, self.team_photo, self.silver_package,
                  self.digital_copy, self.banner, self.flex, self.frame,
                  self.payment_type, self.payment_amount, self.notes]

        for widget in fields:
            self.form_box.add_widget(widget)
        scroll.add_widget(self.form_box)
        self.add_widget(scroll)

        btn_box = MDBoxLayout(size_hint_y=None, height=60, spacing=10)
        submit_btn = MDRectangleFlatButton(text='Submit', on_release=self.generate)
        total_btn = MDRectangleFlatButton(text='Total Up', on_release=self.total_up)
        export_num = MDRectangleFlatButton(text='Export Number', on_release=self.export_team_by_number)
        export_grade = MDRectangleFlatButton(text='Export Grade', on_release=self.export_team_by_grade)
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

    def _save_files(self, name: str) -> None:
        df = pd.DataFrame(self.team_data)
        df.to_csv(os.path.join(self.save_path, f"{name}.csv"), index=False)
        with open(os.path.join(self.save_path, f"{name}.pickle"), 'wb') as f:
            pickle.dump(self.team_data, f)
        try:
            df.to_csv(os.path.join(self.backup_save_path, f"{name}.csv"), index=False)
            with open(os.path.join(self.backup_save_path, f"{name}.pickle"), 'wb') as f:
                pickle.dump(self.team_data, f)
        except Exception:
            pass

    def generate_card(self) -> None:
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
        center = (paperwidth / 2) - (paperwidth / 3)
        interval, height = 250, 800
        draw.text((center, height + interval), control_text, (0, 0, 0), font=ImageFont.truetype(font=font_path, size=300))
        draw.text((center, height + interval * 2), f"FName - {self.fname.text}", (0, 0, 0), font=font)
        draw.text((center, height + interval * 3), f"LName - {self.lname.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval * 4), f"Grade - {self.grade.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval * 5), f"Number - {self.number.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval * 6), f"Sport - {self.sport.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval * 7), f"School - {self.school.text}", (25, 25, 25), font=font)
        draw.text((center, height + interval * 8), f"Team - {self.team.text}", (25, 25, 25), font=font)
        background.save(os.path.join(self.save_path, f"{control_text}_{self.fname.text}_{self.lname.text}.png"))

    def generate(self, instance) -> None:
        parsed = phonenumbers.parse(self.parent_phone.text, 'US')
        if not phonenumbers.is_valid_number(parsed):
            return
        self.control_number += 1
        self.generate_card()
        self._add_record()
        self._save_files('registration')
        for widget in [self.fname, self.lname, self.number, self.parent_fname, self.parent_lname,
                       self.parent_phone, self.email, self.eight_by_ten, self.team_photo,
                       self.silver_package, self.digital_copy, self.banner, self.flex,
                       self.frame, self.payment_amount, self.notes]:
            widget.text = ''
        self.payment_type.text = 'Did not pay'

    def total_up(self, instance) -> None:
        df = pd.DataFrame(self.team_data)
        df['payment_amount'] = df['payment_amount'].astype(int)
        cards = df[df['payment_type'] == 'Card'].payment_amount.sum()
        cash = df[df['payment_type'] == 'Cash'].payment_amount.sum()
        checks = df[df['payment_type'] == 'Check'].payment_amount.sum()
        total = df.payment_amount.sum()
        print(f"Card: {cards} Cash: {cash} Check: {checks} Total: {total}")

    def _export_sorted(self, key: str, filename: str) -> None:
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

    def export_team_by_number(self, instance) -> None:
        self._export_sorted('number', 'Roster By Number.csv')

    def export_team_by_grade(self, instance) -> None:
        self._export_sorted('grade', 'Roster By Grade.csv')


class RegistrationApp(MDApp):
    """KivyMD App wrapper."""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return RegistrationLayout()


if __name__ == '__main__':
    RegistrationApp().run()
