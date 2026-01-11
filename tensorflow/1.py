import tensorflow as tf
import numpy as np
a=tf.constant([[[0,1,2,3,4],[5,6,7,8,9]],])
print(a)
rank_0_tensor = tf.constant(4)
print(rank_0_tensor)
a = tf.constant([[1, 2],
                 [3, 4]])
b = tf.constant([[1, 1],
                 [1, 1]]) # Could have also said `tf.ones([2,2], dtype=tf.int32)`

print(tf.add(a, b), "\n")
print(tf.multiply(a, b), "\n")
print(tf.matmul(a, b), "\n")