import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
# Wait for debugger to attach
ptvsd.wait_for_attach()
ptvsd.break_into_debugger()

## CODE GOES UNDERNEATH THIS LINE ##

import theano
import theano.tensor as T
x = T.dmatrix('x')
s = 1 / (1 + T.exp(-x))
logistic = theano.function([x], s)
vals = logistic([[0, 1], [-1, -2]])
print vals