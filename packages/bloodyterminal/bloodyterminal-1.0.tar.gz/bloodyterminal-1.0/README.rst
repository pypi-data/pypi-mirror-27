Bloody Terminal
===============

A simple piece of code to help structure your console outputs. BT makes
use of colorama to provide a few options to create a consistent console
output “theme”. 

----

.. code:: python

    from bloodyterminal import bt

    bt.success("your string")
    bt.info("your string")
    bt.warning("your string")
    bt.debug("your string")
    bt.custom("your prefix", "your string")

Will result in something like this: 

|alt text|

.. |alt text| image:: https://d3vv6lp55qjaqc.cloudfront.net/items/0O0b1D0Y0f320U1u3D2Q/Image%202017-12-15%20at%207.10.11%20AM.png?X-CloudApp-Visitor-Id=411fc111b6ab769874aa3f398e8fb6a6&v=54bae9c2

The [INFO] prefix has a more vibrant yellow color in most terminals.

To test this you can also use bt.demo() to get this output.
