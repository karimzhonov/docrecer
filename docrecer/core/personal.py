from pathlib import Path
from dataclasses import dataclass
from .data import Data
from .base.base_patent import PatentData
from .base.base_passport import PassportData
from .base.base_migration_card import MigrationCardData
from .base.base_snils import SnilsData


@dataclass
class PersonalData(Data):

    passport: PassportData = PassportData()
    patent: PatentData = PatentData()
    migration_card: MigrationCardData = MigrationCardData()
    snils: SnilsData = SnilsData()

    def reset(self):
        self.snils.reset()
        self.passport.reset()
        self.patent.reset()
        self.migration_card.reset()

    def save_as_txt(self, path: Path):
        personal_data = self.to_json(False)
        email_content = ''
        email_title = ''
        if personal_data['passport']:
            email_title = f"{self.passport.surname if self.passport.surname else ''} {self.passport.name if self.passport.name else ''} {self.passport.middle_name if self.passport.middle_name else ''}"
            email_content = f"""{email_content}
{f"Паспорт.Номер: {personal_data['passport'].get('number', '-')}<br/>" if personal_data['passport'].get('number', None) else ''}
{f"Паспорт.Серия: {personal_data['passport'].get('serial', '-')}<br/>" if personal_data['passport'].get('serial', None) else ''}
{f"Паспорт.ДатаВыдачи: {personal_data['passport'].get('issue_date', '-')}<br/>"if personal_data['passport'].get('issue_date', None) else ''}
{f"Паспорт.ДатаДействия: {personal_data['passport'].get('expiration_date', '-')}<br/>"if personal_data['passport'].get('expiration_date', None) else ''}
{f"Паспорт.МестоРождения: {personal_data['passport'].get('birth_place', '-')}<br/>"if personal_data['passport'].get('birth_place', None) else ''}
{f"Паспорт.ДатаРождения: {personal_data['passport'].get('birth_date', '-')}<br/>"if personal_data['passport'].get('birth_date', None) else ''}
{f"Паспорт.Гражданство: {personal_data['passport'].get('citizenship', '-')}<br/>"if personal_data['passport'].get('citizenship', None) else ''}
{f"Паспорт.Фамилия: {personal_data['passport'].get('surname', '-')}<br/>"if personal_data['passport'].get('surname', None) else ''}
{f"Паспорт.Имя: {personal_data['passport'].get('name', '-')}<br/>"if personal_data['passport'].get('name', None) else ''}
{f"Паспорт.Отчество: {personal_data['passport'].get('middle_name', '-')}<br/>"if personal_data['passport'].get('middle_name', None) else ''}
{f"Паспорт.Пол: {personal_data['passport'].get('gender', '-')}<br/>"if personal_data['passport'].get('gender', None) else ''}
{f"Паспорт.КемВыдан: {personal_data['passport'].get('authority', '-')}<br/>"if personal_data['passport'].get('authority', None) else ''}"""
        

        if self.patent.to_json(False):
            if not email_title: f"{self.patent.surname if self.patent.surname else ''} {self.patent.name if self.patent.name else ''} {self.patent.middle_name if self.patent.middle_name else ''}"
            email_content = f"""{email_content}
{f"Патент.Серия: {self.patent.serial}<br/>" if self.patent.serial else ''}
{f"Патент.Номер: {self.patent.number}<br/>" if self.patent.number else ''}
{f"Патент.Фамилия: {self.patent.surname}<br/>" if self.patent.surname else ''}
{f"Патент.Имя: {self.patent.name}<br/>" if self.patent.name else ''}
{f"Патент.Отчество: {self.patent.middle_name}<br/>" if self.patent.middle_name else ''}
{f"Патент.КемВыдано: {self.patent.authority}<br/>" if self.patent.authority else ''}
{f"Патент.ДатаВыдачи: {self.patent.issue_date}<br/>" if self.patent.issue_date else ''}
{f"Патент.ИНН: {self.patent.tin}<br/>" if self.patent.tin else ''}
{f"Патент.СерияПаспорта: {self.patent.passport_serial}<br/>"if self.patent.passport_serial else ''}
{f"Патент.НомерПаспорта: {self.patent.passport_number}<br/>"if self.patent.passport_number else ''}
{f"Патент.Гражданство: {self.patent.citizenship}<br/>"if self.patent.citizenship else ''}
{f"Патент.ДатаРождения: {self.patent.birth_date}<br/>"if self.patent.birth_date else ''}
{f"Патент.Должность: {self.patent.position}<br/>"if self.patent.position else ''}"""
        

        if self.migration_card.to_json(False): 
            email_content = f"""{email_content}
{f"МК.Серия: {self.migration_card.serial}<br/>" if self.migration_card.serial else ''}
{f"МК.Номер: {self.migration_card.number}<br/>" if self.migration_card.number else ''}
            """

        if self.snils.to_json(False):
            email_content += f"""
{f"СНИЛС. Номер: ${self.snils.number}<br/>" if self.snils.number else ''}
            """
        if not email_title: email_title = str(path.parents[-1])
        content = f"""
{email_title}
##########
{email_content}"""
        path.write_text(content)

