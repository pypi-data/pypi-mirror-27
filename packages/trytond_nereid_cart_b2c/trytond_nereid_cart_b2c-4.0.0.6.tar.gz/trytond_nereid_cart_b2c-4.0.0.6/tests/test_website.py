#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

    Test website

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) LTD
    :license: GPLv3, see LICENSE for more details
'''
import json

from trytond.tests.test_tryton import POOL, with_transaction
from test_product import BaseTestCase


class TestWebsite(BaseTestCase):
    """
    Test website
    """
    @with_transaction()
    def test_0010_user_status(self):
        """
        Test that `_user_status()` returns dictionary with correct params.
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_client() as c:
            self.login(c, 'email@example.com', 'password')

            SaleLine = POOL.get('sale.line')

            product, = self.Product.search([('name', '=', 'product-1')])

            rv = c.post(
                '/cart/add',
                data={
                    'product': product.id, 'quantity': 7
                }
            )
            self.assertEqual(rv.status_code, 302)

            line, = SaleLine.search([])
            results = c.get('/user_status')

            data = json.loads(results.data)
            lines = data['status']['cart']['lines']

            self.assertEqual(len(lines), 1)
            self.assertEqual(line.serialize('cart'), lines[0])
