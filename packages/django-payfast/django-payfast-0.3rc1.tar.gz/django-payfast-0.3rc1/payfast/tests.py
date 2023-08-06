# coding: utf-8
from __future__ import unicode_literals

import json
import unittest
from collections import OrderedDict

import django
from django.test import TestCase

from payfast.forms import notify_url, PayFastForm, NotifyForm
from payfast.models import PayFastOrder
from payfast.api import signature
from payfast import conf
import payfast.signals


def _test_data():
    return OrderedDict([
        ('merchant_id', '10000100'),
        ('merchant_key', '46f0cd694581a'),
        ('notify_url', "http://127.0.0.1:8000/payfast/notify/"),
        ('name_first', "Вася"),
        ('last_name', 'Пупников'),
        ('m_payment_id', '23'),
        ('amount', '234'),
        ('item_name', "Payment (Планета суши). ID:272-15"),
    ])


def _notify_data(data, payment_form):
    notify_data = data.copy()
    # prepare server data
    notify_data['m_payment_id'] = payment_form.order.m_payment_id
    notify_data['amount_gross'] = data['amount']
    del notify_data['amount']
    del notify_data['merchant_key']
    notify_data['signature'] = NotifyForm._calculate_itn_signature(notify_data)
    return notify_data


def _order():
    return PayFastOrder.objects.all()[0]


class SignatureTest(unittest.TestCase):
    def test_signature(self):
        data = _test_data()
        self.assertEqual(signature(data), 'c71d41dd5041bf28d819fe102ab0106b')


class NotifyTest(TestCase):

    def setUp(self):
        conf.IP_ADDRESSES = ['127.0.0.1']
        conf.USE_POSTBACK = False
        conf.MERCHANT_ID = '10000100'
        conf.REQUIRE_AMOUNT_MATCH = True

        self.notify_handler_orders = []  # type: list
        payfast.signals.notify.connect(self.notify_handler)

    def tearDown(self):
        payfast.signals.notify.disconnect(self.notify_handler)

    def notify_handler(self, sender, order, **kwargs):
        self.notify_handler_orders.append(order)

    def _create_order(self):
        """
        Create a payment order, and return the notification data for it.
        """
        data = _test_data()

        # user posts the pay request
        payment_form = PayFastForm(initial={
            'amount': data['amount'],
            'item_name': data['item_name']
        })
        self.assertEqual(_order().trusted, None)

        return _notify_data(data, payment_form)

    def _assertBadRequest(self, response, expected_json):
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        response_json = json.loads(response.content)
        self.assertEqual(response_json, expected_json)

    def test_notify(self):
        notify_data = self._create_order()
        order = _order()

        # the server sends a notification
        response = self.client.post(notify_url(), notify_data)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.notify_handler_orders, [order])

        order = _order()
        self.assertEqual(order.request_ip, '127.0.0.1')
        self.assertEqual(order.debug_info, '')
        self.assertEqual(order.trusted, True)

    def test_untrusted_ip(self):
        """
        The notify handler rejects notification attempts from untrusted IP address.
        """
        notify_data = self._create_order()

        # the server sends a notification
        response = self.client.post(notify_url(), notify_data, REMOTE_ADDR='127.0.0.2')
        self._assertBadRequest(response, {
            '__all__': [{'code': '', 'message': 'untrusted ip: 127.0.0.2'}],
        })
        self.assertEqual(self.notify_handler_orders, [])

        order = _order()
        self.assertEqual(order.request_ip, '127.0.0.2')
        self.assertEqual(order.debug_info, '__all__: untrusted ip: 127.0.0.2')
        self.assertEqual(order.trusted, False)

    def test_non_existing_order(self):
        response = self.client.post(notify_url(), {})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.notify_handler_orders, [])

        self.assertQuerysetEqual(PayFastOrder.objects.all(), [])

    def test_invalid_request(self):
        form = PayFastForm(initial={'amount': 100, 'item_name': 'foo'})
        notify_data = {'m_payment_id': form.order.m_payment_id}
        notify_data['signature'] = NotifyForm._calculate_itn_signature(notify_data)
        response = self.client.post(notify_url(), notify_data)
        expected_amount = ('100' if django.VERSION < (1, 8) else
                           '100.00' if django.VERSION < (2, 0) else
                           '100')
        self._assertBadRequest(response, {
            'amount_gross': [{'code': '', 'message': ('Amount is not the same: {} != None'
                                                      .format(expected_amount))}],
            'item_name': [{'code': 'required', 'message': 'This field is required.'}],
            'merchant_id': [{'code': 'required', 'message': 'This field is required.'}],
        })
        self.assertEqual(self.notify_handler_orders, [])

        order = _order()
        self.assertEqual(order.request_ip, '127.0.0.1')
        self.assertEqual(set(order.debug_info.split('|')), {
            'amount_gross: Amount is not the same: {} != None'.format(
                '100' if django.VERSION < (1, 8) else
                # Django 1.8+ returns more precise DecimalField values
                '100.00' if django.VERSION < (2, 0) else
                # Django 2.0+ returns less precise DecimalField values again.
                '100'
            ),
            'item_name: This field is required.',
            'merchant_id: This field is required.',
        })
        self.assertEqual(order.trusted, False)
