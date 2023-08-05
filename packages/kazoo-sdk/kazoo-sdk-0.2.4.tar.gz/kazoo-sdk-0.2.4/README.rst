Installing
==========

Install from pip::

    pip install kazoo-sdk


Authentication
==============

Either authenticate using a username/password pair::

    >>>import kazoo
    >>>client = kazoo.Client(username='myusername', password='mypassword',
                             account_name='my account name',
                             base_url='http://api.example.com:8000/v1')
    >>>client.authenticate()

Or using an api key::

    >>>import kazoo
    >>>client = kazoo.Client(api_key="sdfasdfas")
    >>>client.authenticate()

The default api url is: 'http://api.2600hz.com:8000/v1'.  You can override this
by supplying an extra argument, 'base_url' to kazoo.Client().

Example of overriding 'base_url'::

    >>>client = kazoo.Client(base_url='http://api.example.com:8000/v1',
                             api_key="sdfasdfas")

API calls which require data take it in the form of a required argument
called 'data' which is the last argument to the method. For example ::

    >>>client.update_account(acct_id, {"name": "somename", "realm":"superfunrealm"})

Dictionaries and lists will automatically be converted to their appropriate
representation so you can do things like: ::

    >>>client.update_callflow(acct_id, callflow_id, {"flow":{"module":"somemodule"}})

Invalid data will result in an exception explaining the problem.

The server response is returned from each method as a python dictionary of
the returned JSON object, for example: ::

    >>>client.get_account(acct_id)
    {'auth_token': 'abc437daf8517d0454cc984f6f09daf3',
     'data': {'billing_mode': 'normal',
      'caller_id': {},
      'caller_id_options': {},
      'id': 'c4f64412ad0057222c12559a3e7da011',
      'media': {'bypass_media': 'auto'},
      'music_on_hold': {},
      'name': 'test3',
      'notifications': {},
      'realm': '4c8b50.sip.2600hz.com',
      'superduper_admin': False,
      'timezone': 'America/Los_Angeles',
      'wnm_allow_additions': False},
     'request_id': 'ea6441422fb85f67ad21db4f1e2326c1',
     'revision': '3-c16dd0a629fe1da254fe1e7b3e5fb35a',
     'status': 'success'}

For each resource exposed by the kazoo api there are corresponding methods
on the client. For example, for the 'callflows' resource the
correspondence is as follows. ::

    GET /accounts/{account_id}/callflows -> client.get_callflows(acct_id)
    GET /accounts/{account_id}/callflows/{callflow_id} -> client.get_callflow(acct_id, callflow_id)
    PUT /accounts/{account_id}/callflows/ -> client.create_callflow(acct_id, data)
    POST /account/{account_id}/callflows/{callflow_id} -> client.update_callflow(acct_id, data)
    DELETE /account/{account_id}/callflows/{callflow_id} -> client.delete_callflow(acct_id, callflow_id)

Some resources do not have all methods available, in which case they are
not present on the client.

There are also some resources which don't quite fit this paradigm, they are: ::

    GET /accounts/{account_id}/media -> client.get_all_media(acct_id)
    GET /accounts/{account_id}/children -> client.get_account_children(acct_id)
    GET /accounts/{account_id}/descendants -> client.get_account_descendants(acct_id)
    GET /accounts/{account_id}/devices/status -> client.get_all_devices_status(acct_id)
    GET /accounts/{account_id}/servers/{server_id}/deployment -> client.get_deployment(acct_id, server_id)
    GET /accounts/{account_id}/users/hotdesk -> client.get_hotdesk(acct_id)

The kazoo Rest API documentation is available at https://2600hz.atlassian.net/wiki/display/APIs/Configuration+APIs

You can see a list of available client methods at: https://kazoo-api.readthedocs.org/en/latest/
