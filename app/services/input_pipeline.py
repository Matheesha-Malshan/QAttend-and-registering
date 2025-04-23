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
    
    def normalize_data(self,data):
        return tf.reshape(tf.linalg.l2_normalize(data,axis=1),shape=(-1,1))
    
    def distance(self,embeddings,new_embedding):
        return tf.norm(embeddings-new_embedding,axis=1)
