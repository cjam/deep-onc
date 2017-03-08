import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
# Wait for debugger to attach
ptvsd.wait_for_attach()
#ptvsd.break_into_debugger()

## CODE GOES UNDERNEATH THIS LINE ##

# # Theano Examples
# import theano
# import theano.tensor as T

# # This example is from http://deeplearning.net/software/theano/tutorial/examples.html#logistic-function
# x = T.dmatrix('x')
# s = 1 / (1 + T.exp(-x))
# logistic = theano.function([x], s)
# vals = logistic([[0, 1], [-1, -2]])


# # http://deeplearning.net/software/theano/tutorial/examples.html#computing-more-than-one-thing-at-the-same-time
# a, b = T.dmatrices('a', 'b')
# diff = a - b
# abs_diff = abs(diff)
# diff_squared = diff**2
# f = theano.function([a, b], [diff, abs_diff, diff_squared])
# print f([[1, 1], [1, 1]], [[0, 1], [2, 3]])


# # http://deeplearning.net/software/theano/tutorial/examples.html#copying-functions
# state = theano.shared(0)
# inc = T.iscalar('inc')
# accumulator = theano.function([inc], state, updates=[(state, state+inc)], on_unused_input='ignore')
# accumulator(10)
# print(state.get_value())
# new_state = theano.shared(0)
# new_accumulator = accumulator.copy(swap={state:new_state})
# new_accumulator(100)
# print(new_state.get_value())




###### KERAS EXAMPLES
# https://keras.io/#getting-started-30-seconds-to-keras

from keras.models import Sequential
from keras.layers import Dense, Activation

model = Sequential()

model.add(Dense(output_dim=64, input_dim=100))
model.add(Activation("relu"))
model.add(Dense(output_dim=10))
model.add(Activation("softmax"))

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

