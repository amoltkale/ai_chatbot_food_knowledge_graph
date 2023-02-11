# capstone

## Organization
Each componenent is currently structured in its own directory. This allows the needed flexibilty of having a requirements file that maintains the requirements for each componenet. This is necessary due to restrictions between arc gis requiring python 3.9.x and the ontology code requiring python 3.10.x. This also allows the flexibility of having different versions library versions needed for arcgis agaisnt other code dependencies.

* ontologies: code related to parsing ontology files (owl) and identify patterns
* arc_gis: code related to interfacing with arcgis and geolocation
* neo4j: code used to interface between python and neo4j such as running python scripts to update data on a server
* models: code related to machine learning
    * nutitrional_analysis: code related to analyzing nutitrion and ingredients
    * conversational_ai: code related to building, training, and interacting with the conversational ai

## Set up
### Python environment
There are two different python versions currently being used. Arcgis requires python 3.9.x while everything else requires python 3.10.x.

Toggling python version on Windows:
https://github.com/pyenv-win/pyenv-win

Toggling python version on Mac/Linux:
https://github.com/pyenv/pyenv

Mac note:
`brew install pyenv`
`pyenv local` and `pyenv global` doesn't quite work (at least with brew install). to correctly create a virtual environment the following command is useful:  
`~/.pyenv/versions/3.X.X/bin/python3.X -m venv <virtual_env_name>`  
where X.X = python version (ie 3.10.10). We recommended setting the virtual environment name to `venv_3.X.X`. This is already in the `.gitignore` and will be ignored.


1. Create virtual environment. See [Python environment](### Python environment) for details on toggling python version.
    * `python -m venv <environment_name>`
        * We recommended setting the virtual environment name to `venv_3.X.X`. This is already in the `.gitignore` and will be ignored.
    * Virtual environments are a handy method for swapping between python versions and different library requirements
2. Activate the virtual environment
    * `source <environment_name>/bin/activate`
3. Install requirements
    * `pip install -r requirements.txt`
4. Run code
5. To deactivate, simply run `deactivate`
