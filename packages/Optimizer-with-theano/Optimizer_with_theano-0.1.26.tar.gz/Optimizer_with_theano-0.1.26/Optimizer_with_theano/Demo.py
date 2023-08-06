from .Optimizer import optimizer

def MNIST(is_cnn=False):
    print("MNIST demo")
    if is_cnn:
        print("CNN version.")
        print("""
import Optimizer_with_theano as op
o = op.optimizer(128)
o = o.set_datasets()
o = o.reshape((1,28,28))
o = o.conv_and_pool(64,3,3, "same", act="relu")
o = o.conv_and_pool(32,3,3, "same", act="relu")
o = o.flatten().dense(10)
o = o.softmax().loss_cross_entropy()
o = o.opt_Adam(0.001).compile()
o = o.optimize(10, 1)
        """)
        o = optimizer(128)
        o = o.set_datasets()
        o = o.reshape((1, 28, 28))
        o = o.conv_and_pool(64, 3, 3, "same", act="relu")
        o = o.conv_and_pool(32, 3, 3, "same", act="relu")
        o = o.flatten().dense(10)
        o = o.softmax().loss_cross_entropy()
        o = o.opt_Adam(0.001).compile()
        o = o.optimize(10, 1)
    else:
        print("Fully connected version.")
        print("""
import Optimizer_with_theano as op
o = op.optimizer(128)
o = o.set_datasets()
o = o.dense(400, act="relu")
o = o.dense(30,  act="relu")
o = o.dense(20,  act="relu")
o = o.dense(10)
o = o.softmax().loss_cross_entropy()
o = o.opt_Adam(0.001).compile()
o = o.optimize(100, 10)
        """)
        o = optimizer(128)
        o = o.set_datasets()
        o = o.dense(400, act="relu")
        o = o.dense(30,  act="relu")
        o = o.dense(20,  act="relu")
        o = o.dense(10)
        o = o.softmax().loss_cross_entropy()
        o = o.opt_Adam(0.001).compile()
        o = o.optimize(100, 10)
    return o
