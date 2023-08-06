===============================================
Deep Learning: A Perspective of Systems Science
===============================================


Systems Science
===============

Systems science or systems theory [1]_ [2]_ is a fundamental science about
the **whole emergence**. Bertalanffy, the pioneer of systems science, pointed
out that we must distinguish two kinds of the whole. The one is the whole with
additivity, which does not have the emergence property and is not the system.
The other is the whole without additivity, that is, the system, which has the
emergence property. Systems science is not the science about all the whole or
all wholeness, but is the subject which only focuses on the whole without
additivity, i.e., the **whole emergence**.

Emergent phenomenon is qualitatively described as follows: The whole has some
new attributes and behavior patterns which the parts and their sum do not have,
and it is impossible to fully explain the characteristics, functions and
behaviors of the whole only according to the characteristics, functions and
behaviors of the parts. More generally speaking, the whole is greater than
the sum of the parts. Emergent phenomenon can also be quantitatively expressed
as follows: Let   be the whole of the system and consist of :math:`n` parts. Also,
let :math:`p_i` be the :math:`i`-th part, :math:`i=1,2, \cdots, n`. Then
formalize it as

.. math:: W > \sum_i^n p_i

More succinctly expressed as

.. math:: 2 > 1 + 1

Emergence in Deep Neural Networks
=================================

I believe, in deep neural networks, emergent phenomena not only exists, but
are also very common, especially in the complex models when in the face of
complex problems. According to the three conditions of Muller's judgment [4]_,
I try to give the definition and the proof of the emergence in deep neural networks.

**Theorem**

*Emergence in deep neural networks*: Deep learning model composed of
a large number of basic neurons in accordance with a certain parallel structure and
hierarchical structure is an adaptive and self-organizing system; The overall
characteristic of the whole system is a new property that the basic neurons do not
have, and it's either not a property of the simple superposition of all constituent
neurons.

**Proof**

* *Emergent features of the whole are not the sum of its parts*. Any single simple
  neuron in deep learning model cannot produce powerful performance. Deep learning
  model begins to get the unprecedented ability of classification and feature
  learning only when a certain number of these simple neurons accumulates into an
  elaborate structure by some ingenious combination. A great deal of practice shows
  that the emergence of these new properties is not due to the simple accumulation
  of all parts in the system.
* *The types of emergent features are quite different from those types of features
  in the parts*. In the deep learning model, the overall performance of the system,
  such as the capability of feature learning (CNN, etc.), adaptability, plasticity
  (GAN [5]_), associative memory (LSTM [6]_, Memory Networks [7]_ [8]_ [9]_, NTM [10]_,
  DNC [12]_, etc.) and so on, is far beyond the binary classification characteristic
  of single neuron.
* *Emergent features cannot be deduced or predicted from the behaviors of independent
  parts*. Recent years, the practice of deep learning in computer vision [13]_ [14]_,
  speech recognition [15]_ and NLP/NLU [16]_ shows, deep learning is the art of
  architecture and composition. The *whole emergence* in deep learning model with a
  certain structure is a structural effect inspired from the mutual interaction, mutual
  complementation and mutual restriction of each constituent. It has been far from being
  predicted from the behaviors of independent parts.



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


