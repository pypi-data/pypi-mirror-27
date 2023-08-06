
=================
Language Modeling
=================

A statistical language model is a probability distribution over sequences of words.
Given such a sequence, say of length :math:`m`, it assigns a probability :math:`P(w_1, \cdots, w_m)`
to the whole sequence. Having a way to estimate the relative likelihood of different
phrases is useful in many natural language processing applications, especially ones
that generate text as an output. Language modeling is used in speech recognition,
machine translation, part-of-speech tagging, parsing, handwriting recognition,
information retrieval and other applications. [2]_

In speech recognition, the computer tries to match sounds with word sequences. The
language model provides context to distinguish between words and phrases that sound
similar. For example, in American English, the phrases "recognize speech" and "wreck
a nice beach" are pronounced almost the same but mean very different things. These
ambiguities are easier to resolve when evidence from the language model is incorporated
with the pronunciation model and the acoustic model. [2]_


Papers
------

* [12.10] `Large Scale Language Modeling in Automatic Speech Recognition
  <https://arxiv.org/abs/1210.8440>`_


Posts
-----

* `Ngram 语言模型 <https://flystarhe.github.io/2016/08/16/ngram/>`_
* `[我们是这样理解语言的-2]统计语言模型 <http://www.flickering.cn/nlp/2015/02/%E
  6%88%91%E4%BB%AC%E6%98%AF%E8%BF%99%E6%A0%B7%E7%90%86%E8%A7%A3%E8%AF%AD%E8%A8
  %80%E7%9A%84-2%E7%BB%9F%E8%AE%A1%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/>`_, 我们不妨一起看下语言模型，尤其是 N-Gram 语言模型的数学表示、效果评估、模型平滑及模型训练（尤其是分布式），为我们后续介绍神经网络语言模型和序列标注技术打个好基础。
* `[我们是这样理解语言的-3]神经网络语言模型 <http://www.flickering.cn/nlp/2015/03
  /%E6%88%91%E4%BB%AC%E6%98%AF%E8%BF%99%E6%A0%B7%E7%90%86%E8%A7%A3%E8%AF%AD%E8%
  A8%80%E7%9A%84-3%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AF%AD%E8%A8%80%E6%A8%
  A1%E5%9E%8B/>`_, 随着深度学习的发展，神经网络相关研究越来越深入，神经网络语言模型（Neural Network Language Model，NNLM）越来越受到学术界和工业界的关注，本文将系统介绍下 NNLM 的建模及其应用。
* `在Keras模型中使用预训练的词向量 <https://keras-cn.readthedocs.io/en/latest/blog/word_embedding/>`_, 通过本教程，你可以掌握技能：使用预先训练的词向量和卷积神经网络解决一个文本分类问题 本文代码已上传到Github
* `中文维基百科语料库词向量的训练 <http://wulc.me/2016/10/12/%E4%B8%AD%E6%96%87%E7%BB%B4%E5%9F%BA%E7%99%BE%E7%A7%91%E7%9A%84%E8%AF%8D%E5%90%91%E9%87%8F%E7%9A%84%E8%AE%AD%E7%BB%83/>`_, 要通过计算机进行自然语言处理，首先就需要将这些文本数字化。目前用得最广泛的方法是词向量，根据训练使用算法的不同，目前主要有 Word2Vec 和 GloVe 两大方法，本文主要讲述通过这两个方法分别训练中文维基百科语料库的词向量。




Software
--------

* `fastText <https://github.com/facebookresearch/fastText>`_, fastText is a library for efficient learning of word representations and sentence classification.
* `word2vec <https://github.com/dav/word2vec>`_, This tool provides an efficient implementation of the continuous bag-of-words and skip-gram architectures for computing vector representations of words.
* `gensim <https://github.com/RaRe-Technologies/gensim>`_, Gensim is a Python library for topic modelling, document indexing and similarity retrieval with large corpora. Target audience is the natural language processing (NLP) and information retrieval (IR) community.


* IRSTLM: `HomePage <http://hlt-mt.fbk.eu/technologies/irstlm>`_,
  `Github <https://github.com/irstlm-team/irstlm>`_ and
  `test codes <https://github.com/irstlm-team/irstlm-regression-testing>`_,
  and `SourceForge <https://sourceforge.net/projects/irstlm/>`_
  The IRST Language Modeling (IRSTLM) Toolkit features algorithms and data structures suitable to estimate,
  store, and access very large n-gram language models. Our software has been integrated into a popular
  open source Statistical Machine Translation decoder called Moses, and is compatible with language
  models created with other tools, such as the SRILM Tooolkit.
* SRILM: `HomePage <http://www.speech.sri.com/projects/srilm/>`_, `语言模型训练工具SRILM详解
  <http://www.52nlp.cn/language-model-training-tools-srilm-details>`_,
  SRILM is a toolkit for building and applying statistical language models (LMs), primarily for use in
  speech recognition, statistical tagging and segmentation, and machine translation. It has been under
  development in the SRI Speech Technology and Research Laboratory since 1995. The toolkit has also greatly
  benefitted from its use and enhancements during the Johns Hopkins University/CLSP summer workshops
  in 1995, 1996, 1997, and 2002 (see history). SRILM consists of the following components:

  - A set of C++ class libraries implementing language models, supporting data stuctures and
    miscellaneous utility functions.
  - A set of executable programs built on top of these libraries to perform standard tasks
    such as training LMs and testing them on data, tagging or segmenting text, etc.
  - A collection of miscellaneous scripts facilitating minor related tasks.

  SRILM runs on UNIX and Windows platforms. Related papers: [4]_, [5]_, [6]_ and [7]_.
* MIT Language Modeling Toolkit: `Github <https://github.com/mitlm/mitlm>`_,
  The MIT Language Modeling (MITLM) toolkit is a set of tools designed
  for the efficient estimation of statistical n-gram language models
  involving iterative parameter estimation.  It achieves much of its
  efficiency through the use of a compact vector representation of
  n-grams.  Details of the data structure and associated algorithms can
  be found in the paper [1]_. Currently, MITLM supports the following features:

  - Smoothing: Modified Kneser-Ney, Kneser-Ney, maximum likelihood
  - Interpolation: Linear interpolation, count merging, generalized
    linear interpolation
  - Evaluation: Perplexity
  - File formats: ARPA, binary, gzip, bz2
* BerkeleyLM: `Google Code <https://code.google.com/archive/p/berkeleylm/>`_,
  This project provides a library for estimating storing large n-gram language
  models in memory and accessing them efficiently. It is described in the paper [3]_.
  Its data structures are faster and smaller than `SRILM <http://www.speech.sri.com/projects/srilm/>`_
  and nearly as fast as `KenLM <http://kheafield.com/code/kenlm/>`_ despite being
  written in Java instead of C++. It also achieves the best published lossless encoding
  of the Google n-gram corpus.
* KenLM: `HomePage <http://kheafield.com/code/kenlm/>`_
  and `Github <https://github.com/kpu/kenlm>`_,
  recent and popular language modeling toolkit.




.. references

.. [1] Bo-June (Paul) Hsu and James Glass. Iterative Language Model Estimation:
        Efficient Data Structure & Algorithms.  In Proc. Interspeech, 2008.
.. [2] https://en.wikipedia.org/wiki/Language_model
.. [3] Pauls, Adam, and Dan Klein. "Faster and smaller n-gram language models."
        Proceedings of the 49th Annual Meeting of the Association for Computational
        Linguistics: Human Language Technologies-Volume 1. Association for Computational
        Linguistics, 2011. http://nlp.cs.berkeley.edu/pubs/Pauls-Klein_2011_LM_paper.pdf
.. [4] A. Stolcke (2002), SRILM -- An Extensible Language Modeling Toolkit. Proc. Intl.
        Conf. on Spoken Language Processing, vol. 2, pp. 901-904, Denver.
.. [5] J. A. Bilmes and K. Kirchhoff (2003), Factored language models and generalized parallel
        backoff, Proc. HLT-NAACL, pp. 7-9, Edmonton, Alberta.
.. [6] T. Alumäe and M. Kurimo (2010), Efficient Estimation of Maximum Entropy Language
        Models with N-gram features: an SRILM extension, Proc. Interspeech, pp. 1820-1823,
        Makuhari, Japan.
.. [7] Stolcke, Andreas, et al. "SRILM at sixteen: Update and outlook." Proceedings of IEEE
        Automatic Speech Recognition and Understanding Workshop. Vol. 5. 2011.



