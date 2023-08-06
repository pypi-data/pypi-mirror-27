from .Layer import *
from .Initializer import *



class Batchnorm(Layer):
    def __init__(self, 
                 obj, 
                 ep=1e-8, 
                 init_kinds="xavier",
                 random_kinds="normal",
                 random_params=(0, 1),
                 act="linear",
                 is_train=True,
                 name=None):
        super().__init__(obj, name=name)
        self.gamma  = theano.shared(Initializer(name=init_kinds,
                                                 random_kinds=random_kinds,
                                                 random_params=random_params,
                                                 shape=self.n_in,                                             ).out.astype(dtype=theano.config.floatX), borrow=True)
        self.beta  = theano.shared(Initializer(name=init_kinds,
                                               random_kinds=random_kinds,
                                               random_params=random_params,
                                               shape=self.n_in,                                             ).out.astype(dtype=theano.config.floatX), borrow=True)
        #self.beta = beta
        self.ep = ep
        self.n_out = self.n_in
        if is_train:
            self.params = {self.name + "_gamma":self.gamma, self.name + "_beta":self.beta}

    def out(self):
        obj = self.obj
        gamma, beta, ep = self.gamma, self.beta, self.ep
        x = obj.out
        n_batch = obj.n_batch
        mu = x.sum() / n_batch
        sigma2 = ((x - mu)**2) / n_batch
        
        x_hat = (x - mu) / T.sqrt(sigma2 + ep)
        #obj.out = T.sqrt(T.var(x)) * x_hat + T.mean(x)
        obj.out = gamma * x_hat + beta
        
        return obj
    
    def gen_name(self):
        if self.name is None:
            self.name = "Batchnorm_{}".format(self.obj.layer_info.layer_num)
            
class Reshape(Layer):
    def __init__(self, obj, n_out, name=None):
        super().__init__(obj, name=name)
        self.n_out   = n_out

    def out(self):
        obj = self.obj
        obj.out = obj.out.reshape([-1, *self.n_out])
        return obj
    
    def gen_name(self):
        if self.name is None:
            self.name = "Reshape_{}".format(self.obj.layer_info.layer_num)

class Flatten(Layer):
    def __init__(self, obj, name=None):
        super().__init__(obj, name=name)

    def out(self):
        obj = self.obj
        self.n_out = (np.array(self.n_in).prod(),)
        obj.out = obj.out.reshape((-1, *self.n_out))
        return obj

    def gen_name(self):
        if self.name is None:
            self.name = "Flatten_{}".format(self.obj.layer_info.layer_num)
