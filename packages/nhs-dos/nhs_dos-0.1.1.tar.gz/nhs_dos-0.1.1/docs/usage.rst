=====
Usage
=====

To use the NHS DoS client library in a project::

    from nhs_dos import User


Firstly, you will need to create a User object using your API credentials::

    u = nhs_dos.User('my_username', 'my_password')

This object can then be used with either the REST or SOAP APIs.

REST API
--------
Firstly, create a RestApiClient object, passing in your User object::


    client = RestApiClient(u)


SOAP API
--------
Firstly, create a SoapApiClient object, passing in your User object::

    client = SoapApiClient(u)

