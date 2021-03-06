PS_PY: Pub-Sub-Python
=====================


1.0.0.1
-------

* package name changes from pspy to ps_py due to conflict.

1.0.0.0
-------

* General Bugfixes
* Testcases for all functionality


0.1.0.0
-------

PS_PY: A Event Driven programming helper.

* Can create ``callable`` and non-``callable`` subjects.
* Supports any python picklable objects as value.
* Singleton Publisher class helps to get subjects created anywhere in the code to be subscribed to.
* Make any picklable object an event using the ``Of`` operator.
* Combine multiple subscriptions to single one using ``Merge`` operator.
* Manipulate the event value using ``pipe`` attribute along with ``map`` operator.


Dependancies
============

* `python`_>=3.5.9


QuickStart
==========

Installation and Basic Configuration
------------------------------------

1. Install PS_PY: Pub-Sub-Python by running ``pip install ps_py``.
2. There is no specific configuration needed to use ps_py.

.. code:: python

    # **non-callable subject**
    # publisher code
    from ps_py.publisher import Publisher
    publisher = Publisher()
    subject = publisher.add('example_subject', initial_value='example_value')
    subject.next('example_value_1')  # to publish new value.

    # subscriber code
    from ps_py.publisher import Publisher
    publisher = Publisher()
    subject = publisher.get_subject('example_subject')
    # NOTE: The above will create a new subject **if and only if** the subject doesn't exist.

    """Assuming ``on_success``, ``on_error`` are already defined somewhere
    before the below statement.
    ``onSuccess`` is mandatory to subscribe; whereas ``onError`` is optional.
    ``onSuccess``, ``onError``: can be either callable or a ``dict`` of format shown below:
    ``{'func': <callable>, 'args': <None | list | tuple>, 'kwargs': <None | dict>}``
    ``onSuccess``: The callable defined either directly or via dict should take a
    argument (positional or keyword) with name ``value``.
    ``onError``: The callable defined either directly or via dict should take a
    argument (positional or keyword) with name ``error``.
    """
    subscriber = subject.subscribe(onSuccess=on_success, onError=on_error)
    """That is it. at any point the publisher publishes any thing to this subject
    the ``onSuccess`` or ``onError`` will be called accordingly.
    NOTE: if the subject has any value which is not None and not initial_value,
    it will be passed to ``onSuccess`` right away.
    """
    # to unsubscribe
    subscriber.unsubscribe()

    # **callable subject**
    # there is no publisher code for this because the callable will be the publisher
    from ps_py.publisher import Publisher
    publisher = Publisher()
    subject = publisher.add(lambda x,y,z=None: (x, y, z), 'x', 'y', 'z'='z_val', initial_value='init')
    # syntax: subject = publisher.add(<function>, ``*args``, ``**kwargs``)
    """NOTE: The subject callable will not be called/executed until the first subscribe.
    If no subscription the the subject callable will never be called/executed.
    """
    subscriber = subject.subscribe(onSuccess=on_success, onError=on_error)

    # **Creating subjects and using it directly**
    from ps_py.subject import Subject
    # for non-callable subject
    # Subject constructor takes in one mandatory value that is subject unique identifier.
    # ``initial_value`` is optional.
    subject = Subject('example_subject', initial_value='example_value')
    subject.next('example_value_1')

    """Assuming ``on_success``, ``on_error`` are already defined somewhere
    before the below statement.
    """
    subscriber = subject.subscribe(onSuccess=on_success, onError=on_error)

    # for callable subject
    subject = Subject(lambda x,y,z=None: (x, y, z), 'x', 'y', 'z'='z_val', initial_value='init')
    """NOTE: The function passed is called only at the fisrt subscription."""

    """Assuming ``on_success``, ``on_error`` are already defined somewhere
    before the below statement.
    """
    subscriber = subject.subscribe(onSuccess=on_success, onError=on_error)



Basic Usage
===========

Below are some basic ussage for PS_PY package.

example::

    >>>from ps_py.subject import Subject
    >>>sbj = Subject('exp1', initial_value='val1')
    >>>sbj.value
    'val1'
    >>>sbj2 = Subject('exp1', initial_value='val2')
    >>>id(sbj) == id(sbj2)
    True
    >>>sbj.value  # the value of sbj is now the latest that is provided by sbj2
    'val2'
    >>>sbc = sbj.subscribe(onSuccess=lambda value: print(value), onError=None)  # onError is optional, sbj.value is passed to onSuccess; return Subscriber object.
    val2
    >>>sbc1 = sbj.subscribe(onSuccess=lambda value: print(value), onError=None)
    val2
    >>>sbj.next('val3')  # calls the onSuccess of both ``sbc`` anf ``sbc1``; returns
    val3
    val3
    >>>sbc1.unsubscribe()  # ``sbc1`` is obsolete after this point.
    >>>sbj.next([1, 2])  # calls the onSuccess of ``sbc``; any picklable value can be send.
    [1, 2]
    >>>sbj2 = Subject(lambda val, val2=None: (val, val2), 'args', val2='kwargs')
    >>>sbc2 = sbj2.subscribe(onSuccess=lambda value: print(value))
    ('args', 'kwargs')

    >>>from ps_py.contrib import map
    >>>sbj = Subject("pip-map_ex", initial_value='val1')
    >>>sbj1 = sbj.pipe(map(lambda value: "%s:%s"%("modified", value)))
    >>>sbc = sbj1.subscribe(onSuccess=lambda value: print(value))
    modified:val1  # the current value in the sbj is passed down to the pip.
    >>>sbj.next('new_val')
    modified:new_val

    >>>from ps_py.contrib import Merge, map
    >>>sbj1 = Subject("Merge_ex_1")
    >>>sbj2 = Subject("Merge_ex_2")
    >>>mrg = Merge(sbj1, sbj2)
    >>>sbc = mrg.subscribe(onSuccess=lambda value: print(value))
    >>>sbj1.next("first_val")
    first_val
    >>>sbj2.next("second_val")
    second_val
    >>>mrg_sbj = mrg.pipe(map(lambda value: "%s:%s"%("mergePipe", value)))
    >>>sbc1 = mrg_sbj.subscribe(onSuccess=lambda value: print(value))
    mergePipe:second_val  # latest value is passed to the pipe.
    >>>sbj1.next("third_value")
    third_value  # this is the value printed by ``sbc``'s ``onSuccess``
    mergePipe:third_value  # this is the value printed by ``sbc1``'s ``onSuccess``
    >>>sbj2.next("fourth_value")
    fourth_value  # this is the value printed by ``sbc``'s ``onSuccess``
    mergePipe:fourth_value  # this is the value printed by ``sbc1``'s ``onSuccess``
    >>>sbc.unsubscribe()
    >>>sbj1.next("fifth_value")
    mergePipe:fifth_value  # this is the value printed by ``sbc1``'s ``onSuccess``

    >>>from ps_py.contrib import Of, map
    >>>of_obj = Of("val1", ["v", "a", "l", "2"], {"v": "a", "l":3}, timeout=2)
    >>>of_sbj = of_obj.pipe(map(lambda value: "%s:%s"%("ofPipe", value)))
    >>>sbc1 = of_sbj.subscribe(onSuccess=lambda value: print(value))
    >>>sbc = of_obj.subscribe(onSuccess=lambda value: print("of_direct:%s" % value)
    of_direct:val1
    ofPipe:val1
    of_direct:['v', 'a', 'l', '2']
    ofPipe:['v', 'a', 'l', '2']
    of_direct:{'l': 3, 'v': 'a'}
    ofPipe:{'l': 3, 'v': 'a'}



Publisher APIs
==============


subjects
--------

* type: property
* input: None
* output: type->dict; {<subject_name>: <subject>}


get_subject
-----------

* type: method
* input: subject<str | callable>
* output: type->Subject; <subject>


add
---

* type: method
* input: subject<str | callable>, ``*args``, ``**kwargs``
* output: type->Subject; <subject>


subscribe
---------

* type: method
* input: subject<str | callable>, onSuccess<callable | dict {'func': <callable>, args: <None | list | tuple>>, onError<None | callable | dict {'func': <callable>, args: <None | list | tuple>>
* output: type->Subscriber; <subscriber>
* sideEffect: Will call the onSuccess if the subjects current_value != None and current_value != initial_value.


next
----

* type: method
* input: subject<str | callable>, value<any python picklable object>
* output: None



Subject APIs
============


publisher
---------

* type: property
* input: None
* output: type->Publisher; <publisher>


subject
-------

* type: property
* input: None
* output: type->Str | callable; returns the input of the Subject constructor


subscribe
---------

* type: method
* input: onSuccess<callable | dict {'func': <callable>, args: <None | list | tuple>>, onError<None | callable | dict {'func': <callable>, args: <None | list | tuple>>
* output: type->Subscriber; <subscriber>
* sideEffect: Will call the onSuccess if the subjects current_value != None and current_value != initial_value.


add_subscriber
--------------

* type: method
* input: subscriber<Subscriber>
* output: None
* sideEffect: Will call the subscriber.success if the subjects current_value != None and current_value != initial_value.


pipe
----

* type: method
* input: map<Map>, [map<Map>, ...]
* output: map<Map>  # latest pipe to which you can subscribe.


add_pipe
--------

* type: method
* input: map<Map>
* output: map<Map>  # latest pipe to which you can subscribe.


next
----

* type: method
* input: value<any python picklable object>, error<boolean> (default=False)
* output: None


subscribers
-----------

* type: property
* input: None
* output: dict->{<subscriber_name>: subscriber<Subscriber>, ...}


pipes
-----

* type: property
* input: None
* output: list-> [pipe<Map>, ...]


value
-----

* type: property
* input: None
* output: value<current value of the subject; any python picklable object>


unsubscribe
-----------

* type: method
* input: subscriber<Subscriber>
* output: None



Subscriber APIs
===============


name
----

* type: property
* input: None
* output: type-> str


subject
-------

* type: property
* input: None
* output: type-> Subject; The subject to which this subscriber is subscribed to


onSuccess
---------

* type: property
* input: None
* output: type-> partial func; The validated&modified input onSuccess.


onError
---------

* type: property
* input: None
* output: type-> partial func; The validated&modified input onError.


success
-------

* type: method
* input: value <any python picklable object>
* output: None


error
-----

* type: method
* input: error <any python picklable object; mostly Exception object>
* output: None


unsubscribe
-----------

* type: method
* input: None
* output: None



Merge APIs
==========


add
---

* type: method
* input: sub<Subject | Subscribe>
* output: None


subscribe
---------

* type: method
* input: onSuccess<callable | dict {'func': <callable>, args: <None | list | tuple>>, onError<None | callable | dict {'func': <callable>, args: <None | list | tuple>>
* output: type->Subscriber; <subscriber>
* sideEffect: Will call the onSuccess if the subjects current_value != None and current_value != initial_value.


pipe
----

* type: property
* input: None
* output: list-> [pipe<Map>, ...]


subscribers
-----------

* type: property
* input: None
* output: dict->{<subscriber_name>: subscriber<Subscriber>, ...}



Of APIs
=======


subscribe
---------

* type: method
* input: onSuccess<callable | dict {'func': <callable>, args: <None | list | tuple>>, onError<None | callable | dict {'func': <callable>, args: <None | list | tuple>>
* output: type->Subscriber; <subscriber>
* sideEffect: Will call the onSuccess if the subjects current_value != None and current_value != initial_value.


pipe
----

* type: property
* input: None
* output: list-> [pipe<Map>, ...]


subscribers
-----------

* type: property
* input: None
* output: dict->{<subscriber_name>: subscriber<Subscriber>, ...}



.. _python: http://python.org
