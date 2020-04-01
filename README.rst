PSPY: Pub-Sub-Python
================


0.1.0.0
-------

PSPY: A Event Driven programming helper.

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

1. Install PSPY: Pub-Sub-Python by running ``pip install pspy``.


Basic Usage
===========

Below are some basic ussage for PSPY package.

example::

    >>>from pspy.subject import Subject
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

    >>>from pspy.contrib import map
    >>>sbj = Subject("pip-map_ex", initial_value='val1')
    >>>sbj1 = sbj.pipe(map(lambda value: "%s:%s"%("modified", value)))
    >>>sbc = sbj1.subscribe(onSuccess=lambda value: print(value))
    modified:val1  # the current value in the sbj is passed down to the pip.
    >>>sbj.next('new_val')
    modified:new_val

    >>>from pspy.contrib import Merge, map
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

    >>>from pspy.contrib import Of, map
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


.. _python: http://python.org
