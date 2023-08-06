=========================
Starter Server API Client
=========================


Install
=======
pip install starter_api


Usage
=====
.. code-block:: python

    import starter_api

    starter_api.init("http://HOST:PORT")

    # simple build and submit task to server
    res = starter_api.build_submit("YOUR_SERVICE", {"myparam": 1})
    print('res = ' + str(res))

    # build task object into variable and submit to server
    task = starter_api.build_task("YOUR_SERVICE", {"myparam": 1})
    task_dict = starter_api.submit(task)
    print('str(task_dict))
    # {u'status': u'NEW', u'retries': 0, u'origin': u'USER', u'sessionId': None, u'serviceId': u'adptools.schema_db', u'dateTarget': u'2017-10-24T20:01:26Z', u'taskId': u'3f7ddc54-17ee-4a0c-8b8e-b6854613c315', u'agentId': None, u'data': {u'myparam': 1}, u'processingResult': None}




