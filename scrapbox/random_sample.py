import tensorflow as tf

learning_rate = 0.01

with tf.Session() as sess:
    for i in range(100):
        elems = tf.convert_to_tensor([0, 1])
        samples = tf.multinomial(tf.log([[learning_rate, 1 - learning_rate]]), 1)  # note log-prob
        print(elems[tf.cast(samples[0][0], tf.int32)].eval())
        learning_rate += 0.01