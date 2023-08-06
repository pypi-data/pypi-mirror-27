# Overview

[![Build Status](https://travis-ci.org/wontonst/transactionpro-py.svg?branch=master)](https://travis-ci.org/wontonst/transactionpro-py)

TransactionPro-py is used to generate csv files that 
can be consumed by Transaction Pro 6.0

The csv format is from the [data dictionary file][1]
provided by Transaction Pro.

It currently only handles invoices but handling
other imports would be very easy to accomplish.
You can alternatively open up an issue and I can
perhaps find time to implement it for you.

# Installation

TransactionPro is python2.7 and python3 compatible.
Simply run

`pip install transactionpro`

# Usage

```python
from transactionpro.import_types import Invoice
invoice = Invoice()
invoice.add_row(
    customer='Some Company',
    ref_number='123',
    item='Some Item',
)
with open('myfile.csv', 'w') as f:
    invoice.write_to(f)  # saves to file
```

You can also pass a file-like object to save, eg

```python
output = io.StringIO()
invoice.write_csv_to(output)
```

To get a tuple of the field names, you can use
`invoice.fields`. To understand what these fields mean,
take a look at the [data dictionary][1].

# Contribution

This repo is actively monitored. Please open an
issue before contributing new features.

[1]: http://www.baystateconsulting.com/forum/forum_posts.asp?TID=338&title=tpi-field-listing-data-dictionary
