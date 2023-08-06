============================================
深度学习的成功证明了什么
============================================
.. What did the success of deep learning prove?

深度学习最大的成功，其实是通过实践证明了，大脑的智能是可以通过仿生学的方式进行模拟的。
而进一步的，这种仿生学的智能路线证明了，结构的美，与组合方式的美，能产生更完美、更先
进的智能行为。

近几年来，在computer vision和natural language processing/understanding上的深度学习
实践表明，任何分类、识别等任务的巨大成功，其实都源于深度学习网络的结构的巨大成功：或是
网络结构的不断加深，如VGG16 [1]_ ，VGG19 [1]_ ，Residual Neural Network [2]_ 、
Densely connected Network [3]_ ；或是网络组件的不断变革，如Simple RNN Cell 到 LSTM
Cell [4]_ 或GRU Cell [5]_ ，inception v3 cell [6]_ ；或是网络组件的有效的不断组合，
如Google's Neural Machine Translation System [7]_ ，attention machinism [8]_ 的广
泛应用，CNN+RNN在图像语义 [9]_ 中的广泛应用。

当然，这些所有组件组合的成功，其实都基于深度学习基础性研究的巨大突破，如ReLU激活函
数 [10]_ 、batch normalization [11]_ 、各种参数初始化方法(如 glorot
initialization [12]_ , orthogonal initialization [13]_ 等)、各种优化方法(如SGD、
RMSprop [14]_ 、Adam [15]_ 等) :math:`\cdots` 也就是说，这些所有的基础性tricks保证
了深度学习网络至少能工作，而结构的不断扩展使得深度学习能更好地、更有效地工作。

深度学习处处体现了结构的美，组合的美。它的所有思想其实都源自于生活，如attention思想非
常简单直观。在 Neural Machine Translation 上，一个语言到另一个语言的翻译，其实翻译出
的该词很大程度上只依赖于前一语言中的部分词。而在各种classification的任务上，一个句子的
结果往往只对该句部分有效词才具备较强的依赖性。

深度学习的成功告诉我们，人工智能的仿生学方法是可行的。我们要做的，就是：或是不断地利用
已有组件创造出更好、更优秀的网络，或是不断地从生理学、心理学中获得灵感借鉴到深度学习中
创造出更好的结构；更或者，创造出更优秀的、更有效的基础组件，来服务于更高层网络的构建。
另外，深度学习的实践也证明了，我们可以从仿生学起步，再到超越仿生学，走出一条自己的路，
即走出一条具有深度学习特色的智能系统实现之路。比如，如今的Residual Network [2]_ 的层数
就早已经超越大脑视觉系统处理的层数，将层数扩展到上千层(当然，我们也可以说，Residual
Network只是从很巧合地模仿到了大脑某些我们未知的结构。

另外，深度学习的成功也进一步表明了，人类认识复杂系统的困难性，甚至是不可能性。连深度学
习这么简单的模拟人脑神经元结构的网络，数学或者哲学等等学科都无法解释，那更别说实际的、
这么复杂的、真正的大脑。

``2016-11-27``


.. [1] Simonyan, Karen, and Andrew Zisserman. "Very deep convolutional networks
        for large-scale image recognition." arXiv preprint arXiv:1409.1556 (2014).
.. [2] He, Kaiming, et al. "Deep residual learning for image recognition."
        Proceedings of the IEEE Conference on Computer Vision and Pattern
        Recognition. 2016.
.. [3] Huang, Gao, et al. "Densely connected convolutional networks." arXiv
        preprint arXiv:1608.06993 (2016).
.. [4] Hochreiter, Sepp, and Jürgen Schmidhuber. "Long short-term memory."
        Neural computation 9.8 (1997): 1735-1780.
.. [5] Cho, Kyunghyun, et al. "Learning phrase representations using RNN
        encoder-decoder for statistical machine translation." arXiv preprint
        arXiv:1406.1078 (2014).
.. [6] Szegedy, Christian, et al. "Rethinking the inception architecture for
        computer vision." Proceedings of the IEEE Conference on Computer Vision
        and Pattern Recognition. 2016.
.. [7] Wu, Yonghui, et al. "Google's Neural Machine Translation System: Bridging
        the Gap between Human and Machine Translation." arXiv preprint
        arXiv:1609.08144 (2016).
.. [8] Bahdanau, Dzmitry, Kyunghyun Cho, and Yoshua Bengio. "Neural machine
        translation by jointly learning to align and translate." arXiv preprint
        arXiv:1409.0473 (2014).
.. [9] Karpathy, Andrej, and Li Fei-Fei. "Deep visual-semantic alignments for
        generating image descriptions." Proceedings of the IEEE Conference on
        Computer Vision and Pattern Recognition. 2015.
.. [10] Maas, Andrew L., Awni Y. Hannun, and Andrew Y. Ng. "Rectifier
        nonlinearities improve neural network acoustic models." Proc. ICML.
        Vol. 30. No. 1. 2013.
.. [11] Ioffe, Sergey, and Christian Szegedy. "Batch normalization: Accelerating deep network
        training by reducing internal covariate shift." arXiv preprint arXiv:1502.03167 (2015).
.. [12] Glorot, Xavier, and Yoshua Bengio. "Understanding the difficulty of training deep feedforward neural networks." Aistats. Vol. 9. 2010.
.. [13] Saxe, Andrew M., James L. McClelland, and Surya Ganguli. "Exact solutions to the nonlinear dynamics of learning in deep linear neural networks." arXiv preprint arXiv:1312.6120 (2013).
.. [14] Tieleman, Tijmen, and G. Hinton. "Lecture 6.5-RMSProp, COURSERA: Neural networks for
        machine learning." University of Toronto, Tech. Rep (2012).
.. [15] Kingma, Diederik, and Jimmy Ba. "Adam: A method for stochastic optimization." arXiv
        preprint arXiv:1412.6980 (2014).
