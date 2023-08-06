=================================================================
深度学习：从定性的思考到定量的研究
=================================================================
.. Deep Learning: From qualitative thinking to quantitative research

目前，学术界对于深度学习的研究表现出一种倾向，就是，大家已经不仅仅是限于对深度学习工程
优越性的陶醉了。已有一大批研究者真正地想弄清楚深度学习为什么如此有效。已有的研究的切入
点主要如下：

* Achievable functions [1]_ [2]_ [3]_ 。任意函数的逼近性。试图论证深度学习或者神经网
  络能逼近任意一类函数。
* Expressivity [4]_ [5]_ 。表现力。试图论证是什么使深度学习模型有效。是width？depth？
  还是connectivity？更或者是一个新的维度，trajectory length？
* Geometry representation [6]_ [7]_ 。数学框架。这两个工作都是滑铁卢大学的一个数学教授
  和他的一个学生做的。他们试图自己建立一个数学框架来表示（不是解释）深度学习。

.. 这些东西我也看不懂，我也不知道我的上述理解是不是对的。反正论文只看了点皮毛。

这样的定量的研究是有必要的，尽管可能无疾而终。马克思说，**一种科学只有当它达到了能够运用
数学时，才算真正发展了**。借鉴这句话，我们可以说，深度学习，只有真正尝试着去数学论证了，
才有可能弄得懂，才可能真正有学术发展价值，而不仅仅是工程价值。另外，马克思主义哲学也说明
了，定量与定性是辩证统一的。在我们没有对事物进行定量研究，弄清其数量关系，找到决定其质量
的数量界限以前，我们对事物的性质还只能使初步的、粗略的认识。

下面，我想结合着我目前对于深度学习的理解，试图给出**一个定量研究的切入方向**。

首先，深度学习网络实质是一个复杂系统。它是大量相同性质的简单模型的聚合。首先是层内的聚合。
比如，CNN在每一层的卷积中有多个相同的filter，数量一般为32, 64, 128等，RNN的每层也有多
个time step，每个time step进行一模一样的操作，time step大小同样一般为32, 64等。（补充说
明一下：个人认为这种数量的限制并不是因为深度学习的什么本质属性导致的，而是我们的技术手段所
致。比如，对于RNN来说，如果time step超过64，太长了，梯度消失、暴涨现象就太严重了，无法有
效训练。）其次是层间的聚合。GoogleNet [10]_ 、VGG Net [8]_ 、Residual Net [9]_ 等，每
一层可能都是相同的，然后，相同的层通过一定数量累计在一起。最后，这种层间与层内的多个相同简
单模型聚合在一起，通过自组织，协同训练。然后深度学习网络便可能开始产生新的特征。

我们可以注意到，任何一个单一的模型都不可能产生如此强大的效果。而只有当一定数量的这些简单
模型，累积到一定程度，才产生了威力。另外，目前深度学习的实践普遍表明，层数的增加对任务的
进行有很大的帮助。这其实充分说明一点，目前的深度学习网络系统，一度程度上，系统越复杂，引
入的子系统越多，效果越好。

因此，我们可以认为，深度学习系统是一个自组织系统，是一个无序到有序的的不断演化的协同系统。
所以，我们是否可以从**协同学、耗散结构理论**等方面入手，对深度学习的一些性质进行论证。

``2016-12-12``


.. [1] Hornik, Kurt, Maxwell Stinchcombe, and Halbert White. "Multilayer feedforward networks are universal approximators." Neural networks 2.5 (1989): 359-366.
.. [2] Cybenko, George. "Approximation by superpositions of a sigmoidal function." Mathematics of Control, Signals, and Systems (MCSS) 2.4 (1989): 303-314.
.. [3] Eldan, Ronen, and Ohad Shamir. "The power of depth for feedforward neural networks." Conference on Learning Theory. 2016.
.. [4] Poole, Ben, et al. "Exponential expressivity in deep neural networks through transient chaos." Advances In Neural Information Processing Systems. 2016.
.. [5] Raghu, Maithra, et al. "On the expressive power of deep neural networks." arXiv preprint arXiv:1606.05336 (2016).
.. [6] Anthony L. Caterini and Dong Eui Chang. A Novel Representation of Neural Networks. CoRR, 2016 abs/1610.01549
.. [7] Caterini, Anthony L., and Dong Eui Chang. "A Geometric Framework for Convolutional Neural Networks." arXiv preprint arXiv:1608.04374 (2016).

.. [8] Simonyan, Karen, and Andrew Zisserman. "Very deep convolutional networks
        for large-scale image recognition." arXiv preprint arXiv:1409.1556 (2014).
.. [9] He, Kaiming, et al. "Deep residual learning for image recognition."
        Proceedings of the IEEE Conference on Computer Vision and Pattern
        Recognition. 2016.
.. [10] Szegedy, Christian, et al. "Rethinking the inception architecture for
        computer vision." Proceedings of the IEEE Conference on Computer Vision
        and Pattern Recognition. 2016.
