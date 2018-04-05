"""test's module."""
import csv
import os
import unittest

from app.forms import DownloadForm
from app.utils import start_parser
from fabfile import PROJECT_DIR


class YellSpiderTest(unittest.TestCase):
    """Public Yell Spider class test."""

    def test_parse(self):
        """Test parsing 2 sites."""
        template_folder = os.path.join(PROJECT_DIR, 'tests', 'html')
        self.assertEqual(os.path.exists(template_folder), True)

        file_moscow_path = os.path.join(template_folder, 'moscow.html')
        self.assertEqual(os.path.exists(file_moscow_path), True)
        url_moscow = 'file://{}'.format(file_moscow_path)

        file_vologda_path = os.path.join(template_folder, 'vologda.html')
        self.assertEqual(os.path.exists(file_vologda_path), True)
        url_vologda = 'file://{}'.format(file_vologda_path)

        urls = '{},{}'.format(url_moscow, url_vologda)
        filename = start_parser(
            url=urls,
            type_parsing=DownloadForm.CHOICES_TYPE_PARCING[0][0]
        )
        self.assertIsNotNone(filename)

        url_moscow_check = 'https://www.yell.ru/moscow/com/world-gym_3389506/'
        url_vologda_check = 'https://www.yell.ru/vologda/com/platina_9761388/'
        count_check_objects = 2

        if filename:
            with open(filename) as csv_file:
                items = csv.DictReader(csv_file, delimiter=',')

                for item in items:
                    if item['link'] == url_moscow_check:
                        self.assertEqual(
                            item['name'],
                            'World Gym Дубининская'
                        )
                        self.assertEqual(
                            item['category'],
                            'Москва|Спорт и фитнес|Фитнес клубы'
                        )
                        self.assertEqual(
                            item['rating'],
                            '4.9'
                        )
                        self.assertEqual(
                            item['addr'],
                            'г Москва, ул Дубининская, д 71'
                        )
                        self.assertEqual(
                            item['phones'],
                            '+7 499 116-84-09'
                        )
                        self.assertEqual(
                            item['metro'],
                            'Автозаводская,Добрынинская,Тульская,Шаболовская'
                        )
                        self.assertEqual(
                            item['district'],
                            'Даниловский'
                        )
                        self.assertEqual(
                            item['services'],
                            'Spa,Аквааэробика,Бассейн,Групповые занятия,'
                            'Единоборства,Консультация врача,Массаж,'
                            'Персональный тренер,'
                            'Процедуры снижения веса,Солярий')
                        count_check_objects -= 1

                    elif item['link'] == url_vologda_check:
                        self.assertEqual(
                            item['name'],
                            'Platina'
                        )
                        self.assertEqual(
                            item['category'],
                            'Вологда|Развлечения и отдых|Танцевальные клубы'
                        )
                        self.assertEqual(
                            item['rating'],
                            '4.0'
                        )
                        self.assertEqual(
                            item['addr'],
                            'Россия, г Вологда, ул Авксентьевского'
                        )
                        self.assertEqual(item['phones'], '')
                        self.assertEqual(item['metro'], '')
                        self.assertEqual(item['district'], '')
                        self.assertEqual(item['services'], '')
                        count_check_objects -= 1

                # script must find 2 objects
                # and count_check_objects must equal 0 after it
                self.assertEqual(count_check_objects, 0)
