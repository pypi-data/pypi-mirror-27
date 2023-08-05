Django ORM + Twisted + asyncio - blocking
----------------------------------------
This is a library that contains a custom queryset and a custom manager that adds introspection to use
the twisted database api instead of django. It returns deferred (Future or coroutine) instead of just hitting the database.


since v0.6:
-----------
- added support for django_bulk_update (github.com/aykut/django-bulk-update)


since v0.5:
-----------
- model instance save method replacing on the fly, now u can:
```python
await obj.save()
```

since v0.3-0.4:
-----------
- get_or_create fix


since v0.2:
-----------
- mostly rewrited;
- renamed package as "twisted-django-orm";
- python 3.5.2+ now is required;
- used asyncio to avoid "callback hell";
- you still can obtain result as defered;
- there are some untested cases;
 

To install:
-----------
Python 3.5.2+ is required

1. pip install twango
2. Import and set the manager as the manager for any model (see examples)
3. Use it on the top of the twisted and asyncio

This will keep the orm from blocking when using the django orm!

Important
-----------
Does not make job in asynchronous way, but goes into threads and do not perform blocking main reactor.

Example 352+:
--------
```python

q = await Operation.twisted.all()[:5].fetch()
print(q)

b = await Operation.twisted.all().fetch()
print(b[5])

async for x in Operation.twisted.all().order_by('cell', 'status'):
    print(x.price, x.status, x.cell)

async for x in Operation.twisted.all().order_by('cell', 'status')[:5]:
    print(x.price, x.status, x.cell)

x = await Operation.twisted.get(price=3000, status=1, cell=11)
print(x)

p = await Operation.twisted.count()
print(p)

x, created = await Operation.twisted.update_or_create(defaults={'cell': 11, 'price': 333}, price=1, status=1, cell=25)
print(x)

x, _created = await Operation.twisted.get_or_create(price=27, status=1, cell=11)
print(x)
```

Example (old):
--------
You can create models that are separate to be used in twisted processes:

```python
from myapp import Book
from twango.manager import TwistedManager
from django.db.models.manager import Manager

class TwistedBook(Book):
    objects = Manager()
    twisted = TwistedManager()

    class Meta:
        app_label = 'myapp'
        proxy = True
```
