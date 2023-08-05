"""Occurrences.

trade: Financial Application Framework
http://trade.readthedocs.org/
https://github.com/rochars/trade
License: MIT

Copyright (c) 2015-2017 Rafael da Silva Rocha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import absolute_import
from __future__ import division

import math
from . accumulator import Occurrence, Subject

from . utils import (
    average_price,
    same_sign,
    merge_operations,
    find_purchase_and_sale
)


class Asset(Subject):
    """An asset represents anything that can be traded."""

    default_state = {
        'quantity': 0,
        'price': 0,
        'results': {}
    }

    def __init__(self, symbol=None, name=None, expiration_date=None, **kwargs):
        super(Asset, self).__init__(symbol, name, expiration_date)
        self.underlying_assets = kwargs.get('underlying_assets', {})


class Operation(Occurrence):
    """An Operation represents an occurrence with an Asset.

    Class Attributes:
        update_position: A boolean indication if the operation should
            update the position of the accumulator or not.
        update_results: A boolean indication if the operation should
            update the results of the accumulator or not.
        update_container: A boolean indication if the operation should
            update the context in a OperationContainer or not.

    Attributes:
        date: A string 'YYYY-mm-dd', the date the operation occurred.
        subject: An Asset instance, the asset that is being traded.
        quantity: A number representing the quantity being traded.
            Positive quantities represent a purchase.
            Negative quantities represent a sale.
        price: The raw unitary price of the asset being traded.
        commissions: A dict of discounts. String keys and float values
            representing the name of the discounts and the values
            to be deducted added to the the operation value.
        operations: A list of underlying occurrences that the
            might may have.

    """

    # By default every operation
    # updates the accumulator position
    update_position = True

    # By default every operation
    # updates the accumulator results
    update_results = True

    # By default every operation updates
    # the OperationContainer positions
    update_container = True

    def __init__(self, subject=None, date=None, **kwargs):
        super(Operation, self).__init__(subject, date)
        self.quantity = kwargs.get('quantity', 0)
        self.price = kwargs.get('price', 0)
        self.commissions = kwargs.get('commissions', {})
        self.raw_results = kwargs.get('raw_results', {})
        self.operations = kwargs.get('operations', [])

    @property
    def results(self):
        """Returns the results associated with the operation."""
        return self.raw_results

    @property
    def real_value(self):
        """Returns the quantity * the real price of the operation."""
        return self.quantity * self.real_price

    @property
    def real_price(self):
        """Returns the real price of the operation.

        The real price is the price with all commission and costs
        already deducted or added.
        """
        return self.price + math.copysign(
            self.total_commissions / self.quantity,
            self.quantity
        )

    @property
    def total_commissions(self):
        """Returns the sum of all commissions of this operation."""
        return sum(self.commissions.values())

    @property
    def volume(self):
        """Returns the quantity of the operation * its raw price."""
        return abs(self.quantity) * self.price

    def update_accumulator(self, accumulator):
        """Updates the accumulator with the operation data."""
        if self.need_position_update(accumulator):
            self.update_positions(accumulator)
        if self.update_results:
            self.update_accumulator_results(accumulator)

    def update_accumulator_results(self, accumulator):
        """Updates the results stored in the accumulator."""
        for key, value in self.results.items():
            if key not in accumulator.state['results']:
                accumulator.state['results'][key] = 0
            accumulator.state['results'][key] += value

    def need_position_update(self, accumulator):
        """Check if there is a need to update the position."""
        return (
            self.subject.symbol == accumulator.subject.symbol and
            self.quantity
        )

    def update_position_different_sign(self, accumulator, new_quantity):
        """Update when the operation and position have opposing signs."""
        # if we are trading more than the amount in the portfolio
        # the result will be calculated based only on what was traded
        # (the rest creates a new position)
        if abs(self.quantity) > abs(accumulator.state['quantity']):
            result_quantity = accumulator.state['quantity'] * -1
        else:
            result_quantity = self.quantity
        results = \
            result_quantity * accumulator.state['price'] - \
            result_quantity * self.real_price
        if results:
            self.results['trades'] = results
        if not same_sign(accumulator.state['quantity'], new_quantity):
            accumulator.state['price'] = self.real_price

    def update_position_same_sign(self, accumulator):
        """Update position when operation and position have the same sign."""
        accumulator.state['price'] = average_price(
            accumulator.state['quantity'],
            accumulator.state['price'],
            self.quantity,
            self.real_price
        )

    def update_positions(self, accumulator):
        """Updates the state of the asset with the operation data."""
        new_quantity = accumulator.state['quantity'] + self.quantity
        # same sign, udpate the cost
        if same_sign(accumulator.state['quantity'], self.quantity):
            self.update_position_same_sign(accumulator)
        # different signs, update the results
        elif accumulator.state['quantity'] != 0:
            self.update_position_different_sign(accumulator, new_quantity)
        else:
            accumulator.state['price'] = self.real_price
        accumulator.state['quantity'] = new_quantity
        if not accumulator.state['quantity']:
            accumulator.state['price'] = 0


class Daytrade(Operation):
    """A daytrade operation.

    Daytrades are operations of purchase and sale of an asset on
    the same date.

    Attributes:
        asset: An asset instance, the asset that is being traded.
        quantity: The traded quantity of the asset.
        purchase: A Operation object representing the purchase of the
            asset.
        sale: A Operation object representing the sale of the asset.
        update_position: Set to False, as daytrades don't change the
            portfolio position; they just create results.
    """

    update_position = False

    def __init__(self, operation_a, operation_b):
        """Create the daytrade object. A daytrade have 2 operations.

        - a purchase operation
        - a sale operation.
        """
        super(Daytrade, self).__init__(
            date=operation_a.date, subject=operation_a.subject,
        )
        purchase, sale = find_purchase_and_sale(operation_a, operation_b)
        self.extract_daytrade(purchase, sale)
        self.operations = [
            Operation(
                date=purchase.date,
                subject=purchase.subject,
                quantity=self.quantity,
                price=purchase.price
            ),
            Operation(
                date=sale.date,
                subject=sale.subject,
                quantity=self.quantity*-1,
                price=sale.price
            )]

    @property
    def results(self):
        """Returns the profit or the loss generated by the day trade."""
        return {
            'daytrades': abs(self.operations[1].real_value) - \
                                        abs(self.operations[0].real_value)
        }

    def update_accumulator(self, accumulator):
        """Updates the accumulator state with the day trade result."""
        self.update_accumulator_results(accumulator)

    def extract_daytrade(self, purchase, sale):
        """Extracts the daytraded quantity from 2 operations."""
        self.quantity = min([purchase.quantity, abs(sale.quantity)])
        purchase.quantity -= self.quantity
        sale.quantity += self.quantity

    def append_to_positions(self, container):
        """Saves a Daytrade object in the container.

        If there is already a day trade with the same asset on the
        container, then the day trades are merged.
        """
        if 'positions' not in container.context:
            container.context['positions'] = {}

        if 'daytrades' not in container.context['positions']:
            container.context['positions']['daytrades'] = {}

        if self.subject.symbol in container.context['positions']['daytrades']:
            self.merge_underlying(container, 0)
            self.merge_underlying(container, 1)
            container.context['positions']['daytrades'][self.subject.symbol].quantity +=\
                self.quantity
        else:
            container.context['positions']['daytrades'][self.subject.symbol] = self

    def merge_underlying(self, container, operation_index):
        """Merges one day trade underlying operation."""
        merge_operations(
            container.context['positions']['daytrades'][self.subject.symbol]\
                .operations[operation_index],
            self.operations[operation_index]
        )
