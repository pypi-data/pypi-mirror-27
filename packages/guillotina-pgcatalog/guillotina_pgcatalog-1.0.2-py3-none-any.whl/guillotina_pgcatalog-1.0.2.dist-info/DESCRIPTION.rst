Introduction
============

Basic catalog implementation for guillotina using the default postgresql
server.


Status
------

This is just a proof of concept right now.

What is does right now:

- provides indexes for basic types
- works with the POST @search endpoint


What it does *not* do:

- check security of what is being queried

1.0.2 (2017-12-30)
------------------

- Fix getting transaction when creating catalog
  [vangheem]


1.0.1 (2017-04-12)
------------------

- fix get_data not using correct signature for latest guillotina
  [vangheem]


1.0.0 (2017-04-10)
------------------

- initial


