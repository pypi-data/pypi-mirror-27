from .Initializer import Initializer
from .Layer import *
from numpy import *


class Capsule_layer(Layer):
    def __init__(self, 
                 obj, 
                 n_out, 
                 init_kinds="xavier", 
                 random_kinds="normal", 
                 random_params=(0, 1),
                 activation="linear",
                 is_train=True,
                 func_to_variable=None,
                 name=None,
                 num_vector1=8,
                 num_vector2=16,
                 num_channel=8,
                 num_routing=9,
                 ksize=(9,9)
                ):
        super().__init__(obj, activation=activation, name=name)
        
        self.num_capsule = num_channel * array(ksize).prod()
        self.num_vector1 = num_vector1
        self.num_vector2 = num_vector2
        self.num_routing = num_routing
        self.num_channel = num_channel
        self.ksize       = ksize
        
        self.n_out   = (n_out,)
        self.theta   = theano.shared(Initializer(name=init_kinds,
                                                 n_in=self.n_in,
                                                 n_out=(n_out, self.num_vector2, self.num_vector1),
                                                 random_kinds=random_kinds,
                                                 random_params=random_params,
                                                 shape=(n_out, self.num_vector2, self.num_vector1),
                                                 ).out.astype(dtype=theano.config.floatX), borrow=True)
        
        self.b       = theano.shared(Initializer(name=init_kinds,
                                                 n_in=self.n_in,
                                                 n_out=(self.num_capsule, n_out),
                                                 random_kinds=random_kinds,
                                                 random_params=random_params,
                                                 shape=(self.num_capsule, n_out),
                                                 ).out.astype(dtype=theano.config.floatX), borrow=True)
        
        self.func_to_variable = func_to_variable
        
        self.gen_name()
        

        if is_train:
            self.params = {self.name + "_theta":self.theta, self.name + "_b":self.b}

    def out(self):
        obj = self.obj
        obj = obj.conv2d((self.num_vector1 * self.num_channel, *self.ksize),mode="valid")
        obj.residual = residual = self.num_channel * obj.out.shape[-1] * obj.out.shape[-1] #.astype(int64)
        obj = obj.reshape((self.num_vector1, residual))#.transpose((1,2,0))
        ##self.obj = obj
        obj.u = u = T.batched_dot(self.theta, obj.out)
        ##
        obj.c = c = T.nnet.softmax(self.b.T).T
        ##
        #s = T.dot(u, c)
        #
        #norm_s = s.norm(L=2)
        #v = norm_s / (1 + norm_s) * s / norm_s
        #
        #obj.out = v
        
        
        
               
        #if len(obj.n_in) == 1:
        #    def _step(seq, prior):
        #        y = tout[..., seq:seq+1].dot(self.theta) + self.b + prior.dot(self.theta2)
        #        return Activation(self.activation)(y)
        #    i = theano.shared(self.n_iter)
        #    
        #    arr = T.zeros_like(tout[..., 0:1]).dot(self.theta)
        #    self.obj.arr = arr
        #    result, updates = theano.scan(fn=_step,
        #                      sequences=T.arange(i),
        #                      outputs_info=arr,
        #                      non_sequences=None,
        #                      n_steps=None)
        #    self.obj.result = result
        #else:
        #    def _step(seq, prior):
        #        y = tout[..., seq].dot(self.theta) + self.b + prior.dot(self.theta2)
        #        return Activation(self.activation)(y)
        #    i = theano.shared(self.n_iter)
        #    
        #    arr = T.zeros_like(tout[..., 0]).dot(self.theta)
        #    self.obj.arr = arr
        #    result, updates = theano.scan(fn=_step,
        #                      sequences=T.arange(i),
        #                      outputs_info=arr,
        #                      non_sequences=None,
        #                      n_steps=None)
        #    self.obj.result = result
        
        
        
        

    
    def gen_name(self):
        if self.name is None:
            self.name = "CapsNet_{}".format(self.obj.layer_info.layer_num)

           