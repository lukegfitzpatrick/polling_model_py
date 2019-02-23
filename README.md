# polling_model_py
State space model for aggregating poll data

This is a modified version of a state space model developed for Python 2: 
https://github.com/eliflab/polling_model_py

that itself was based on an R implementation:
https://statmodeling.stat.columbia.edu/2016/08/06/state-space-poll-averaging-model/

This version makes a couple of modifications:

### 1 There's no scraping. The data is already downloaded.
### 2 The standard deviation of the random walk is now an argument. If the analyst feels that public sentiment changes more rapidly, then the parameter can be changed. A larger standard deviation of the random walk will make the true value $\mu_t$ more jumpy. 

