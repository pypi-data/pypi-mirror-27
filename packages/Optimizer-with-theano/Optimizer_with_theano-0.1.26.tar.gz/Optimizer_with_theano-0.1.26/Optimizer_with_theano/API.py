import Optimizer_with_theano as op
import numpy as np
import inspect
import PIL.Image as I
import theano
import theano.tensor as T
import os
import pylab 
import requests

class Encoder_decoder:
    def __init__(self, 
                 encoder=None, 
                 decoder=None,
                 enc_dec=None):
        self.encoder = encoder
        self.decoder = decoder
        self.enc_dec = enc_dec
    
    def build(self):
        #self.build_encoder()
        self.build_decoder()
        #self.build_enc_dec()
        
    def build_encoder(self):
        if self.decoder is None:
            layerlst = self.enc_dec.layer_info.layerlst
            dec_i = 0
            n_layer = len(layerlst)
            for i, layer in enumerate(layerlst):
                if layer.name == name_of_decoder:
                    dec_i = i
                    break
            input_shape = (1,) + layerlst[dec_i].n_in
            output_shape = (1,) + layerlst[-1].n_out
            o = op.optimizer()
            o = o.set_data(input_shape, output_shape, test_size=0)
            o.layer_info.layerlst += layerlst[dec_i:n_layer]
            self.decoder = o.layer_info.update_layers()
    
    def build_decoder(self, name_of_decoder="decoder"):
        if self.decoder is None:
            if self.encoder is None:
                layerlst = self.enc_dec.layer_info.layerlst
                dec_i = 0
                n_layer = len(layerlst)
                for i, layer in enumerate(layerlst):
                    if layer.name == name_of_decoder:
                        dec_i = i
                        break
                input_shape = (1,) + layerlst[dec_i].n_in
                output_shape = (1,) + layerlst[-1].n_out
                o = op.optimizer()
                o = o.set_data(input_shape, output_shape, test_size=0)
                o = o.set_layers(layerlst[dec_i:n_layer])
                self.decoder = o
    #def 

class neural_style:
    def __init__(self, 
                 content_img_path=None, 
                 style_img_path=None,
                 out_img_path=None,
                 img_shape=(400,400)
                ):
        
        root_dir = "{}".format("/".join(inspect.getfile(op.optimizer).split("/")[:-1]))
        self.content_img_path       = "{}/sample/parakeet.jpg".format(root_dir)    if not content_img_path else content_img_path
        self.style_img_path         = "{}/sample/psychedelic.jpg".format(root_dir) if not style_img_path else style_img_path
        self.out_img_path           = "./" if not out_img_path else out_img_path
        self.img_shape              = img_shape
    
    def build(self, 
              layer_for_content=None,
              layers_for_style=None,
              content_weight=0.0025,
              style_weight=1,
              total_variation_weight=1,
              ):
        
        img = I.open(self.content_img_path)
        img = np.array(img.resize(self.img_shape))\
              .transpose(2,0,1).astype(np.float32)
            
        img[2] -= 103.939
        img[1] -= 116.779
        img[0] -= 123.68
        
        style = I.open(self.style_img_path)
        style = np.array(style.resize(self.img_shape)).transpose(2,0,1).astype(np.float32)
        style[2] -= 103.939
        style[1] -= 116.779
        style[0] -= 123.68
        
        comb = theano.shared(img.astype(np.float32))
        data = theano.tensor.concatenate([img[None,], style[None,], comb[None,...]])
        
        o = op.optimizer(n_batch=3)
        o.set_data(data, np.ones((3,1)), test_size=0, is_shuffle=False)
        o = Vgg19().build(o, is_train=False)
        
        # define loss functions
        loss = 0
        
        # content loss    
        layer_name = "conv5_2" if layer_for_content is None else layer_for_content
        features = o.layer_info.get_out(layer_name)
        M = features.shape[2] * features.shape[3]# * arr.shape[1]#img_row * img_col
        N = features.shape[1]# * arr.shape[1]#img_row * img_col
        base_image_features  = style
        combination_features = comb
        base_image_features  = features[0] 
        combination_features = features[2]
        loss += content_weight *\
                ((base_image_features - combination_features)**2).sum() / (M * N)
        
        # style loss
        if layers_for_style is None: 
            feature_layers = ['conv1_1', 'conv2_1',
                              'conv3_1', 'conv4_1',
                              'conv5_1']
        else:
            feature_layers = layers_for_style
        
        img_row, img_col = self.img_shape
        for layer_name in feature_layers:
            arr = o.layer_info.get_out(layer_name)
            arr = arr.reshape(list(arr.shape[:2]) + [-1])
            s = arr[1]
            S = s.dot(s.T) # so-called gram matrix.
            c = arr[2]
            C = c.dot(c.T) # so-called gram matrix.
            M = arr.shape[2]# * arr.shape[1]#img_row * img_col
            N = arr.shape[1]# * arr.shape[1]#img_row * img_col
            sl = ((S - C) ** 2).sum() / (4 * (N ** 2) * (M ** 2))
            loss += (style_weight / len(feature_layers)) * sl
        
        # total variation loss
        a = comb[ :, :img_row - 1, :img_col-1] - comb[ :, 1:, :img_col -1]
        b = comb[ :, :img_row - 1, :img_col-1] - comb[ :, :img_row-1, 1:]
        loss += total_variation_weight * ((a**2 + b**2) ** 1.25).sum()
        
        o = o.loss_self(loss)
            
        self.obj = o
        self.result_img = comb

    def generate_image(self,
                       dump_per_train=10,
                       n_train=1000,
                       n_view=10,
                       learning_rate=3,
                       img_name="img",
                       is_view=True):
    
        self.obj = self.obj.opt_Adam(learning_rate, input_grads=[self.result_img])\
                       .compile(is_fast=True, is_random=False)
        cnt = 0
        img_lst = []
        for i in range(n_train):
            loss, _ = self.obj.train_loss_and_acc(0)
            line = "Iter.: %i, loss: %.4e. " %(i, loss)
            if not i % dump_per_train:
                file_name = "{}_{}.jpg".format(img_name, cnt)
                print(file_name + " is dumped.")
                result_img = np.array(self.result_img.eval())
                result_img[2] += 103.939
                result_img[1] += 116.779
                result_img[0] += 123.68
                result_img = result_img.clip(0,255)\
                                       .transpose(1,2,0)\
                                       .astype(np.uint8)
                result = I.fromarray(result_img)
                result.save(self.out_img_path + "/" + file_name) 
                img_lst += [result_img]
                cnt += 1
                
            if not i % n_view:
                print(line)
        
        
        if is_view:
            pylab.figure(figsize=(20,20))
            n_img = len(img_lst)
            for i, img in enumerate(img_lst):
                pylab.subplot(2, n_img//2 + n_img%2, i+1) 
                pylab.axis("off")
                pylab.imshow(img)
            pylab.show()
            

def download_param(url, dump_path):
  res = requests.get(url)
  if res.status_code == 200:
        #image_name = url.split("?")[0].split("/")[-1]
        with open(dump_path, 'wb') as file:
            file.write(res.content)    
            print("File has downloaded at {}".format(dump_path))
  
            
class Vgg19:
    def __init__(self, vgg19_npy_path=None):
        if vgg19_npy_path is None:
            dir_path = "{}/param_dir/".format("/".join(inspect.getfile(op.optimizer).split("/")[:-1]))
            vgg19_npy_path = dir_path + "vgg19.npy"
            if not os.path.exists(vgg19_npy_path):
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                download_param("https://www.dropbox.com/s/xnxtad79ogf7v0a/vgg19.npy?dl=1", vgg19_npy_path)
        self.data_dict = np.load(vgg19_npy_path, encoding="latin1").item()
        
    def build(self, obj, is_train=False):
        # Block 1
        obj = obj.conv2d(kshape=(64,3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv1_1"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv1_1"][1], 
                         is_train=is_train,
                         name="conv1_1")
        obj = obj.conv2d(kshape=(64,3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv1_2"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv1_2"][1], 
                         is_train=is_train,
                         name="conv1_2")
        obj = obj.pool(name="block1_pool")
        
        # Block 2
        obj = obj.conv2d(kshape=(128,3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv2_1"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv2_1"][1], 
                         is_train=is_train,
                         name="conv2_1")
        obj = obj.conv2d(kshape=(128,3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv2_2"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv2_2"][1], 
                         is_train=is_train,
                         name="conv2_2")
        obj = obj.pool(name="block2_pool")
        
        # Block 3
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv3_1"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv3_1"][1], 
                         is_train=is_train,
                         name="conv3_1")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv3_2"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv3_2"][1], 
                         is_train=is_train,
                         name="conv3_2")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv3_3"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv3_3"][1], 
                         is_train=is_train,
                         name="conv3_3")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv3_4"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv3_4"][1], 
                         is_train=is_train,
                         name="conv3_4")
        obj = obj.pool(name="block3_pool")
            
        # Block 4
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv4_1"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv4_1"][1], 
                         is_train=is_train,
                         name="conv4_1")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv4_2"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv4_2"][1], 
                         is_train=is_train,
                         name="conv4_2")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv4_3"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv4_3"][1], 
                         is_train=is_train,
                         name="conv4_3")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv4_4"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv4_4"][1], 
                         is_train=is_train,
                         name="conv4_4")
        obj = obj.pool(name="block4_pool")
        
        # Block 5
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv5_1"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv5_1"][1], 
                         is_train=is_train,
                         name="conv5_1")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv5_2"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv5_2"][1], 
                         is_train=is_train,
                         name="conv5_2")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv5_3"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv5_3"][1], 
                         is_train=is_train,
                         name="conv5_3")
        obj = obj.conv2d(kshape=(512, 3, 3), 
                         mode="same", 
                         act="relu", 
                         theta=self.data_dict["conv5_4"][0].transpose(3,2,0,1), 
                         b=self.data_dict["conv5_4"][1], 
                         is_train=is_train,
                         name="conv5_4")
        obj = obj.pool(name="block5_pool")
        return obj
        
            