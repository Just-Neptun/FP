# FP Versuch Machine Learning
This repository contains the code for the machine learning FP project. It is structured into four subtasks which can be
found in the four notebooks.

## Setup
### Set up the environment
#### uv (long term python usage recommendation)
uv is a python package manager which is simple to install and very fast you can find the installation instructions here: https://docs.astral.sh/uv/getting-started/installation/

After installing uv, open this directory in the terminal and run
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

#### Conda
If you already have conda, you can open this directory in the terminal and execute
```bash
conda env create -f environment.yaml
```

After you created your environment, set the python interpreter in VSCode to the python environment you just created.

## AI Usage
The usage of large language models (LLMs) can drastically speed up the time it takes to solve the tasks. In general, using
LLMs for help is allowed and encouraged, with the only exception being the beginning of part 1 up to 1.3.2, which should be simple
enough and hopefully instrumental. However, when using LLMs we expect you to understand 100% of the code you submit and be able to 
explain and reason about it. Your understanding will be checked during the final discussion after you finished all tasks.


## Reading Recommendations

**Pytorch**:
You will use pytorch to train a neural network. To get familiar with the package, you can read
[this pytorch introduction](https://pytorch.org/tutorials/beginner/introyt/introyt1_tutorial.html).

**K-Nearest Neighbors**: [geeks4geeks post](https://www.geeksforgeeks.org/k-nearest-neighbours/)

**PCA**: [stack exchange explanation](https://stats.stackexchange.com/questions/2691/making-sense-of-principal-component-analysis-eigenvectors-eigenvalues/140579#140579), [wikipedia](https://en.wikipedia.org/wiki/Principal_component_analysis)

**T-SNE**: [blogpost](https://medium.com/@sachinsoni600517/mastering-t-sne-t-distributed-stochastic-neighbor-embedding-0e365ee898ea)

**UMAP**: [blogpost](https://pair-code.github.io/understanding-umap/)

**Decision Trees, Random Forests, and Gradient Boosting**: 
[blogpost](https://medium.com/@brandon93.w/decision-tree-random-forest-and-xgboost-an-exploration-into-the-heart-of-machine-learning-90dc212f4948),
more details on wikipedia:

  - [decision tree wikipedia](https://en.wikipedia.org/wiki/Decision_tree_learning)
  - [random forest wikipedia](https://en.wikipedia.org/wiki/Random_forest)
  - [gradient boosting wikipedia](https://en.wikipedia.org/wiki/Gradient_boosting)

**Neural Networks**:
[visual series on neural networks](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi), 
[more detailed explanation of convolutional neural networks](https://cs231n.github.io/convolutional-networks/)
