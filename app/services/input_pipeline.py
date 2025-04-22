import tensorflow as tf

class Input_pipe:
    def __init__(self):
        #self.data=data
        #self.labels=labels
        pass

    def conver_to_tensors(self,data):

        tensors=tf.convert_to_tensor(data,tf.float32)/255
        tensors=tf.transpose(tensors,perm=[2,0,1])
        tensors=(tensors-0.5)/0.5
        tensors=tf.expand_dims(tensors,axis=0)
        return tensors.numpy()
    
    def normalisze_data(self):
        nor_data,lables=self.data/255,self.labels
        return nor_data,lables
    
    def input_(self):
        nor_data=nor_data.map(self.normalize_data(self.data,self.labels))
