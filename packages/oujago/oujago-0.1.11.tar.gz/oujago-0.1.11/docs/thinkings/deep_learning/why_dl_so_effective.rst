
========================================
深度学习为何如此有效
========================================
.. Why Deep Neural Network is so Effective?

It can work
===========

深度学习方法其实提出了很多年。但是，却只在近几年显现出威力。是因为，只有在这些年，我们才知道，
什么样的参数与什么样的手段能使DL能work起来。比如优化方法的一些变革 [1]_ [2]_ [3]_ [4]_ [5]_,
Mini-Batch SGD、ReLU激活函数 [6]_ 、Batch Normalization [7]_ 等。

所有上述这些，其实都是 *tricks* ！！！不是什么深度学习的颠覆性的重大突破等。深度学习为什么有效？
前提就是，它能work起来！

``2016-11-07``


Data
====

深度学习最大的贡献，其实就是颠覆人工智能领域以前“人工特征”的范式，知识驱动转换成数据驱动，
摈弃feature engineering。因为，**人工特征提供的知识、经验，其实都蕴含在数据中**，都是在
数据中得以体现。所以，如果当数据量大得很，达到一定程度的时候，*直接从数据中学到经验和知识*，
就不是不可能。那为什么只有数据量大了才能够学到这些经验与知识呢？我从训练的微观角度的思考如下：
第一，**见多识广**。训练数据提供了更广泛的分布，更有效的样本，深度学习模型的参数因为得到
了 *很多不同的输入* 的刺激，导致一些更新不到的参数得到了有效的更新。第二，**见微知著**。训练数
据中存在着大量看起来差不多的、但是结果却完全不同的相似数据，深度学习模型的参数因为得到了 *很多
相似的输入* 的刺激，导致已经训练僵化的参数做出变化，产生新的特征！因此，如此大量的数据，正如山
世光研究员所说，导致“**测试数据与训练数据同分布**”，或者“**测试数据跑不出训练数据的范围**”
时，深度学习模型就开始见效。

``2016-11-07``

Algorithms
==========

但是，仅仅是数据量大也不行，还得算法牛逼。DL方法提供了足够复杂的算法，**参数足够多，非线性
转化函数也足够多**。

``2016-11-07``


Nonhuman Logic
==============

深度学习为何如此有效？我试图再次从定性的角度给一个简短的解释。那就是，以前的算法都是在人类的
逻辑思维可解决的范围内进行工作。但是深度学习提供一个超越人类逻辑思维所能理解的方式，来处理一
些智能问题。

``2016-12-12``




.. [1] Duchi, John, Elad Hazan, and Yoram Singer. "Adaptive subgradient methods for online
        learning and stochastic optimization." Journal of Machine Learning Research 12.Jul
        (2011): 2121-2159.
.. [2] Tieleman, Tijmen, and G. Hinton. "Lecture 6.5-RMSProp, COURSERA: Neural networks for
        machine learning." University of Toronto, Tech. Rep (2012).
.. [3] Zeiler, Matthew D. "ADADELTA: an adaptive learning rate method." arXiv preprint
        arXiv:1212.5701 (2012).
.. [4] Lin, Rui, et al. "Hierarchical Recurrent Neural Network for Document Modeling."
        EMNLP. 2015.
.. [5] Kingma, Diederik, and Jimmy Ba. "Adam: A method for stochastic optimization." arXiv
        preprint arXiv:1412.6980 (2014).
.. [6] Maas, Andrew L., Awni Y. Hannun, and Andrew Y. Ng. "Rectifier nonlinearities improve
        neural network acoustic models." Proc. ICML. Vol. 30. No. 1. 2013.
.. [7] Ioffe, Sergey, and Christian Szegedy. "Batch normalization: Accelerating deep network
        training by reducing internal covariate shift." arXiv preprint arXiv:1502.03167 (2015).


