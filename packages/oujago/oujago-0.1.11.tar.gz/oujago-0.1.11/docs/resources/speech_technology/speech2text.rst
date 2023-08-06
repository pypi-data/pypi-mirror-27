
===========
Speech2Text
===========



Papers
------

* [1408] `First-Pass Large Vocabulary Continuous Speech Recognition using Bi-Directional Recurrent
  DNNs <https://arxiv.org/abs/1408.2873>`_, CTC beam search.
* [1412] `Deep Speech: Scaling up end-to-end speech recognition <https://arxiv.org/abs/1412.5567>`_
* [ICML2014] `Towards End-to-End Speech Recognitionwith Recurrent Neural
  Networks <http://www.jmlr.org/proceedings/papers/v32/graves14.pdf>`_
* [1512] `Deep Speech 2: End-to-End Speech Recognition in English and
  Mandarin <https://arxiv.org/abs/1512.02595>`_,
  Chinese version is `here <http://www.leiphone.com/news/201606/Gr6RbHF4cH31SW4V.html>`_.
* [1605] `Listen, attend and spell: A neural network for large vocabulary conversational speech recognition
  <http://ieeexplore.ieee.org/abstract/document/7472621/>`_
* [1605] `End-to-End Attention-based Large Vocabulary Speech Recognition
  <http://ieeexplore.ieee.org/abstract/document/7472618/>`_
* [1609] `Advances in All-Neural Speech Recognition <https://arxiv.org/abs/1609.05935>`_

* [1612] `Very Deep Convolutional Networks for End-to-End Speech Recognition <https://arxiv.org/abs/1610.03022>`_
* [1701] `Towards End-to-End Speech Recognition with Deep Convolutional Neural
  Networks <https://arxiv.org/abs/1701.02720>`_


Codes
-----

* `Speech-to-Text-WaveNet <https://github.com/buriburisuri/speech-to-text-wavenet>`_: End-to-end sentence level English
  speech recognition based on DeepMind's WaveNet and tensorflow
* `DeepSpeech <https://github.com/mozilla/DeepSpeech>`_, A TensorFlow implementation of Baidu's DeepSpeech architecture
* `Tensorflow Speech Recognition <https://github.com/pannous/tensorflow-speech-recognition>`_, Speech recognition using
  google's tensorflow deep learning framework, sequence-to-sequence neural networks.
* `Speech Recognition with BVLC caffe <https://github.com/pannous/caffe-speech-recognition>`_, Speech Recognition with
  the caffe deep learning framework
* `deepspeech.torch <https://github.com/SeanNaren/deepspeech.torch>`_, Speech Recognition using DeepSpeech2 network and
  the CTC activation function.
* `deepspeech.pytorch <https://github.com/SeanNaren/deepspeech.pytorch>`_, Speech Recognition using DeepSpeech2 and
  the CTC activation function.
* `Automatic_Speech_Recognition <https://github.com/zzw922cn/Automatic_Speech_Recognition>`_, End-to-end automatic
  speech recognition from scratch in Tensorflow(从头实现一个端对端的自动语音识别系统).
* `kaldi-lstm <https://github.com/dophist/kaldi-lstm>`_, C++ implementation of LSTM (Long Short Term Memory), in
  Kaldi's nnet1 framework. Used for automatic speech recognition, possibly language modeling etc, the training can be
  switched between CPU and GPU(CUDA). This repo is now merged into official Kaldi codebase(Karel's setup), so this repo
  is no longer maintained, please check out the Kaldi project.
* `Attention-based Speech Recognizer <https://github.com/rizar/attention-lvcsr>`_, implementation of paper <End-to-End
  Attention-Based Large Vocabulary Speech Recognition>, based on kaldi and kaldi-python.
* `stanford-ctc <https://github.com/amaas/stanford-ctc>`_, This repository contains code for a bi-directional RNN
  training using the CTC loss function.
* `tfkaldi <https://github.com/vrenkens/tfkaldi>`_, Speech recognition software where the neural net is trained with
  TensorFlow and GMM training and decoding is done in Kaldi
* `kaldi-ctc <https://github.com/lingochamp/kaldi-ctc>`_, Connectionist Temporal Classification (CTC) Automatic Speech
  Recognition. Training and Decoding are extremely fast.
* `ctc-beam-search <https://github.com/bshillingford/ctc-beam-search>`_,  python implementation of Alex grave's
  paper "Towards End-to-End Speech Recognition with Recurrent Neural Networks",
* `ctc_beam_search_proto <https://github.com/kuke/ctc_beam_search_proto>`_



Frameworks
----------

* [c] `kaldi <https://github.com/kaldi-asr/kaldi>`_, Kaldi Speech Recognition Toolkit, http://kaldi-asr.org
* [c] `julius <https://github.com/julius-speech/julius>`_, Open-Source Large Vocabulary Continuous Speech Recognition
  Engine.
* [c] `CMU Sphinx <https://github.com/cjac/cmusphinx>`_, CMU Sphinx - Speech Recognition Toolkit.
  http://cmusphinx.sourceforge.net/
* [c++] `uSpeech <https://github.com/arjo129/uSpeech>`_, The uSpeech library provides an interface for voice recognition
  using the Arduino.
* [c++] `Aalto ASR Tools <https://github.com/aalto-speech/AaltoASR>`_, Aalto Automatic Speech Recognition tools
* [java] `Sphinx-4 Speech Recognition System <https://github.com/cmusphinx/sphinx4>`_, Sphinx-4 is a state-of-the-art,
  speaker-independent, continuous speech recognition system written entirely in the Java programming language.
* [python] `Python wrapper for CMU Sphinx-4 <https://github.com/kelvinguu/simple-speech-recognition>`_, A complete
  speech recognition system you can deploy with just a few lines of Python, built on CMU Sphinx-4.
* [python] `Dragonfly <https://github.com/t4ngo/dragonfly>`_, Dragonfly is a speech recognition framework. It is a
  Python package which offers a high-level object model and allows its users to easily write scripts, macros, and
  programs which use speech recognition.
* [python] Python wrappers for Kaldi data: `dmitriy-serdyuk <https://github.com/dmitriy-serdyuk/kaldi-python>`_,
  `janchorowski <https://github.com/janchorowski/kaldi-python>`_


Others
------

* `wer_are_we <https://github.com/syhw/wer_are_we>`_, An attempt at tracking states of the art(s) and recent results
  on speech recognition.
