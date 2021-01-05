import os
import json
import datetime

import unittest

from bdf.bdf import BusinessDatasetFormatter
from bdf.exceptions import ENoDeliveryException


class TestBusinessDatasetFormatter(unittest.TestCase):

    def setUp(self):
        self.deliveries = [{'_id': datetime.datetime(2020, 4, 29, 0, 0), 'deliveries': 1}, #wednesday
                           {'_id': datetime.datetime(2020, 4, 27, 0, 0), 'deliveries': 1}, #monday
                           {'_id': datetime.datetime(2020, 4, 26, 0, 0), 'deliveries': 1}, #sunday
                           {'_id': datetime.datetime(2020, 4, 24, 0, 0), 'deliveries': 2}, #friday
                           {'_id': datetime.datetime(2020, 4, 21, 0, 0), 'deliveries': 3},
                           {'_id': datetime.datetime(2020, 4, 19, 0, 0), 'deliveries': 3}, #sunday
                           {'_id': datetime.datetime(2020, 4, 18, 0, 0), 'deliveries': 2}, #saturday
                           {'_id': datetime.datetime(2020, 4, 17, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 16, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 15, 0, 0), 'deliveries': 2},
                           {'_id': datetime.datetime(2020, 4, 14, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 13, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 11, 0, 0), 'deliveries': 1}, #saturday
                           {'_id': datetime.datetime(2020, 4, 10, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 9, 0, 0), 'deliveries': 2},
                           {'_id': datetime.datetime(2020, 4, 8, 0, 0), 'deliveries': 4},
                           {'_id': datetime.datetime(2020, 4, 7, 0, 0), 'deliveries': 3},
                           {'_id': datetime.datetime(2020, 4, 6, 0, 0), 'deliveries': 1},
                           {'_id': datetime.datetime(2020, 4, 5, 0, 0), 'deliveries': 5}]
        self.dd = BusinessDatasetFormatter()
        self.current_date = datetime.date(year=2020, month=4, day=29)
        self.id_field = '_id'
        self.qty_field = 'deliveries'

    def test_no_deliveries(self):
        return_value = []
        with self.assertRaises(ENoDeliveryException):
            self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)

    def test_one_date(self):
        return_value = self.deliveries[:1]
        group = self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)
        current_date = datetime.datetime(year=self.current_date.year, \
            month=self.current_date.month, day=self.current_date.day)
        self.assertEqual(len(group), 1)
        self.assertEqual(current_date, group[0]['date'])
        self.assertEqual(1, group[0]['deliveries'])

    def test_two_dates(self):
        return_value = self.deliveries[:2]
        today_method = self.current_date
        group = self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)
        current_date = datetime.datetime(year=self.current_date.year, \
            month=self.current_date.month, day=self.current_date.day)
        second_date = current_date - datetime.timedelta(days=1)
        self.assertEqual(len(group), 2)
        self.assertEqual(current_date, group[0]['date'])
        self.assertEqual(1, group[0]['deliveries'])
        self.assertEqual(second_date, group[1]['date'])

    def test_three_dates(self):
        return_value = self.deliveries[:3]
        today_method = self.current_date
        group = self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)
        current_date = datetime.datetime(year=self.current_date.year, \
            month=self.current_date.month, day=self.current_date.day)
        second_date = current_date - datetime.timedelta(days=1)
        third_date = current_date - datetime.timedelta(days=2)
        self.assertEqual(len(group), 3)
        self.assertEqual(current_date, group[0]['date'])
        self.assertEqual(second_date, group[1]['date'])
        self.assertEqual(0, group[1]['deliveries'])
        self.assertEqual(third_date, group[2]['date'])
        self.assertEqual(1, group[2]['deliveries'])

    def test_six_dates(self):
        return_value = self.deliveries[:6]
        today_method = self.current_date
        groups = self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)
        current_date = datetime.datetime(year=self.current_date.year, \
            month=self.current_date.month, day=self.current_date.day)
        second_date = current_date - datetime.timedelta(days=1)
        third_date = current_date - datetime.timedelta(days=2)
        fourth_date = current_date - datetime.timedelta(days=3)
        fifth_date = current_date - datetime.timedelta(days=5)
        sixth_date = current_date - datetime.timedelta(days=6)
        self.assertEqual(len(groups), 6)
        self.assertEqual(current_date, groups[0]['date'])
        self.assertEqual(second_date, groups[1]['date'])
        self.assertEqual(third_date, groups[2]['date'])
        self.assertEqual(fourth_date, groups[3]['date'])
        self.assertEqual(fifth_date, groups[4]['date'])
        self.assertEqual(sixth_date, groups[5]['date'])

    def test_ten_deliveries(self):
        return_value = self.deliveries
        today_method = self.current_date
        group = self.dd.return_15_days_data(self.current_date, return_value, self.id_field, self.qty_field)
        current_date = datetime.datetime(year=self.current_date.year, \
            month=self.current_date.month, day=self.current_date.day)
        second_date = current_date - datetime.timedelta(days=1)
        third_date = current_date - datetime.timedelta(days=2)
        fourth_date = current_date - datetime.timedelta(days=3)
        fifth_date = current_date - datetime.timedelta(days=5)
        sixth_date = current_date - datetime.timedelta(days=6)
        seventh_date = current_date - datetime.timedelta(days=7)
        eighth_date = current_date - datetime.timedelta(days=8)
        ninth_date = current_date - datetime.timedelta(days=9)
        tenth_date = current_date - datetime.timedelta(days=10)
        self.assertEqual(len(group), 15)
        self.assertEqual(current_date, group[0]['date'])
        self.assertEqual(second_date, group[1]['date'])
        self.assertEqual(third_date, group[2]['date'])
        self.assertEqual(fourth_date, group[3]['date'])
        self.assertEqual(fifth_date, group[4]['date'])
        self.assertEqual(sixth_date, group[5]['date'])
        self.assertEqual(seventh_date, group[6]['date'])
        self.assertEqual(eighth_date, group[7]['date'])
        self.assertEqual(ninth_date, group[8]['date'])
        self.assertEqual(tenth_date, group[9]['date'])

if __name__ == '__main__':
    unittest.main()
