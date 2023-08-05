# Model of the Calvin Cycle
We share Python files with the minimal mathematical model that we are currently developing at the Insitute for Quantitative and Theoretical Biology at University of Duesseldorf. The model comprises a set of three coupled ordinary differential equations and captures the temporal evolution of 10 sugars during the carbon fixation. 

## Dependencies
All Python packages that are needed in order to run the model are listed in the file requirements.txt and can be installed by running 
	
	pip install -r requirements.txt
	
It was noticed that under some systems LSODA integrator from the scipy.odeint package is not available. This integrator is necessary for a correct computation. Please check if it is available on your system before running the model.

## Dependencies for the 'minimal' development branch
In an attempt to separate specific models from universally used kinetic modelling routines, also the 'modelbase' project needs to be installed in the python path:

    git clone git@git.hhu.de:kinetic-models/modelbase.git

(Project accessible to all HHU internal users)

To run the calvin cycle model, both modules modelbase and calvinmodel must be installed in the search path. During development the easiest is to use virtual environments.

Make a working directory where all development projects are cloned into. E.g. 

    ~/git-projects
    ~/git-projects/calvinmodel
    ~/git-projects/modelbase

Install virtualenv and virtualenvwrapper (if you haven't done so already):

    pip install virtualenv

    pip install virtualenvwrapper
    source /usr/local/bin/virtualenvwrapper.sh

Create a virtual environment with

    mkvirtualenv venv

(Replace 'venv' by the name of your virtual environment, e.g. 'models').

Now

    workon venv

will switch to the virtual environment venv.

Once in your virtual environment, add the path to the virtual environment:

    add2virtualenv ~/git-projects

Whenever you switch to your virtual environment, this path will be remembered.

See also 

    http://docs.python-guide.org/en/latest/dev/virtualenvs/
    http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#add2virtualenv

## Example
For internal debbuging information we produce a number of output on the command line. In order to avoid them, we suggest to suppress them by writing all log information to /dev/null. 

To run your first simulation where you will see the change in concentration over the time, simply type:
	
	python minimal_calvin.py >/dev/null 2>/dev/null