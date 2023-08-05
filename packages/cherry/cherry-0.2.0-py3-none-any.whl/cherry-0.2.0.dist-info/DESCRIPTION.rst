cherry
=======================
.. image:: https://api.travis-ci.org/Sunkist-Cherry/cherry.png?branch=master
    :target: https://travis-ci.org/repositories/Sunkist-Cherry/cherry

.. image:: https://img.shields.io/pypi/v/cherry.svg
    :target: https://pypi.python.org/pypi/cherry

.. image:: https://img.shields.io/pypi/l/cherry.svg
    :target: https://pypi.python.org/pypi/cherry

.. image:: https://img.shields.io/pypi/pyversions/cherry.svg
    :target: https://pypi.python.org/pypi/cherry


:Version: 0.1.8
:Download: https://pypi.python.org/pypi/cherry/
:Source: https://github.com/Sunkist-Cherry/cherry
:Support: >=Python3.4
:Keywords: spam, filter, python, native, bayes

.. _`中文版本`:
这个项目目的是使用机器学习／人工智能来进行数据分类

例子1中的应用是判别垃圾内容，现阶段用户输入句子会先经过分词，然后通过朴素贝叶斯模型判别成正常，色情，赌博，政治敏感四个类别。现在每个类别各使用了100个训练数据，辨别准确率大约为93%。（数据內容请勿分發，传阅，出售，出租给他人）

特点
----
- 开箱即用，快速上手

  内置预训练模型以及文件缓存，开箱即用。同时使用numpy库做矩阵计算，判断速度非常快
- 准确率高

  现阶段使用了400个训练数据，准确率达到93%。下载后可以通过运行

  .. code-block:: bash

    python -m unittest tests.test_bayes

  得到准确率测试结果

  .. code-block:: bash

    This may takes some time
    Completed 0 tasks, 20 tasks left.
    Completed 5 tasks, 15 tasks left.
    Completed 10 tasks, 10 tasks left.
    Completed 15 tasks, 5 tasks left.
    The error rate is 6.83%

    测试20次，每次从数据集随机取出20个数据作为测试数据，剩下的作为训练数据。然后计算平均错误率

- 可定制

  自己可以添加修改数据源，增加训练正确率

通过pip安装：
-----------

.. code-block:: bash

   pip install cherry

基本使用:
--------

.. code-block:: python

    >>> from classify import bayes
    >>> test_bayes = bayes.Classify()
    >>> test_bayes.bayes_classify('选择轮盘游戏随机赔率，高达119倍。')
    Building prefix dict from the default dictionary ...
    Loading model from cache /var/folders/md/0251yy51045d6nknpkbn6dc80000gn/T/jieba.cache
    Loading model cost 0.969 seconds.
    Prefix dict has been built succesfully.
    (1, [-52.665796469015774, -41.781387161169008, -53.513237457719043, -56.71342538342271])

这里使用了内置的训练模型缓存，如果你修改了数据源的话，需要更新缓存

.. code-block:: python

    >>> from classify import bayes
    >>> test_bayes = bayes.Filter(cache=False) # 缓存文件被更新
    >>> test_bayes = bayes.Filter() # 将使用新数据源的缓存


我们一开始使用了 `jieba`_ 进行分词，上面的0.969秒是分词的时间（感谢fxsjy维护如此优秀的中文分词库）。返回了一个tuple，包含bayes判断结果的类别1（所对应的是赌博），以及对应的所有类别的相对概率，现在支持的类别有四个，用户可以自行添加数据然后进行训练

.. _`jieba`: https://github.com/fxsjy/jieba

- NORMAL = 0
- GAMBLE = 1
- SEX = 2
- POLITICE = 3


未来功能
-----

- 添加英文句子分类功能
- 繁体字转换成简体字再训练
- 把中文分词库分离，让用户可以自己选择分词方式
- 对长文本增加tf-idf计算词权重
- 增加SVM分类算法


.. _`english-version`:
This project uses Native Bayes algorithm to detect spam content, like normal, sex, gamble, political content. We use 400 Chinese sentences to train the algorithm and the correct rate is about 93%. Right now we only support Chinese spam content classify :<

How to use:

.. code-block:: python

    >>> from classify import bayes
    >>> test_bayes = bayes.Classify()
    >>> test_bayes.bayes_classify('选择轮盘游戏随机赔率，高达119倍。')
    Building prefix dict from the default dictionary ...
    Loading model from cache /var/folders/md/0251yy51045d6nknpkbn6dc80000gn/T/jieba.cache
    Loading model cost 0.969 seconds.
    Prefix dict has been built succesfully.
    (1, [-52.665796469015774, -41.781387161169008, -53.513237457719043, -56.71342538342271])

- NORMAL = 0
- GAMBLE = 1
- SEX = 2
- POLITICE = 3


