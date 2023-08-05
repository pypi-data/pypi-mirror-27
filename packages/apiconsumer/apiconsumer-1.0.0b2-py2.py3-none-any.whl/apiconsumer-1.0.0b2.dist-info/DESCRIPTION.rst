APICONSUMER: A super lightweight REST API requests wrapper
==========================================================

Following the same philosophy of Requests module (REST) ApiConsumer is here to make your life easier.

Are you lazy enough to configure authentication for every single request? How about handling errors? Wouldn't it be
great if all that could be done in 2 lines?


How to use
----------

Behold the power of ApiConsumer:

.. code-block:: python

    >>> from apiconsumer import ApiConsumer
    >>> my_api = ApiConsumer(url='https://myapi.com', extra_headers={'Authorization': 'JWT mytoken'})
    >>> users = my_api.get_users()


Making POST request is also easy:

.. code-block:: python

    >>> new_user = my_api.post_users(data={'email': 'someguy@something.com', 'password': 'correct-horse-battery-staple'})


How to install
--------------
.. code-block:: bash

    $ pip install apiconsumer


Contribute
----------
Be our guest. We'd like to see your awesome ideas. Just fork the repo, create a branch and create pull request.



