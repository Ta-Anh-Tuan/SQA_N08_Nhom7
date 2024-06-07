from django.test import TestCase
from .models import *
from .forms import *
import unittest
import inc_dec


class TestModels(TestCase):

    def setUp(self):
        self.client = Client.objects.create(
            meter_number=1234567,
            first_name='Le',
            middle_name='Thanh',
            last_name='Tong',
            contact_number='+639123456789',
            address='123 Main St., Tang8, Dianguc',
            status='Connected'
        )

    def test_client_str(self):
        # Kiểm tra chuỗi đại diện của Client
        expected_str = 'Tong, Le Thanh'
        actual_str = str(self.client)
        self.assertEqual(actual_str, expected_str)

    def test_client_status(self):
        # Kiểm tra trạng thái của Client
        self.assertEqual(self.client.status, 'Connected')

    def test_water_bill_payable_with_penalty(self):
        # Tạo một Metric mới
        metric = Metric.objects.create(consump_amount=1, penalty_amount=2)

        # Tạo một WaterBill mới
        bill = WaterBill.objects.create(
            name=self.client,
            meter_consumption=100,
            status='Paid',
            duedate=datetime.date.today(),
            penaltydate=datetime.date.today()
        )

        # Tính tổng tiền phải trả, bao gồm tiền phạt
        expected_payable = bill.meter_consumption + metric.penalty_amount
        actual_payable = bill.payable()
        self.assertEqual(actual_payable, expected_payable)

    def test_metric_amounts(self):
        # Tạo một Metric mới và kiểm tra giá trị của nó
        metric = Metric.objects.create(consump_amount=1, penalty_amount=2)
        self.assertEqual(metric.consump_amount, 1)
        self.assertEqual(metric.penalty_amount, 2)

class TestForms(TestCase):

    def test_bill_form_valid(self):
        # Tạo dữ liệu form cho BillForm
        form_data = {
            'name': Client.objects.create(
                meter_number=1234567,
                first_name='Nguyen',
                middle_name='Cao',
                last_name='Anh',
                contact_number='+639123456789',
                address='123 Main St., Tang7, Dianguc',
                status='Connected'
            ).id,
            'meter_consumption': 100,
            'status': 'Pending',
            'duedate': datetime.date.today(),
            'penaltydate': datetime.date.today()
        }
        form = BillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_form_valid(self):
        # Tạo dữ liệu form cho ClientForm
        form_data = {
            'meter_number': 1234567,
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'contact_number': '+639123456789',
            'address': '123 Main St., Anytown, USA',
            'status': 'Connected'
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_metrics_form_valid(self):
        # Tạo dữ liệu form cho MetricsForm
        form_data = {
            'consump_amount': 1,
            'penalty_amount': 2
        }
        form = MetricsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_form_invalid(self):
        # Tạo dữ liệu form không hợp lệ cho ClientForm
        form_data = {
            'meter_number': '',  # meter_number rỗng
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'contact_number': '+639123456789',
            'address': '123 Main St., Anytown, USA',
            'status': 'Connected'
        }
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_bill_form_invalid(self):
        # Tạo dữ liệu form không hợp lệ cho BillForm
        form_data = {
            'name': '',  # name rỗng
            'meter_consumption': 100,
            'status': 'Pending',
            'duedate': datetime.date.today(),
            'penaltydate': datetime.date.today()
        }
        form = BillForm(data=form_data)
        self.assertFalse(form.is_valid())
