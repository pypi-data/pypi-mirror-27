from collections.abc import Callable
import numpy as np
from keras import backend as K
from keras import initializers
from keras import activations
from keras.engine.topology import Layer


class KeyValueAttention1DLayer(Layer):
    """key-value-attention1d的特点是输入的Key和Value为成对的数据Query一般为外部数据,Key和Query有一致的dim,和Value有一致的timestep,
    输出的是Query的timestep,Value的dim形状的张量

    Attributes:
        similarity (Union[Callable,str]): - 指定使用的相似度计算函数,目前可选的有\
        加性相似度(additive),乘性相似度(multiplicative),点乘相似度(dot_product),\
        当然也可以自己写一个,只要最终输出的是一个(?,output,input_timestep)的
        kernel_initializer (str): - 权重V的初始化函数,默认glorot_uniform
        wk_kernel_initializer (): - 权重W_k的初始化函数,默认glorot_uniform
        wq_kernel_initializer (): - 权重W_q的初始化函数,默认glorot_uniform
    """

    def __init__(self, similarity="additive",
                 kernel_initializer='glorot_uniform',
                 wk_kernel_initializer='glorot_uniform',
                 wq_kernel_initializer='glorot_uniform',
                 **kwargs):
        if isinstance(similarity, Callable):
            self.similarity = similarity
        elif isinstance(similarity, str) and similarity in (
                "multiplicative", "dot_product", "additive"):
            self.similarity = similarity
        else:
            raise ValueError(
                'similarity now only support '
                '"multiplicative","dot_product","additive",'
                'and you can input a function as the similarity function!'
            )

        self.kernel_initializer = initializers.get(kernel_initializer)
        self.wk_kernel_initializer = initializers.get(
            wk_kernel_initializer)
        self.wq_kernel_initializer = initializers.get(
            wq_kernel_initializer)
        self.dim = None
        if self.similarity == "additive":
            self.kernel = None
            self.wk_kernel = None
            self.wq_kernel = None
        elif self.similarity == "multiplicative":
            self.kernel = None
        super().__init__(**kwargs)

    def _build_w(self, s_time, q_time, dim):
        self.dim = dim
        if self.similarity == "additive":
            self.kernel = self.add_weight(
                name='kernel',
                shape=(dim, s_time),
                initializer=self.kernel_initializer,
                trainable=True)
            self.wk_kernel = self.add_weight(
                name='wk_kernel',
                shape=(q_time, s_time),
                initializer=self.wk_kernel_initializer,
                trainable=True)
            self.wq_kernel = self.add_weight(
                name='wq_kernel',
                shape=(q_time, q_time),
                initializer=self.wk_kernel_initializer,
                trainable=True)
        elif self.similarity == "multiplicative":
            self.kernel = self.add_weight(
                name='kernel',
                shape=(
                    dim, dim),
                initializer=self.kernel_initializer,
                trainable=True)

    def build(self, input_shape):
        if not isinstance(input_shape, list) or len(input_shape) != 3:
            raise ValueError('A key-value attention layer should be called '
                             'on a list of 3 inputs.')

        if len(input_shape[0]) != 3 or len(
                input_shape[1]) != 3 or len(input_shape[2]) != 3:
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs.'
                             'Got ' + str(input_shape) + ' inputs.')
        if input_shape[0][-1] != input_shape[2][-1]:
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs '
                             'and key ,query have the same dim.'
                             'Got ' + str(input_shape) + ' inputs.')

        if input_shape[0][-2] != input_shape[1][-2]:
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs '
                             'and key ,value have the same timestep.'
                             'Got ' + str(input_shape) + ' inputs.')

        dim = input_shape[0][-1]
        s_time = input_shape[0][1]
        q_time = input_shape[2][1]
        self._build_w(s_time, q_time, dim)
        # Be sure to call this somewhere!
        super().build(input_shape)

    def multiplicative(self, Key, Query):
        r"""乘性相似度,其中的权重矩阵形状为[dim,dim]\
        输出的固定为与原输入一样形状

        .. math::  Similarity(Key,Query) = Query \cdot W \cdot Source^T
        """
        Key_t = K.permute_dimensions(Key, (0, 2, 1))
        s = K.dot(Query, self.kernel)
        sim = K.batch_dot(s, Key_t)
        return sim

    def dot_product(self, Key, Query):
        r"""点乘相似度,在google的attention is all you need 中看到的.\
        很迷,没有要训练的矩阵,直接转置点乘

        .. math::  Similarity(Key,Query) = \frac{Key^T\cdot Query}{\sqrt{d_k}}
        """
        sim = K.batch_dot(Key, Query)
        return sim

    def additive(self, Key, Query):
        r"""
        加性相似度,最经典的注意力相似度机制,如果是在self attention中\
        则该层有3个权重矩阵形状为W_k(time_q,time_k)和W_q(time_q,time_q)\
        以及V(dim,time_k)

        .. math:: Similarity(Key)=tanh(W_k\cdot Key+W_q\cdot Query)\cdot V
        """
        key_att = K.dot(self.wk_kernel, Key)
        key_att = K.permute_dimensions(key_att, (1, 0, 2))
        que_att = K.dot(self.wq_kernel, Query)
        que_att = K.permute_dimensions(que_att, (1, 0, 2))
        f_att = key_att + que_att
        sim = K.dot(K.tanh(f_att), self.kernel)
        return sim

    def _call_attention(self, Key, Value, Query):
        r"""self-attention就是通过相似度函数计算得的相似矩阵过softmax后与自身点乘得到

        .. math::  A = Softmax(Similarity(Source,Query))
        .. math::  C = A \cdot Source
        """
        if isinstance(self.similarity, Callable):
            sim = self.similarity(Key, Query)
        else:
            sim = getattr(self, self.similarity)(Key, Query)
        sm = activations.softmax(sim)
        result = K.batch_dot(sm, Value)
        return result

    def call(self, inputs):
        Key = inputs[0]
        Value = inputs[1]
        Query = inputs[2]
        result = self._call_attention(Key, Value, Query)
        return result

    def compute_output_shape(self, input_shape):
        return (input_shape[-1][0], input_shape[-1][1], input_shape[1][-1])

    def get_config(self):
        config = {
            'similarity': self.similarity,
            'kernel_initializer': self.kernel_initializer,
            'wk_kernel_initializer': self.wk_kernel_initializer,
            'wq_kernel_initializer': self.wq_kernel_initializer
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class KeyValueAttention2DLayer(KeyValueAttention1DLayer):
    """key-value-attention2d的特点是输入的Key和Value为成对的数据Query一般为外部数据,
    Key和Query有一致的dim,和Value有一致的timestep,也就是中间两个纬度,
    输出的是Query的timestep,Value的dim形状的张量.
    4d的attention是为cnn设计的,其原理就是将4维的中间两维压缩为一维,之后输出的时候再解压缩出来.

    Attributes:
        output_size (tuple[int,int]): - 指定输出的形状,如果是加性相似度(additive),\
        则必须指定,且可以随意指定,如果是其他则可以不指定,那就是原样形状输出,\
        如果指定的话则必须积与原形状第1,2纬度的积相等
        similarity (Union[Callable,str]): - 指定使用的相似度计算函数,目前可选的有\
        加性相似度(additive),乘性相似度(multiplicative),点乘相似度(dot_product),\
        当然也可以自己写一个,只要最终输出的是一个(?,output,input_timestep)的\
        用于指定第一个权重的形状,各维的意义[输出的纬度,第二个权重矩阵的第一个纬度]
        kernel_initializer (str): - 第一个权重的初始化函数,默认glorot_uniform
        wk_kernel_initializer (str): - 第二个权重的初始化函数,默认glorot_uniform
        wq_kernel_initializer (str): - 权重W_q的初始化函数,默认glorot_uniform
    """

    def __init__(self, output_size=None,
                 similarity="additive", *,
                 kernel_initializer='glorot_uniform',
                 wk_kernel_initializer='glorot_uniform',
                 wq_kernel_initializer='glorot_uniform',
                 **kwargs):
        self.output_size = output_size
        super().__init__(similarity=similarity,
                         kernel_initializer=kernel_initializer,
                         wk_kernel_initializer=wk_kernel_initializer,
                         wq_kernel_initializer=wq_kernel_initializer, **kwargs)

    def build(self, input_shape):
        if not isinstance(input_shape, list) or len(input_shape) != 3:
            raise ValueError('A attention layer should be called '
                             'on a list of 3 inputs.')

        if len(input_shape[0]) != 4 or len(
                input_shape[1]) != 4 or len(input_shape[2]) != 4:
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs.'
                             'Got ' + str(input_shape) + ' inputs.')
        if input_shape[0][-1] != input_shape[2][-1]:
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs '
                             'and key ,query have the same dim.'
                             'Got ' + str(input_shape) + ' inputs.')

        if (input_shape[0][1] != input_shape[1][1]) or (
                input_shape[0][2] != input_shape[1][2]):
            raise ValueError('A key-value attention layer should be called '
                             'by 3 (batch,time_step,dim)3D inputs '
                             'and key ,value have the same timestep.'
                             'Got ' + str(input_shape) + ' inputs.')

        dim = input_shape[0][-1]
        self.dim = input_shape[1][-1]
        s_time = input_shape[0][1] * input_shape[0][2]
        q_time = input_shape[2][1] * input_shape[2][2]

        if (self.output_size is not None) and (
                q_time != self.output_size[0] * self.output_size[1]):
            raise ValueError('output size error ')
        if self.output_size is None:
            self.output_size = (input_shape[1][1], input_shape[1][2])
        self._build_w(s_time, q_time, dim)
        super(KeyValueAttention1DLayer, self).build(input_shape)

    def call(self, inputs):
        r"""self-attention就是通过相似度函数计算得的相似矩阵过softmax后与自身点乘得到

        .. math::  A = Softmax(Similarity(Key,Query))
        .. math::  C = A \cdot Value
        """
        Key_ = inputs[0]
        Value_ = inputs[1]
        Query_ = inputs[2]
        Key_shape = Key_.shape
        Value_shape = Value_.shape
        Query_shape = Query_.shape

        Key = K.reshape(
            Key_, shape=np.asarray(
                [-1,
                 (Key_shape[1] * Key_shape[2]).value,
                 Key_shape[3].value]))
        Value = K.reshape(
            Value_, shape=np.asarray(
                [-1,
                 (Value_shape[1] * Value_shape[2]).value,
                 Value_shape[3].value]))
        Query = K.reshape(
            Query_, shape=np.asarray(
                [-1,
                 (Query_shape[1] * Query_shape[2]).value,
                 Query_shape[3].value]))
        _result = self._call_attention(Key, Value, Query)
        result = K.reshape(
            _result,
            np.asarray([-1,
                        self.output_size[0],
                        self.output_size[1],
                        self.dim]))
        return result

    def compute_output_shape(self, input_shape):
        return (input_shape[0][0],  self.output_size[0],
                self.output_size[1], self.dim)

    def get_config(self):
        config = {
            "output_size": self.output_size
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


__all__ = ["KeyValueAttention1DLayer", "KeyValueAttention2DLayer"]
