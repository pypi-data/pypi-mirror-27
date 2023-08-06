import six


def sum(a, b):
    six.print_('Adding a and b...')
    return a + b

def sum2(a, b):
    six.print_('Hello py 2!', a, b)
    return a + b

def sum3(a, b):
    six.print_('Hello py 3!', a, b, flush=True)
    return a + b
