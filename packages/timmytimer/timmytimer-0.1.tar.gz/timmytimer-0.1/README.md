# Timmytimer
Named after the childrens TV-show Timmy Time

A simple wrapper to log/print functionname, \*args and \**kwargs.

## Example Usage

```
from timmytimer import timmy, timmyprint

# set up logger
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

@timmy  # this goes to logging
def func(greeting, name='Henrik'):
    print('{} {}'.format(greeting, name))

@timmyprint  # this just prints
def funcprint(greeting, name='Henrik'):
    print('{} {}'.format(greeting, name))

func('Hello', name='Gustav')
funcprint('Hello', name='Ellinor')
```
output:
```
Hello Gustav
2017-12-25 23:50:53,699 - __main__ - DEBUG - function:func args:('Hello',) kwargs:{'name':'Gustav'} - time: 2.8371810913085938e-05
Hello Ellinor
2017-12-25T23:50:53.699207 - __main__  -  funcprint(('Hello',),{'name': 'Ellinor'})  -  time:7.62939453125e-06
```

## INSTALL
pip install timmytimer

### Import
from timmytimer import timmy, timmyprint

and then add @timmy above any defined function or procedure to output to log.
