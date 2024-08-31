Findemail (`findemail.io`_)
========

|logo| **Findemail** is a python library for interacting with the `findemail.io`_ API as a user.


What is this?
-------------

Findemail offers a convenient email-finding service as part of its comprehensive email outreach platform. Identify and engage with key individuals crucial to your business success. Targeted Email leads for
    * Lists for specific VIP and Common industries or niches
    * Trading and Exchange And Cryptocurrency Users And Companies
    * Customized email marketing campaigns for small businesses
    * real estate agents and brokers
    * healthcare professionals and medical practices
    * e-commerce businesses looking to grow their customer base
    * lists for technology companies and startups
    * marketing services for restaurants and food service businesses
    * financial advisors and investment firms
    * campaigns for fitness and wellness professionals
    * event planners and entertainment companies
    * Targeted email leads for travel agencies and tourism businesses
    * marketing services for non-profit organizations and charities
    * educational institutions and online learning platforms
    * campaigns for beauty salons and spas
    * legal professionals and law firms
    * small business owners looking to expand their reach
    * automotive dealerships and repair shops
    * pet care businesses and animal shelters
    * home improvement contractors and renovation companies
    * marketing agencies looking to connect with potential clients
    * Etc.

Installing
----------

.. code-block:: sh

  pip3 install findemail


Creating a client
-----------------

.. code-block:: python

    from findemail import Client, errors
    from json import dumps


    api_key = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee'

    client = Client(api_key)

    print(dumps(
        client.get_me(), indent=4
    ))


Doing stuff
-----------

.. code-block:: python

    "Handle Domain Search."

    data = client.search_domain('google.com')
    print(dumps(
        data, indent=4
    ))


    "Handle Leak Search."

    data = client.search_leak('google.com', 'domain') # _type: (domain, username, email, phone_number, ip)
    print(dumps(
        data, indent=4
    ))


    "Handle Logs Search."

    data = client.search_logs('google.com', 'domain') # _type: (domain, username, port, tech, keyword, sub_domain or subdomain)
    print(dumps(
        data, indent=4
    ))

    # Example response for all requests
    # 
    # {
    #     "ok": true,
    #     "code": 200,
    #     "data": {
    #         "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",
    #         "domain": "example.com",
    #         "result": [
    #             {
    #                 "email": "test@example.com",
    #                 "...": "..."
    #             }
    #         ],
    #         "download": [
    #             {
    #                 "id": "1",
    #                 "credit": 1,
    #                 "limit": 5000
    #             }
    #         ],
    #         "count": 26,
    #         "time": 1714207384
    #     }
    # } 
    # or 
    # {
    #     "ok": false,
    #     "code": 400,
    #     "message": "Error Message"
    # }

    """
    Handle Download File

    By default, the file will be saved in the same directory as the module used.
    If you want to change the path or the name of the file,
    simply enter the new file name or the exact file address.
    """

    file_name = client.download(
        data['id'],
        data['download'][0]['id'],
        file_name=None or "result.txt"
    )

    print(file_name)

    # result.txt or aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee.txt


Next steps
----------

Do you like how Findemail looks? Check out `Read The Docs`_ for a more
in-depth explanation, with examples, troubleshooting issues, and more
useful information.

.. _findemail.io: https://findemail.io/
.. _Read The Docs: https://api.findemail.io/

.. |logo| image:: logo.svg
    :width: 24pt
    :height: 24pt