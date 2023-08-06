=======
Summary
=======

Laminated provide dictionary like object with the layers support. The
general suppose is a data set with fluctuations in differents pieces.

--------------
Quick Examples
--------------

Example 1
---------

.. code:: python

    from laminated import Laminated

    # The company FOO has employeers with this paymenths in month
    inition_employee_pay = {
        'John': 120000,
        'Mike': 150000,
        'Sara': 80000,
        'David': 60000,
    }

    l = Laminated()
    l.add_layer(
        name='2017-01',
        data=inition_employee_pay,
    )

    # John have increase pays in february
    l.add_layer(
        name='2017-02',
        data={
            'John': 130000,
        },
    )

    # March have no any differences, that layer is empty
    l.add_layer({}, '2017-03')

    # In April Sara groing up
    l.add_layer(
        name='2017-04',
        data={
            'Sara': 100000,
        },
    )

    # how many company FOO spend money on they workers by months
    amount = 0
    for month in l.get_layers_names():
        for employee in l:
            amount += l.get_value_at_layer(month, employee)

    # the result will be 1690000
    print('Total amount of pays is {}'.format(amount))
