==========================
深度学习：系统科学的视角
==========================


系统科学
===========

系统科学 [1]_ [2]_ 是关于整体涌现性的基础科学。系统科学的开创者贝塔朗菲指出，要区分两类整体，
一类是加和性整体，即非系统，不具备涌现性；另一类是非加和性整体，即系统，具有涌现性。
系统科学研究的并不是一切的整体和整体性，而只关注于非加和性整体，即整体涌现性。涌现现象定性地
表述为：**整体具有部分及其总和所没有的新的属性或行为模式，用部分的性质或模式不可能全面解释整体的
性质和模式**。即“整体大于部分之和”。涌现现象也可定量表述为：令 :math:`W` 记为系统整体，
由 :math:`n` 个部分组成；令 :math:`p_i` 记为第 :math:`i` 个部分， :math:`i=1,2, \cdots, n`；
则形式化表示为

.. math:: W > \sum_i^n p_i

更简洁地表述为

.. math:: 2 > 1 + 1

自然界中，存在着大量的涌现现象。比如蚁群 [3]_ 。单个蚂蚁的行为是可由一个简单的规则集概括，如
“沿着气味前进”、“用上颚抓紧物体”、“在认为危险的地方留下气味标记”等。但是当蚂蚁聚集形成蚁群，
群内各成员之间的相互作用使得蚁群的整体行为表现出来的复杂、高效和智慧令人叹为观止。比如，修建桥梁、
跨越深沟和驾驭树叶之舟在溪流上航行。这正是涌现现象的体现：复杂的事物是从小而简单的事物中发展而来的。

我认为，在深度神经网络中，涌现现象不但存在，而且比较普遍，特别是面对复杂问题时所使用的复杂模型。
根据穆勒提出的判断涌现的三个条件 [4]_ ，我尝试给出深度神经网络中涌现的定义和判据条件。

深度神经网络中的涌现
======================

**定义(Theorem)**

**深度神经网络中的涌现**：深度学习模型是一个由大量基础神经元，按照一定的并行结构和层次结构组合而成的，
一个自适应、自组织的神经元网络系统；系统表现出来的整体性质是各个基础神经元并不具备的新的属性，也
不是所有基础神经元特性的简单叠加。

**判断依据(Proof)**

* **一个整体的涌现特征不是其部分的特征之和**。 深度学习系统内的任意一个单一神经元都不可能产生强大
  的效能，只有当一定数量的这些简单神经元，通过某种巧妙的组合方式，累积成某种精巧的结构之后，深度学习
  系统才开始具备前所未有的分类能力和特征学习能力。大量实践表明，这种整体新性质的出现，并不是源于系统
  内各部分的简单累加。
* **涌现特征的种类与组成部分特征的种类完全不同**。在深度学习系统内，系统整体表现出来的特征学习能力
  （CNN）、适应能力、可塑性（GAN [5]_ ）、联想记忆能力（LSTM [6]_ 、MemoryNN [7]_ [8]_ [9]_ ,
  NTM [10]_, DNC [12]_ ）等，远远超过了单个神经元的二元分类特性 。

* **涌现特征不能从独立考察部分的行为中推导或预测出来**。近几年来，在computer vision [13]_ [14]_ ,
  speech recognition [15]_ 和 natural language processing/understanding [16]_ 上的深度学习实践
  表明，深度学习是结构与组合的艺术(Deep learning is the art of architecture and composition.)。
  深度学习的整体涌现性（Whole Emergence）是各组成成分按照一定的结构方式，相互作用、相互补充、相互制
  约而激发出来的一种结构效应，已经远远不可能独立考察各部分行为而得出。





.. [1] Von Bertalanffy, Ludwig. "General system theory." New York 41973.1968 (1968): 40.
.. [2] Von Bertalanffy, Ludwig. "The history and status of general systems theory." Academy of Management Journal 15.4 (1972): 407-426.
.. [3] Holland, John H. Emergence: From chaos to order. OUP Oxford, 2000.
.. [4] Mill, John Stuart. A System of Logic: Ratiocinative and Inductive. Routledge, 1960.
.. [5] Goodfellow, Ian, et al. "Generative adversarial nets." Advances in neural information processing systems. 2014.
.. [6] Hochreiter, Sepp, and Jürgen Schmidhuber. "Long short-term memory." Neural computation 9.8 (1997): 1735-1780.
.. [7] Weston, Jason, Sumit Chopra, and Antoine Bordes. "Memory networks." arXiv preprint arXiv:1410.3916 (2014).
.. [8] Sukhbaatar, Sainbayar, Jason Weston, and Rob Fergus. "End-to-end memory networks." Advances in neural information processing systems. 2015.
.. [9] Kumar, Ankit, et al. "Ask me anything: Dynamic memory networks for natural language processing." CoRR, abs/1506.07285 (2015).
.. [10] Graves, Alex, Greg Wayne, and Ivo Danihelka. "Neural turing machines." arXiv preprint arXiv:1410.5401 (2014).
.. [12] Graves, Alex, et al. "Hybrid computing using a neural network with dynamic external memory." Nature 538.7626 (2016): 471-476.
.. [13] Szegedy, Christian, et al. "Rethinking the inception architecture for computer vision." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2016.
.. [14] Huang, Gao, et al. "Densely connected convolutional networks." arXiv preprint arXiv:1608.06993 (2016).
.. [15] van den Oord, Aäron, et al. "Wavenet: A generative model for raw audio." CoRR abs/1609.03499 (2016).
.. [16] Wu, Yonghui, et al. "Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation." arXiv preprint arXiv:1609.08144 (2016).


