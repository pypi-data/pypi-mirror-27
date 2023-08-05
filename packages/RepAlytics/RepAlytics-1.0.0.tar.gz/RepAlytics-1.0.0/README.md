# RepAlytics-Py

This is in an effort to make connection to and from TeraData with Python as easy as possible for users.

Follow the instructions below for initial setup.

## Setup

The majority of the requirements for this project are built on top of the Anaconda distribution, since that covers the majority of packages in use for this project and future ones.

Download the Anaconda distribution for Mac or Windows, depending on your configuration.

[Anaconda](https://www.anaconda.com/download/)

Once this has been done, we need to create a virtual environment specific to the project.

### Virtual environment

Follow the steps listed on the site linked below for setting up a virtual environment. This will be the basis for which we will install the remaining packages necessary to run Python with TeraData.

[Virtual Environment](http://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

Be sure to name your environment something you will remember (like repalytics, etc). If you ever forget, you can run the conda command below to see all environments created:

`conda info --envs`

Once this has been done, we want to activate the new environment created by running the command below:

`activate yourEnvironmentName`

Once done, your command line terminal should look like the below:

`(yourEnvironmentName) C:\Users\yourUserName>`

### Installing this Repo

From here, you want to create a working directory that you will be using this distribution from and clone the repository to that folder:

`git clone https://github.com/samwood1234/RepAlytics-Py.git`

With the distribution comes a reqs.txt file. You will need to run a command to install additional packages to the new virtual environment you created.

Navigate to the directory that the repalytics-py github is located. Activate your virtual environment if you have not already done so.

Once this has been done, run the shell command:

`pip install -r reqs.txt`

This will install everything you need to get started with TeraData. Most of the requirements should already be satisfied due to the installation of the Anaconda distribution, but there are a few packages necessary to get TeraData up and running.
