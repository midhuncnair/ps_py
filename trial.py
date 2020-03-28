#! /usr/bin/env python3
# GLOBALITEMS = {}


# class A:
#     """
#     """
#     def __new__(self, *args):
#         """
#         """
#         print("args = ", args)
#         name = args[0]

#         if name not in GLOBALITEMS:
#             GLOBALITEMS[name] = super().__new__(self)
#         return GLOBALITEMS[name]

#     def __init__(self, name, value):
#         """
#         """
#         print("in init with name and value ", name, value)
#         self.name = name
#         self.value = value

#     @property
#     def subscribers(self):
#         """
#         """
#         try:
#             if not isinstance(self._subscribers, dict):
#                 self._subscribers = {}
#         except AttributeError:
#             self._subscribers = {}

#         return self._subscribers


# if __name__ == "__main__":
#     a1 = A("midhun", "v1")
#     a1.subscribers["a1"] = "a1"
#     print("a1.subscribers = ", a1.subscribers)
#     # print("a1-%s"%id(a1))
#     # print("GLobalItems = ", GLOBALITEMS)
#     b1 = A("chandran", "c1")
#     print("b1.subscribers = ", b1.subscribers)
#     # print("b1-%s"%id(b1))
#     # print("GLobalItems = ", GLOBALITEMS)
#     a2 = A("midhun", "m1")
#     print("a2.subscribers = ", a2.subscribers)
#     # print("a2-%s"%id(a2))
#     # print("GLobalItems = ", GLOBALITEMS)
#     b2 = A("chandran", "c2")
#     print("b2.subscribers = ", b2.subscribers)
#     # print("b2-%s"%id(b2))
#     # print("GLobalItems = ", GLOBALITEMS)
#     print("id(a1) == id(a2)", id(a1) == id(a2))
#     print("id(b1) == id(b2)", id(b1) == id(b2))
#     print("id(a1) == id(b2)", id(a1) == id(b2))
#     print("id(b1) == id(a2)", id(b1) == id(a2))


import sys
import os
import pdb

sys.path.insert(0, "/Users/midhunch/workspace/pspy")


from pspy import Subject, Publisher, Merge, Of, map

# sub = Subject("Midhun", "Handsome!")
# pub = Publisher("Manisha", "Beautiful")
# sub.pipe(map(lambda value: print("\n\npipe map ", value, "\n\n")))

# def on_success(value):
#     """
#     """
#     print("Onsuccess called with value", value)

# sub.subscribe(onSuccess=on_success)

# sub.next("Wonderful")
# sub1 = pub.get_subject("Manisha")

# merge = Merge(sub, sub1)
# merge.subscribe(onSuccess=lambda value: print("\n\nmergeSuccess", value, "\n\n"), onError=lambda error: print("mergeError", error))

# def on_success2(v1, value):
#     print("on_success2 called with values", v1, value)

# sub1.subscribe(onSuccess={'func': on_success2, 'args':('v1_sub',)})
# print("what what")
# sub1.next("Awesome")

# sub1.subscribe(onSuccess=lambda value: print("lambda value = ", value))
# sub1.next("Awesomeness")

# sub.subscribe(onSuccess=lambda value: print("\n1", value))
# sub.subscribe(onSuccess=lambda value: print("\n2", value))
# sub.subscribe(onSuccess=lambda value: print("\n3", value))
# sub1.subscribe(onSuccess=lambda value: print("\n1", value))
# sub1.subscribe(onSuccess=lambda value: print("\n2", value))
# sub1.subscribe(onSuccess=lambda value: print("\n3", value))

# sub1.next("mass")
# sub.next({'a':'b'})

# l1 = [1,2,3, {1,2,3}, (1,2,3), {'a':'b'}]

# of_item = Of(*l1)

# of_item.subscribe(onSuccess=lambda value: print("\nof value1", value, "\n"))
# of_item.subscribe(onSuccess=lambda value: print("\nof value2", value, "\n"))

# sb = sub.subscribe(onSuccess=lambda value: print("\nSubscribe unsubscribe test ", value, "\n"))
# sub.next("test")
# sub.next("test1")
# sb.unsubscribe()
# sub.next("test3")

# # pdb.set_trace()

# import tests
