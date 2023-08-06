
.. image:: https://readthedocs.org/projects/oujago/badge
   :target: http://oujago.readthedocs.io/en/latest
   :alt: Documentation Status

.. image:: https://img.shields.io/github/issues/oujago/oujago.svg
   :target: https://github.com/oujago/oujago



======
Oujago
======

Coding makes the life easier. This is a factory contains commonly used
algorithms and useful links.


Documentation
=============

Available online documents: `latest <http://oujago.readthedocs.io/en/latest/>`_
and `develop <http://oujago.readthedocs.io/en/develop/>`_.


Installation
============

Install ``oujago`` using pip:

.. code-block:: bash

    $> pip install oujago

Install from source code:

.. code-block:: bash

    $> python setup.py clean --all install


Download data from `BaiDuYun <https://pan.baidu.com/s/1i57RVLj>`_:

.. code-block::

    https://pan.baidu.com/s/1i57RVLj


APIs
====


Natural Language Processing
---------------------------

Hanzi Converter
^^^^^^^^^^^^^^^

繁简转换器.

.. code-block:: shell

    >>> from oujago.nlp import FJConvert
    >>> FJConvert.to_tradition('繁简转换器')
    '繁簡轉換器'
    >>> FJConvert.to_simplify('繁簡轉換器')
    '繁简转换器'
    >>> FJConvert.same('繁简转换器', '繁簡轉換器')
    >>> True
    >>> FJConvert.same('繁简转换器', '繁簡轉換')
    >>> False


Chinese Segment
^^^^^^^^^^^^^^^

Support ``jieba``, ``LTP``, ``thulac``, ``pynlpir`` etc. public segmentation methods.

.. code-block:: shell

    >>> from oujago.nlp import seg
    >>>
    >>> sentence = "这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。"
    >>> seg(sentence, mode='ltp')
    ['这', '是', '一个', '伸手', '不', '见', '五', '指', '的', '黑夜', '。', '我', '叫', '孙悟空',
    '，', '我', '爱', '北京', '，', '我', '爱', 'Python', '和', 'C', '+', '+', '。']
    >>> seg(sentence, mode='jieba')
    ['这是', '一个', '伸手不见五指', '的', '黑夜', '。', '我', '叫', '孙悟空', '，', '我', '爱',
    '北京', '，', '我', '爱', 'Python', '和', 'C++', '。']
    >>> seg(sentence, mode='thulac')
    ['这', '是', '一个', '伸手不见五指', '的', '黑夜', '。', '我', '叫', '孙悟空', '，',
    '我', '爱', '北京', '，', '我', '爱', 'Python', '和', 'C', '+', '+', '。']
    >>> seg(sentence, mode='nlpir')
    ['这', '是', '一个', '伸手', '不见', '五指', '的', '黑夜', '。', '我', '叫', '孙悟空',
    '，', '我', '爱', '北京', '，', '我', '爱', 'Python', '和', 'C++', '。']
    >>>
    >>> seg("这是一个伸手不见五指的黑夜。")
    ['这是', '一个', '伸手不见五指', '的', '黑夜', '。']
    >>> seg("这是一个伸手不见五指的黑夜。", mode='ltp')
    ['这', '是', '一个', '伸手', '不', '见', '五', '指', '的', '黑夜', '。']
    >>> seg('我不喜欢日本和服', mode='jieba')
    ['我', '不', '喜欢', '日本', '和服']
    >>> seg('我不喜欢日本和服', mode='ltp')
    ['我', '不', '喜欢', '日本', '和服']


Part-of-Speech
^^^^^^^^^^^^^^

.. code-block:: shell

    >>> from oujago.nlp.postag import pos
    >>> pos('我不喜欢日本和服', mode='jieba')
    ['r', 'd', 'v', 'ns', 'nz']
    >>> pos('我不喜欢日本和服', mode='ltp')
    ['r', 'd', 'v', 'ns', 'n']


