import os
import numpy as np
import tensorflow as tf
import CSFunctions
from tensorflow.contrib import rnn            

class RNN:
     
     def __init__(self,training_data=[], training_labels=[], validation_data=[], validation_labels=[], network_save_filename=[], minimum_epoch=5, maximum_epoch=10, n_hidden=[100,100], n_classes=2, cell_type='LSTMP', configuration='B', attention_number=2, dropout=0.75, init_method='zero', truncated=100, optimizer='Adam', learning_rate=0.003 ,save_location=[],output_act='sigmoid',snippet_length=100,aug_prob=0,hop_size=512, cost_type='CE',num_frames_either_side=0,batch_size=1000,input_feature_size=84):         
         self.features=training_data
         self.targ=training_labels
         self.val=validation_data
         self.val_targ=validation_labels
         self.filename=network_save_filename
         self.n_hidden=n_hidden
         self.n_layers=len(self.n_hidden)
         self.cell_type=cell_type
         self.dropout=dropout
         self.configuration=configuration
         self.init_method=init_method
         self.truncated=truncated
         self.optimizer=optimizer
         self.learning_rate=learning_rate
         self.n_classes=n_classes
         self.minimum_epoch=minimum_epoch
         self.maximum_epoch=maximum_epoch
         self.num_batch=int(len(self.features)/batch_size)
         self.val_num_batch=int(len(self.val)/batch_size)
         self.batch_size=batch_size
         self.attention_number=attention_number
         self.cost_type=cost_type
         self.nfes=num_frames_either_side
         self.input_feature_size=input_feature_size
         self.batch=np.zeros((self.batch_size,self.input_feature_size*((2*self.nfes)+1)))
         self.batch_targ=np.zeros((self.batch_size,self.n_classes))
         self.save_location=save_location
         self.output_act=output_act
         self.snippet_length=snippet_length
         self.aug_prob=aug_prob
         self.hop_size=hop_size
         self.num_seqs=int(self.batch_size/self.snippet_length)
         
         

     def cell_create(self,scope_name):
         with tf.variable_scope(scope_name):
             if int(scope_name)==1:
                 if self.cell_type == 'tanh':
                     cells = rnn.MultiRNNCell([rnn.BasicRNNCell(self.n_hidden[int(scope_name)-1]) for i in range(1)], state_is_tuple=True)
                 elif self.cell_type == 'LSTM': 
                     cells = rnn.MultiRNNCell([rnn.BasicLSTMCell(self.n_hidden[int(scope_name)-1]) for i in range(1)], state_is_tuple=True)
                 elif self.cell_type == 'GRU':
                     cells = rnn.MultiRNNCell([rnn.GRUCell(self.n_hidden[int(scope_name)-1]) for i in range(1)], state_is_tuple=True)
                 elif self.cell_type == 'LSTMP':
                     cells = rnn.MultiRNNCell([rnn.LSTMCell(self.n_hidden[int(scope_name)-1]) for i in range(1)], state_is_tuple=True)
                 cells = rnn.DropoutWrapper(cells, input_keep_prob=self.dropout_ph,output_keep_prob=self.dropout_ph)
             else:
                 if self.cell_type == 'tanh':
                     cells = rnn.MultiRNNCell([rnn.BasicRNNCell(self.n_hidden[int(scope_name)-1+i]) for i in range(self.n_layers-1)], state_is_tuple=True)
                 elif self.cell_type == 'LSTM': 
                     cells = rnn.MultiRNNCell([rnn.BasicLSTMCell(self.n_hidden[int(scope_name)-1+i]) for i in range(self.n_layers-1)], state_is_tuple=True)
                 elif self.cell_type == 'GRU':
                     cells = rnn.MultiRNNCell([rnn.GRUCell(self.n_hidden[int(scope_name)-1+i]) for i in range(self.n_layers-1)], state_is_tuple=True)
                 elif self.cell_type == 'LSTMP':
                     cells = rnn.MultiRNNCell([rnn.LSTMCell(self.n_hidden[int(scope_name)-1+i]) for i in range(self.n_layers-1)], state_is_tuple=True)
                 cells = rnn.DropoutWrapper(cells, input_keep_prob=self.dropout_ph,output_keep_prob=self.dropout_ph)                 
         return cells
     
     def weight_bias_init(self):
               
         if self.init_method=='zero':
            self.biases = tf.Variable(tf.zeros([self.n_classes]))           
         elif self.init_method=='norm':
               self.biases = tf.Variable(tf.random_normal([self.n_classes]))           
         if self.configuration =='B':
             if self.init_method=='zero':  
                 self.weights =tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)]*2, self.n_classes]))
             elif self.init_method=='norm':
                   self.weights = { '1': tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes])),'2': tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes]))} 
         if self.configuration =='R':
             if self.init_method=='zero':  
                 self.weights = tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes]))     
             elif self.init_method=='norm':
                   self.weights = tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes]))
                   
     def cell_create_norm(self):
         if self.cell_type == 'tanh':
             cells = rnn.MultiRNNCell([rnn.BasicRNNCell(self.n_hidden[i]) for i in range(self.n_layers)], state_is_tuple=True)
         elif self.cell_type == 'LSTM': 
             cells = rnn.MultiRNNCell([rnn.BasicLSTMCell(self.n_hidden[i]) for i in range(self.n_layers)], state_is_tuple=True)
         elif self.cell_type == 'GRU':
             cells = rnn.MultiRNNCell([rnn.GRUCell(self.n_hidden[i]) for i in range(self.n_layers)], state_is_tuple=True)
         elif self.cell_type == 'LSTMP':
             cells = rnn.MultiRNNCell([rnn.LSTMCell(self.n_hidden[i]) for i in range(self.n_layers)], state_is_tuple=True)
         cells = rnn.DropoutWrapper(cells, input_keep_prob=self.dropout_ph,output_keep_prob=self.dropout_ph) 
         return cells
           
     def attention_weight_init(self,num):
         if num==0:
             self.attention_weights=[tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)]*4,self.n_hidden[(len(self.n_hidden)-1)]*2]))]
             self.sm_attention_weights=[tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)]*2,self.n_hidden[(len(self.n_hidden)-1)]*2]))]
         if num>0:
             self.attention_weights.append(tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)]*4,self.n_hidden[(len(self.n_hidden)-1)]*2])))
             self.sm_attention_weights.append(tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)]*2,self.n_hidden[(len(self.n_hidden)-1)]*2])))
             
     def create(self):
       
       tf.reset_default_graph()
       self.x_ph = tf.placeholder("float32", [None, None, self.batch.shape[1]])
       self.y_ph = tf.placeholder("float32", [None, None, self.batch_targ.shape[1]]) 
       self.seq=tf.placeholder("int32")
       self.num_seqs=tf.placeholder("int32")
       self.seq_len=tf.placeholder("int32")
       self.dropout_ph = tf.placeholder("float32")
       if self.attention_number==0:
           self.fw_cell=self.cell_create_norm()
           self.weight_bias_init()
       elif self.attention_number>0:
           self.fw_cell=self.cell_create('1')
           self.fw_cell2=self.cell_create('2')
           self.weight_bias_init()
       else:
           print('negative attention numbers not allowd')
       if self.configuration=='R':
           if self.attention_number>0:
               print('no attention for R models')
           else:
               self.outputs, self.states= tf.nn.dynamic_rnn(self.fw_cell, self.x_ph,
                                                 sequence_length=self.seq,dtype=tf.float32)
               self.presoft=tf.matmul(self.outputs[0][0], self.weights) + self.biases
       elif self.configuration=='B':           
           if self.attention_number==0:
               self.bw_cell=self.cell_create_norm()
               self.outputs, self.states= tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, self.x_ph,
                                         sequence_length=self.seq,dtype=tf.float32)


               self.presoft=tf.map_fn(lambda x:tf.matmul(x,self.weights)+self.biases,tf.concat((self.outputs[0],self.outputs[1]),2))
               
           elif self.attention_number>0:
               self.bw_cell=self.cell_create('1')
               self.bw_cell2=self.cell_create('2') 
               with tf.variable_scope('1'):

                   self.outputs, self.states= tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, self.x_ph,
                                                     sequence_length=self.seq,dtype=tf.float32)
                                                  
               self.first_out=tf.concat((self.outputs[0],self.outputs[1]),2)
               with tf.variable_scope('2'):
                   self.outputs2, self.states2= tf.nn.bidirectional_dynamic_rnn(self.fw_cell2, self.bw_cell2, self.first_out,
                                                     sequence_length=self.seq,dtype=tf.float32)
               self.second_out=tf.concat((self.outputs2[0],self.outputs2[1]),2)

               for i in range((self.attention_number*2)+1):
                   self.attention_weight_init(i)
               
                
               self.zero_pad_second_out=tf.map_fn(lambda x:tf.pad(tf.squeeze(x),[[self.attention_number,self.attention_number],[0,0]]),self.second_out)
               self.first_out_reshape=tf.reshape(self.first_out,[-1,self.n_hidden[self.n_layers-1]*2])
               self.zero_pad_second_out_reshape=[]
               self.attention_m=[]
               for j in range((self.attention_number*2)+1):
                   self.zero_pad_second_out_reshape.append(tf.reshape(tf.slice(self.zero_pad_second_out,[0,j,0],[self.num_seqs,self.seq_len,self.n_hidden[self.n_layers-1]*2]),[-1,self.n_hidden[self.n_layers-1]*2]))
                   self.attention_m.append(tf.tanh(tf.matmul(tf.concat((self.zero_pad_second_out_reshape[j],self.first_out_reshape),1),self.attention_weights[j])))
               self.attention_s=tf.nn.softmax(tf.stack([tf.matmul(self.attention_m[j],self.sm_attention_weights[j]) for j in range(self.attention_number*2+1)]),0)
               self.attention_z=tf.reduce_sum([self.attention_s[j]*self.zero_pad_second_out_reshape[j] for j in range(self.attention_number*2+1)],0)
               self.attention_z_reshape=tf.reshape(self.attention_z,[self.num_seqs,self.seq_len,self.n_hidden[self.n_layers-1]*2])
               self.presoft=tf.map_fn(lambda x:tf.matmul(x,self.weights)+self.biases,self.attention_z_reshape)
#              
               
       if  self.output_act=='softmax':   
           self.pred=tf.nn.softmax(self.presoft)
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
               
       elif self.output_act=='sigmoid':
           self.pred=tf.nn.sigmoid(self.presoft)
           
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='NewHybridCE2':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='NewHybridCE4':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2)  
           elif self.cost_type=='HybridCEMS2':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='HybridCEMS4':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/4.,self.seq_len-2)     
           elif self.cost_type=='HybridCE2-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,1.0)                
           elif self.cost_type=='HybridCE4-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,1.0) 
           elif self.cost_type=='HybridCE2-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.9)                
           elif self.cost_type=='HybridCE4-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.9)
           elif self.cost_type=='HybridCE2-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.8)                
           elif self.cost_type=='HybridCE4-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.8)
           elif self.cost_type=='HybridCE2-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.7)                
           elif self.cost_type=='HybridCE4-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.7)  
           elif self.cost_type=='HybridCE2-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.6)                
           elif self.cost_type=='HybridCE4-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.6)
           elif self.cost_type=='HybridCE2-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.5)                
           elif self.cost_type=='HybridCE4-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.5) 
               
       if self.optimizer == 'GD':
             self.optimize = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
       elif self.optimizer == 'Adam':
             self.optimize = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
       elif self.optimizer == 'RMS':
             self.optimize = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.cost) 
#       self.correct_pred = tf.equal(tf.argmax(self.pred,1), tf.argmax(self.y_ph,1))
#       self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))
       self.init = tf.global_variables_initializer()
       self.saver = tf.train.Saver()
       self.saver_var = tf.train.Saver(tf.trainable_variables())
       if self.save_location==[]:
           self.save_location=os.getcwd()
                             
        
     def train(self):
        
       self.iteration=0
       self.epoch=0
       self.prev_val_loss=100
       self.val_loss=99
       config=tf.ConfigProto(intra_op_parallelism_threads=20)
       with tf.Session(config=config) as sess:
         sess.run(self.init)
         if self.nfes==0:
             while self.epoch < self.minimum_epoch or self.prev_val_loss > self.val_loss:
                 for i in xrange(self.num_batch):

                     sess.run(self.optimize, feed_dict={self.x_ph: np.reshape(np.expand_dims(self.features[i*self.batch_size:(i+1)*self.batch_size,:],0),[-1,self.snippet_length,self.input_feature_size]), self.y_ph: np.reshape(np.expand_dims(self.targ[i*self.batch_size:(i+1)*self.batch_size,:],0),[-1,self.snippet_length,self.n_classes]),self.dropout_ph:self.dropout, self.seq:np.ones(int(self.batch_size/self.snippet_length))*self.snippet_length, self.num_seqs:int(self.batch_size/self.snippet_length), self.seq_len:self.snippet_length})
                          
                 print("Epoch " + str(self.epoch))
                 self.epoch+=1  
                 if self.epoch > self.minimum_epoch:
                     self.loss_val=[]
                     for i in range(self.val_num_batch):
                         self.loss_val.append(sess.run(self.cost, feed_dict={self.x_ph: np.expand_dims(self.val[i*self.batch_size:(i+1)*self.batch_size,:],0), self.y_ph: np.expand_dims(self.val_targ[i*self.batch_size:(i+1)*self.batch_size,:],0),self.dropout_ph:1,self.seq:[self.batch_size],self.num_seqs:1, self.seq_len:self.batch_size}))
                         
                     self.prev_val_loss=self.val_loss
                     self.val_loss=np.mean(np.array(self.loss_val))              
                     print("Val Minibatch Loss " + "{:.6f}".format(self.val_loss))
                 if self.epoch==self.maximum_epoch:
                     break
             print("Optimization Finished!")
             self.saver.save(sess, self.save_location+'/'+self.filename)

         
     def implement(self,data):
             self.data=data
             self.test_out=[]
             with tf.Session() as sess:
                     self.saver.restore(sess, self.save_location+'/'+self.filename)
                     for i in range(len(self.data)):
                             self.test_out.append(sess.run(self.pred, feed_dict={self.x_ph: np.expand_dims(self.data[i],0),self.dropout_ph:1,self.seq:[len(self.data[i])],self.num_seqs:1, self.seq_len:len(self.data[i])})[0]) 

             return self.test_out
        

class CRNN(RNN):
#     
     def __init__(self,training_data=[], training_labels=[], validation_data=[], validation_labels=[], network_save_filename=[], minimum_epoch=5, maximum_epoch=10, n_hidden=[100,100], n_classes=2, cell_type='LSTMP', configuration='B', attention_number=2, dropout=0.75, init_method='zero', truncated=100, optimizer='Adam', learning_rate=0.003 ,save_location=[],output_act='sigmoid',snippet_length=100,aug_prob=0,hop_size=512, cost_type='CE',num_frames_either_side=0,batch_size=1000,input_feature_size=84*11,conv_filter_shapes=[[3,3,1,32],[3,3,32,64]], conv_strides=[[1,1,1,1],[1,1,1,1]], pool_window_sizes=[[1,1,2,1],[1,1,2,1]],pad='SAME'):         
         self.features=training_data
         self.targ=training_labels
         self.val=validation_data
         self.val_targ=validation_labels
         self.filename=network_save_filename
         self.n_hidden=n_hidden
         self.n_layers=len(self.n_hidden)
         self.cell_type=cell_type
         self.dropout=dropout
         self.configuration=configuration
         self.init_method=init_method
         self.truncated=truncated
         self.optimizer=optimizer
         self.learning_rate=learning_rate
         self.n_classes=n_classes
         self.minimum_epoch=minimum_epoch
         self.maximum_epoch=maximum_epoch
         self.num_batch=int(len(self.features)/batch_size)
         self.val_num_batch=int(len(self.val)/batch_size)
         self.batch_size=batch_size
         self.attention_number=attention_number
         self.cost_type=cost_type
         self.nfes=num_frames_either_side
         self.input_feature_size=input_feature_size
         self.batch=np.zeros((self.batch_size,self.input_feature_size))
         self.batch_targ=np.zeros((self.batch_size,self.n_classes))
         self.save_location=save_location
         self.output_act=output_act
         self.snippet_length=snippet_length
         self.aug_prob=aug_prob
         self.hop_size=hop_size
         self.num_seqs=int(self.batch_size/self.snippet_length)
         self.conv_filter_shapes=conv_filter_shapes
         self.conv_strides=conv_strides
         self.pool_window_sizes=pool_window_sizes
         self.pool_strides=self.pool_window_sizes
         self.conv_layer_out=[]
         self.fc_layer_out=[]
         self.w_fc=[]
         self.b_fc=[]
         self.h_fc=[]
         self.w_conv=[]
         self.b_conv=[]
         self.h_conv=[]
         self.h_pool=[]
         self.h_drop_batch=[]
         self.pad=pad
        
             
     def conv2d(self,data, weights, conv_strides, pad):
         return tf.nn.conv2d(data, weights, strides=conv_strides, padding=pad)
     
     def max_pool(self,data, max_pool_window, max_strides, pad):
        return tf.nn.max_pool(data, ksize=max_pool_window,
                            strides=max_strides, padding=pad)
        
     def weight_init(self,weight_shape):
        weight=tf.Variable(tf.truncated_normal(weight_shape))    
        return weight
        
     def bias_init(self,bias_shape,):   
        bias=tf.Variable(tf.constant(0.1, shape=bias_shape))
        return bias
    
     def batch_dropout(self,data):
        batch_mean, batch_var=tf.nn.moments(data,[0])
        scale=tf.Variable(tf.ones([self.num_seqs*self.seq_len,data.get_shape()[1],data.get_shape()[2],data.get_shape()[3]]))
        beta=tf.Variable(tf.zeros([self.num_seqs*self.seq_len,data.get_shape()[1],data.get_shape()[2],data.get_shape()[3]]))
        h_poolb=tf.nn.batch_normalization(data,batch_mean,batch_var,beta,scale,1e-3)
        return tf.nn.dropout(h_poolb, self.dropout_ph)
        
     def conv_2dlayer(self,layer_num):
        self.w_conv.append(self.weight_init(self.conv_filter_shapes[layer_num]))
        self.b_conv.append(self.bias_init([self.conv_filter_shapes[layer_num][3]]))
        self.h_conv.append(tf.nn.relu(self.conv2d(self.conv_layer_out[layer_num], self.w_conv[layer_num], self.conv_strides[layer_num], self.pad) + self.b_conv[layer_num]))
        self.h_pool.append(self.max_pool(self.h_conv[layer_num],self.pool_window_sizes[layer_num],self.pool_strides[layer_num],self.pad))       
#        self.conv_layer_out.append(self.batch_dropout(self.h_pool[layer_num]))  
        self.conv_layer_out.append(self.h_pool[layer_num])  

     def reshape_layer(self):
            convout=self.conv_layer_out[len(self.conv_layer_out)-1]
            self.fc_layer_out=tf.reshape(convout, [self.num_seqs,self.seq_len,1280])
            
     def create(self):
       
       tf.reset_default_graph()
       self.x_ph = tf.placeholder("float32", [None, None, self.batch.shape[1]])
       self.y_ph = tf.placeholder("float32", [None, None, self.batch_targ.shape[1]]) 
       self.seq=tf.placeholder("int32")
       self.num_seqs=tf.placeholder("int32")
       self.seq_len=tf.placeholder("int32")
       self.dropout_ph = tf.placeholder("float32")
       
       self.conv_layer_out.append(tf.expand_dims(tf.reshape(self.x_ph,[-1,11,self.input_feature_size/11]),3))
       for i in xrange(len(self.conv_filter_shapes)):
            self.conv_2dlayer(i)
       self.reshape_layer()
       if self.attention_number==0:
           self.fw_cell=self.cell_create_norm()
           self.weight_bias_init()
       elif self.attention_number>0:
           self.fw_cell=self.cell_create('1')
           self.fw_cell2=self.cell_create('2')
           self.weight_bias_init()
       else:
           print('negative attention numbers not allowd')
       if self.configuration=='R':
           print('no attention for R models yet')
           self.outputs, self.states= tf.nn.dynamic_rnn(self.fw_cell, self.fc_layer_out,
                                             sequence_length=self.seq,dtype=tf.float32)
           self.presoft=tf.matmul(self.outputs[0][0], self.weights) + self.biases
       elif self.configuration=='B':           
           if self.attention_number==0:
               self.bw_cell=self.cell_create_norm()
               self.outputs, self.states= tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, self.fc_layer_out,
                                         sequence_length=self.seq,dtype=tf.float32)


               self.presoft=tf.map_fn(lambda x:tf.matmul(x,self.weights)+self.biases,tf.concat((self.outputs[0],self.outputs[1]),2))
               
               
           elif self.attention_number>0:
               self.bw_cell=self.cell_create('1')
               self.bw_cell2=self.cell_create('2') 
               with tf.variable_scope('1'):

                   self.outputs, self.states= tf.nn.bidirectional_dynamic_rnn(self.fw_cell, self.bw_cell, self.fc_layer_out,
                                                     sequence_length=self.seq,dtype=tf.float32)
                                                  
               self.first_out=tf.concat((self.outputs[0],self.outputs[1]),2)
               with tf.variable_scope('2'):
                   self.outputs2, self.states2= tf.nn.bidirectional_dynamic_rnn(self.fw_cell2, self.bw_cell2, self.first_out,
                                                     sequence_length=self.seq,dtype=tf.float32)
               self.second_out=tf.concat((self.outputs2[0],self.outputs2[1]),2)

               for i in range((self.attention_number*2)+1):
                   self.attention_weight_init(i)

               
                
               self.zero_pad_second_out=tf.map_fn(lambda x:tf.pad(tf.squeeze(x),[[self.attention_number,self.attention_number],[0,0]]),self.second_out)
               self.first_out_reshape=tf.reshape(self.first_out,[-1,self.n_hidden[self.n_layers-1]*2])
               self.zero_pad_second_out_reshape=[]
               self.attention_m=[]
               for j in range((self.attention_number*2)+1):
                   self.zero_pad_second_out_reshape.append(tf.reshape(tf.slice(self.zero_pad_second_out,[0,j,0],[self.num_seqs,self.seq_len,self.n_hidden[self.n_layers-1]*2]),[-1,self.n_hidden[self.n_layers-1]*2]))
                   self.attention_m.append(tf.tanh(tf.matmul(tf.concat((self.zero_pad_second_out_reshape[j],self.first_out_reshape),1),self.attention_weights[j])))
               self.attention_s=tf.nn.softmax(tf.stack([tf.matmul(self.attention_m[j],self.sm_attention_weights[j]) for j in range(self.attention_number*2+1)]),0)
               self.attention_z=tf.reduce_sum([self.attention_s[j]*self.zero_pad_second_out_reshape[j] for j in range(self.attention_number*2+1)],0)
               self.attention_z_reshape=tf.reshape(self.attention_z,[self.num_seqs,self.seq_len,self.n_hidden[self.n_layers-1]*2])
               self.presoft=tf.map_fn(lambda x:tf.matmul(x,self.weights)+self.biases,self.attention_z_reshape)


              
       if  self.output_act=='softmax':   
           self.pred=tf.nn.softmax(self.presoft)
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
               
       elif self.output_act=='sigmoid':
           self.pred=tf.nn.sigmoid(self.presoft)    
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='NewHybridCE2':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='NewHybridCE4':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2)  
           elif self.cost_type=='HybridCEMS2':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='HybridCEMS4':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/4.,self.seq_len-2)     
           elif self.cost_type=='HybridCE2-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,1.0)                
           elif self.cost_type=='HybridCE4-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,1.0) 
           elif self.cost_type=='HybridCE2-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.9)                
           elif self.cost_type=='HybridCE4-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.9)
           elif self.cost_type=='HybridCE2-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.8)                
           elif self.cost_type=='HybridCE4-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.8)
           elif self.cost_type=='HybridCE2-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.7)                
           elif self.cost_type=='HybridCE4-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.7)  
           elif self.cost_type=='HybridCE2-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.6)                
           elif self.cost_type=='HybridCE4-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.6)
           elif self.cost_type=='HybridCE2-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.5)                
           elif self.cost_type=='HybridCE4-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.5) 
               
       if self.optimizer == 'GD':
             self.optimize = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
       elif self.optimizer == 'Adam':
             self.optimize = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost) 
       elif self.optimizer == 'RMS':
             self.optimize = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.cost) 

       self.init = tf.global_variables_initializer()
       self.saver = tf.train.Saver()
       self.saver_var = tf.train.Saver(tf.trainable_variables())
       if self.save_location==[]:
           self.save_location=os.getcwd()


      
class CNN(CRNN):
#     
     def __init__(self,training_data=[], training_labels=[], validation_data=[], validation_labels=[], network_save_filename=[], minimum_epoch=5, maximum_epoch=10, n_hidden=[100,100], n_classes=2, cell_type='LSTMP', configuration='B', attention_number=2, dropout=0.75, init_method='zero', truncated=100, optimizer='Adam', learning_rate=0.003 ,save_location=[],output_act='sigmoid',snippet_length=100,aug_prob=0,hop_size=512, cost_type='CE',num_frames_either_side=0,batch_size=1000,input_feature_size=84*11,conv_filter_shapes=[[3,3,1,32],[3,3,32,64]], conv_strides=[[1,1,1,1],[1,1,1,1]], pool_window_sizes=[[1,1,2,1],[1,1,2,1]],pad='SAME'):         
         self.features=training_data
         self.targ=training_labels
         self.val=validation_data
         self.val_targ=validation_labels
         self.filename=network_save_filename
         self.n_hidden=n_hidden
         self.n_layers=len(self.n_hidden)
         self.cell_type=cell_type
         self.dropout=dropout
         self.configuration=configuration
         self.init_method=init_method
         self.truncated=truncated
         self.optimizer=optimizer
         self.learning_rate=learning_rate
         self.n_classes=n_classes
         self.minimum_epoch=minimum_epoch
         self.maximum_epoch=maximum_epoch
         self.num_batch=int(len(self.features)/batch_size)
         self.val_num_batch=int(len(self.val)/batch_size)
         self.batch_size=batch_size
         self.attention_number=attention_number
         self.cost_type=cost_type
         self.nfes=num_frames_either_side
         self.input_feature_size=input_feature_size
         self.batch=np.zeros((self.batch_size,self.input_feature_size))
         self.batch_targ=np.zeros((self.batch_size,self.n_classes))
         self.save_location=save_location
         self.output_act=output_act
         self.snippet_length=snippet_length
         self.aug_prob=aug_prob
         self.hop_size=hop_size
         self.num_seqs=int(self.batch_size/self.snippet_length)
         self.conv_filter_shapes=conv_filter_shapes
         self.conv_strides=conv_strides
         self.pool_window_sizes=pool_window_sizes
         self.pool_strides=self.pool_window_sizes
         self.conv_layer_out=[]
         self.fc_layer_out=[]
         self.w_fc=[]
         self.b_fc=[]
         self.h_fc=[]
         self.w_conv=[]
         self.b_conv=[]
         self.h_conv=[]
         self.h_pool=[]
         self.h_drop_batch=[]
         self.pad=pad
        
             
     def conv2d(self,data, weights, conv_strides, pad):
         return tf.nn.conv2d(data, weights, strides=conv_strides, padding=pad)
     
     def max_pool(self,data, max_pool_window, max_strides, pad):
        return tf.nn.max_pool(data, ksize=max_pool_window,
                            strides=max_strides, padding=pad)
        
     def weight_bias_init(self):
               
         if self.init_method=='zero':
            self.biases = tf.Variable(tf.zeros([self.n_classes]))           
         elif self.init_method=='norm':
               self.biases = tf.Variable(tf.random_normal([self.n_classes]))           
         if self.init_method=='zero':  
             self.weights =tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes]))
         elif self.init_method=='norm':
               self.weights = { '1': tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes])),'2': tf.Variable(tf.random_normal([self.n_hidden[(len(self.n_hidden)-1)], self.n_classes]))} 

        
#     def weight_init(self,weight_shape):
#        weight=tf.Variable(tf.truncated_normal(weight_shape))    
#        return weight
#        
#     def bias_init(self,bias_shape,):   
#        bias=tf.Variable(tf.constant(0.1, shape=bias_shape))
#        return bias
    
#     def batch_dropout(self,data):
#        batch_mean, batch_var=tf.nn.moments(data,[0])
#        scale=tf.Variable(tf.ones([self.num_seqs*self.seq_len,data.get_shape()[1],data.get_shape()[2],data.get_shape()[3]]))
#        beta=tf.Variable(tf.zeros([self.num_seqs*self.seq_len,data.get_shape()[1],data.get_shape()[2],data.get_shape()[3]]))
#        h_poolb=tf.nn.batch_normalization(data,batch_mean,batch_var,beta,scale,1e-3)
#        return tf.nn.dropout(h_poolb, self.dropout_ph)
        
     def conv_2dlayer(self,layer_num):
        self.w_conv.append(self.weight_init(self.conv_filter_shapes[layer_num]))
        self.b_conv.append(self.bias_init([self.conv_filter_shapes[layer_num][3]]))
        self.h_conv.append(tf.nn.relu(self.conv2d(self.conv_layer_out[layer_num], self.w_conv[layer_num], self.conv_strides[layer_num], self.pad) + self.b_conv[layer_num]))
        self.h_pool.append(self.max_pool(self.h_conv[layer_num],self.pool_window_sizes[layer_num],self.pool_strides[layer_num],self.pad))       
#        self.conv_layer_out.append(self.batch_dropout(self.h_pool[layer_num]))  
        self.conv_layer_out.append(self.h_pool[layer_num])  

     def fc_layer(self,layer_num):
        if layer_num ==0:
            self.convout=self.conv_layer_out[len(self.conv_layer_out)-1]
            self.fc_layer_out.append(tf.reshape(self.convout, [tf.shape(self.convout)[0],tf.shape(self.convout)[1]*tf.shape(self.convout)[2]*tf.shape(self.convout)[3]]))
            self.w_fc.append(self.weight_init([self.convout.get_shape().as_list()[1]*self.convout.get_shape().as_list()[2]*self.convout.get_shape().as_list()[3], self.n_hidden[layer_num]]))
        else:
            self.w_fc.append(self.weight_init([self.n_hidden[layer_num-1], self.n_hidden[layer_num]]))
        self.b_fc.append(self.bias_init([self.n_hidden[layer_num]]))
        self.h_fc.append(tf.nn.relu(tf.matmul(self.fc_layer_out[layer_num], self.w_fc[layer_num]) + self.b_fc[layer_num]))
#        self.fc_layer_out.append(self.batch_dropout(self.h_fc[layer_num]))
        self.fc_layer_out.append(tf.nn.dropout(self.h_fc[layer_num], self.dropout_ph))
            
     def create(self):
       
       tf.reset_default_graph()
       self.x_ph = tf.placeholder("float32", [None, None, self.batch.shape[1]])
       self.y_ph = tf.placeholder("float32", [None, None, self.batch_targ.shape[1]]) 
       self.seq=tf.placeholder("int32")
       self.num_seqs=tf.placeholder("int32")
       self.seq_len=tf.placeholder("int32")
       self.dropout_ph = tf.placeholder("float32")
       self.weight_bias_init()
       
       self.conv_layer_out.append(tf.expand_dims(tf.reshape(self.x_ph,[-1,11,self.input_feature_size/11]),3))
       for i in range(len(self.conv_filter_shapes)):
            self.conv_2dlayer(i)
       for i in range(len(self.n_hidden)):
           self.fc_layer(i)
       self.presoft=tf.map_fn(lambda x:tf.matmul(x,self.weights)+self.biases,tf.reshape(self.fc_layer_out[len(self.fc_layer_out)-1],[self.num_seqs,self.seq_len,self.n_hidden[len(self.n_hidden)-1]]))  

       if  self.output_act=='softmax':   
           self.pred=tf.nn.softmax(self.pre_soft)
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
               
       elif self.output_act=='sigmoid':
           self.pred=tf.nn.sigmoid(self.presoft)    
           if self.cost_type=='CE':
               self.cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=tf.reshape(self.presoft,[-1,self.n_classes]), labels=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='MS':
               self.cost=tf.reduce_mean(tf.losses.mean_squared_error(labels=tf.reshape(self.presoft,[-1,self.n_classes]),predictions=tf.reshape(self.y_ph,[-1,self.n_classes])))
           elif self.cost_type=='NewHybridCE2':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='NewHybridCE4':
               self.cost=CSFunctions.NewHybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2)  
           elif self.cost_type=='HybridCEMS2':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/2.,self.seq_len-2)                
           elif self.cost_type=='HybridCEMS4':
               self.cost=CSFunctions.HybridCEMS(self.pred,self.y_ph,1/4.,self.seq_len-2)     
           elif self.cost_type=='HybridCE2-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,1.0)                
           elif self.cost_type=='HybridCE4-100':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,1.0) 
           elif self.cost_type=='HybridCE2-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.9)                
           elif self.cost_type=='HybridCE4-90':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.9)
           elif self.cost_type=='HybridCE2-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.8)                
           elif self.cost_type=='HybridCE4-80':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.8)
           elif self.cost_type=='HybridCE2-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.7)                
           elif self.cost_type=='HybridCE4-70':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.7)  
           elif self.cost_type=='HybridCE2-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.6)                
           elif self.cost_type=='HybridCE4-60':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.6)
           elif self.cost_type=='HybridCE2-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/2.,self.seq_len-2,0.5)                
           elif self.cost_type=='HybridCE4-50':
               self.cost=CSFunctions.HybridCE(self.pred,self.y_ph,1/4.,self.seq_len-2,0.5) 
       if self.optimizer == 'GD':
             self.optimize = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
       elif self.optimizer == 'Adam':
             self.optimize = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost) 
       elif self.optimizer == 'RMS':
             self.optimize = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.cost) 

       self.init = tf.global_variables_initializer()
       self.saver = tf.train.Saver()
       self.saver_var = tf.train.Saver(tf.trainable_variables())
       if self.save_location==[]:
           self.save_location=os.getcwd()       
             
  