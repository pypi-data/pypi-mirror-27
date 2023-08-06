# SG Markets API Plot Helper

TBD

## 1- Introduction

This repo is meant to make it easy for clients (and employees) to tap SG Research APIs.  

This is a work in progress and subject to rapid changes.  
In particular only a few endpoints of the [Rates Option Trade Builder V1 API](https://analytics-api.sgmarkets.com/rotb/swagger/ui/index) are covered.  

The usual way to expose an API is to make a [swagger](https://swagger.io/) available and also a GUI, typically a web page.  
These have the following drawbacks:
+ A swagger is as precise as it is dull. Unless clients are (working with) IT savvy people they will have a hard time taking advantage of it. In short it is not enough. 
+ A GUI is easy to use but often as much a help as a hindrance: They are very slow/costly to build/adapt, are seldom as flexible as the underlying API, and are no help for industrial use of the API.  

To fill the gap, we introduce the [Jupyter](http://jupyter.org/) notebook as an **API consumption tool** (It as many other uses).  
The associated Python package used here has a very simple API, but can be arbitrarily modified for (and by) the advanced user. It has the same display capabilities as a web page (being one itself). Most importantly is is written in Python so can be evolved by a business user (as opposed to web front end which is invariably delegated to specialist developpers).


This repo contains:
+ ready-to-use sample notebooks
    + [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/sg-research-api-helper/raw/master/demo_sg_research_api_helper.ipynb)
+ the underlying library in folder [sg_research_api_helper](https://gitlab.com/oscar6echo/sg-research-api-helper/tree/master/sg_research_api_helper)

Here, the notebook is a convenient and versatile interface to
+ hide the plumbing
    + going through the corporate proxy
    + getting the SG API access token (Auth v1.0)
+ make API calls explicit and readable
+ analyse the API response
+ slice and display the results as tables and graphs - and save them


## 2 - Install

Two options:

### 2.1 - git clone the repo

From terminal:
```bash
# download repo
git clone https://gitlab.com/oscar6echo/sg-research-api-helper.git

# move into repo directory
cd sg-research-api-helper

# launch notebook
jupyter notebook
```
Open a sample notebook and modify it to your own use case.

### 2.2 - pip install (coming soon)

From terminal:
```bash
# download and install package from pypi.org
pip install sg_research_api_helper

# launch notebook
jupyter notebook
```
Create a notebook or download a sample notebook and modify it to your own use case.


## 3 - User guide

Read the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/sg-research-api-helper/raw/master/demo_sg_research_api_helper.ipynb).

The key steps are the following.

### 3.1 - Define you credentials

Create a file `my_secret.txt` (or pick the name) in your home directory.  
+ On Windows: `C:\Users\youraccountsname`.
+ On Linux/macOS: `~/youraccountsname`.

This file must contain your secrets in the following format:
```
SG_LOGIN=myownsglogin
SG_PASSWORD=myownsgpassword

PROXY_LOGIN=myownproxylogin
PROXY_PASSWORD=myownsproxypassword

PROXY_HOST=myownproxyhost
PROXY_PORT=myownproxyport
```

Pass this file name as argument to the Api object.

```python
from sg_research_api_helper.api import Api
# default name is 'my_secret.txt'
a = Api()

# default name is 'my_secret.txt'
a = Api(path_secret='my_custom_secret.txt')

# to see the logs
a = Api(verbose=True)
```

### 3.2 - Pick an endpoint

Select it from the list of those available in the package.  

```python
from sg_research_api_helper.api import ENDPOINTS
# Examples
ep = ENDPOINTS.v1_curves
ep = ENDPOINTS.v1_compute_strategy_components
```

### 3.3 - Create the associated request

Each end point comes with a `Request` object.  

```python
# For all endpoints
rq = ep.request()
```

And fill the object with the necessary data.  
This part is specific to the endpoint selected.  
See the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/sg-research-api-helper/raw/master/demo_sg_research_api_helper.ipynb) for examples.  

Then explore your `Request` object to make sure it is properly set.
```python
# For all endpoints
# display the structure of the object
rq.info()
```

> **IMPORTANT**:  
> You should make sure the request will not overload the server. If not the API call may time out.  
> To this effect the `Request` object will display information, warnings and recommendations.  


### 3.4 - Call the API

You can call the API directly from the `Request` object.  

```python
# For all endpoints
res = rq.call_api(a)
```

The returned object is a `Response` object associated to this endpoint.  
You can explore it starting with

```python
# For all endpoints
# display the structure of the object
res.info()
```

### 3.5 - Save and show the results

As `.csv` and `.xlsx` files.

```python
# For all endpoints
# save to disk
res.save_result(excel=True)
```

The `Response` objects are different for each endpoint.  
See the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/sg-research-api-helper/raw/master/demo_sg_research_api_helper.ipynb) for examples.  


### 3.6 - Slice the results

For those endpoints which return a large amount of data, slicing the result is usually the best/only way to exploit the results.  
Then use the associated `Slice` results down to a 1-D or 2-D or 3-D dataframe.  

```python
# example - see demo notebook for the context
dic_req_fix = {'date': pd.Timestamp('2016-11-11')}
s1 = ep.slice(res, x='expiry', y='tenor', dic_req_fix=dic_req_fix, value='volNormal')

# display the structure of the object
s1.info()

# save to disk
s1.save()
```

### 3.7 - Plot a slice

Finally you can display a 1-D or 2-D slice with a number of plot functions.  


```python
# examples - see demo notebook for the context

# line(s) plot
Plot.line(s1.df_pivot, figsize=(14, 6), title='Slice 1')

# heatmap
Plot.heatmap(s1.df_pivot, title='Slice 1', cmap='YlGnBu', figsize=(8, 8))

# surface
Plot.surface3D(s1.df_pivot, z_label='volNormal', z_round=4)

# dynamic chart with dates on x axis
Plot.highstock(s4.df_pivot, title='volNormal')
```
