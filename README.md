# Nourish Knowledge Graph Analysis Capstone
The repository is composed of a variety of scripts used to create the knowledge graph and integrate the knowledge graph with a LLM. On top of the integration, there is also code for a front facing website for users to log in to as well as a front end for the chat application. Please see below for more details on each directory and their contents.

1. Arcgis
    * Location: `arc_gis`
    * README: `arc_gis/README.md`
    * Description: Code used to create spatial feature layers, EDA, and querying as well as geoenrichement code.
2. Chatbot
    * Location: `chatbot_apps`
    * README: `README.md`
    * Description: Tools used to interface with Openai and knowledge graph. Code for the front facing chat application is also located here and is called `nourish_chatbot_app.py`
3. Front End
    * Location: `front_end`
    * README: `front_end/README.md`
    * Description: Frontend javascript that creates the login for users and queries them for information
4. Models
    * LocationL `models`
    * README: There is not a readme for the one off clustering
    * Description: Scripts used to cluster food products by nutitrion and to calculate HPF scores
5. Neo4j
    * Location: `neo4j`
    * README: None, this was preliminary EDA
    * Description: Initial eda code to connect to neo4j server and directly update server
6. Ontologies
    * Location: `ontologies`
    * README: `ontologies/README.md`
    * Description: Code used to convert owl files into neo4j ready csv files

However, this README will focus on the main product: the chatbot application.

## Requirements and Set up
The chatbot application requires `Python 3.9.X` in order to run all the tools due to Arcgis Online. **It is important to note that the langchain version is very important and that slight changes in the version of that package will greatly influence the ability to run this application.**

### Data Sources and Keys
All of the log ins are managed by the `config.ini`. It is important that you provide all the log in information in order for the application to properly query information. You can create your own instances of the databases as well. Please see the `ontologies/README.md` for more details on how to create the neo4j database.

If you would like to directly connect to Nourish, you will need to contact Dr. Amarnath Gupta at UCSD to request permission.

1. `cp template_config.ini config.ini`
2. Provide the following details:
    * Openai key (needed for LLM engine)
    * Google cloud api key (needed to create document indexes and to query google drive folders)
        * [Please see Langchain's docs for more details](https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/google_drive.html)
        * The document indexes used in the demo are actually in the `arcgis/resources/`
        * These keys are only needed if you want to create new document indexes for LLM to use
            * If you run `python chatbot_apps/index_creation.py` and update the google drive folders in the file, it will automatically update the index files in `arcgis/resources/`
            * Currently only the SBA indexes are being used
    * Arcgis Online account info to pull feature layers and maps
        * [UCSD ArcGIS Online](https://ucsdonline.maps.arcgis.com/)
        * Nourish Project Resource Group - [project_nourish_public](https://arcg.is/1nSziL0)
    * Nourish database, particularly the tables below are used:
        * [Branded Foods and nutrition 10/2022](https://fdc.nal.usda.gov/download-datasets.html)
        * A table made from running [Lexmapr](https://github.com/cidgoh/LexMapr) to map branded foods to Foodon ontology
        * HPF clustering results on branded fooded
        * registrants table with user info
    * Neo4j database
        * This can be directly made from running the code in `ontologies` to convert the Foodon Owl file into a neo4j ready database

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

### Running the application
Once you have given all the required keys to access the knowledge graph, you are ready to run the application.

1. `python chatbot_apps/nourish_chatbot_app.py`
2. Navigate to `127.0.0.1:8050/`
3. Have a conversation!
