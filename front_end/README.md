# Nourish User Interface
The Nourish application interface is being developed in JavaScriptand React. It provides a platform for new and aspiring business owners who aim to start a food service business in a specific geographical area. The application tackles the complexity of starting a business by providing assistance and generating conversations using Chat GPT.

## Features

### User Registration
Users can create an account and log in to access the system’s features securely (authentication policies and procedures will be established by responsible parties at UCSD).

### Database Integration
The application is integrated with a Postgres database to store user information, business profile information, geographical data and other relevant data.

## Technologies Used
The following technologies and frameworks were used to develop the Nourish application interface:  
* JavaScript
* React
* Postgres (database)
* HTML/CSS (for user interface design)
* Node.js (for server-side development)
* Express.js (server framework)

## Getting Started
1. Install the required dependencies (DEV environment).
2. Set up the Postgres database and configure the connection details in the application’s  configuration file.
3. Create a `.env` file under the nourish_server directory and add a line to enter your connection string information.
    * Ex: `DB_URI=postgres://username:password@hostname:5342/dbname`

### Nourish UI - React
1. Run `npm i` from the terminal to install all the required packages.
2. Run `npm start` from the terminal.

### Nourish Server
1. Run `npm i` from the terminal to install all the required packages.
2. Run `npm dev` from the terminal in a development environment

### Install the required dependencies (PROD environment)

1. Inside of the nourish_interface directory run `NPM run build` from the terminal.
2. Inside of the nourish_server directory run `npm start`
3. Access the application in your web browser at http://localhost:3000

## File Structure
The project’s file structure is organized as follows:  

```bash
├── src
│   ├── components
│   │   ├── SignUp.js
│   │   ├── Splash.js
│   │   ├── BooleanInput.js
│   │   ├── ChatBox.js
│   │   ├── ChecklistInput.js
│   │   ├── ListInput.js
│   │   ├── EmailInput.js
│   │   ├── Help.js
│   │   ├── NumberInput.js
│   │   ├── PhoneInput.js
│   │   ├── SelectInput.js
│   │   ├── TextInput.js
│   │   ├── SignUp.module.css
│   │   ├── Splash.module.css
│   │   └── general.module.css
│   ├── App.js
├── public
│   ├── index.html
├── package.json
└── nodeServer.js

```  

### Description
* `src`: Contains the application source code.
    * `components`: Contains React components responsible for rendering the user interface. 
        `SignUp.js`: component that handles the registration form.
        * `Slpash.js`: Home page.
        * `BooleanInput.js`:  Contains functions applied to boolean fields.
        * `ChatBox.js`:  Contains placeholders that will be used for the AI integration.
        * `ChecklistInput:`  Contains functions applied to  array fields.
        * `ListInput.js`:  Contains functions applied to list input fields.
        * `EmailInput.js`:  Contains functions applied to email fields.
        * `Help.js`: Future use for the help module.
        * `NumberInput.js`:  Contains functions applied to numeric fields.
        * `PhoneInput.js`:  Contains functions applied to phone number fields.
        * `SelectInput.js`: Contains functions applied to select input fields.
        * `TextInput.js`: Contains functions applied to text input fields.
        * `SignUp.module.css`: Component that handles styling for the Signup page.
        * `Splash.module.css`: Component that handles styling for the home page (Splash.js).
        * `general.module.css`: Component that handles general styling for columns.
* `App.js`: The main React component that serves as the entry point of the application.
* `public`: Contains the static files and the index.html file, which is the main HTML template for the application.
* `package.json`: Defines project dependencies, scripts, and metadata.
* `nodeServer.js`: The Node.js server file that interacts with the Postgres database.

## Database Schema

| Column Name                      | Data                | Type                | Format                 | Description                                           |
|:----------------------------------:|:---------------------:|:---------------------:|:------------------------:|:-------------------------------------------------------:|
| id                               | bigserial           | 999                 | Primary key and unique | Identifier for each user                              |
| first_name                       | text not null       |                     |                        | First name                                            |
| last_name                        | text not null       |                     |                        | Last name                                             |
| middle_name                      | varchar(30)         |                     |                        | Middle name                                           |
| email                            | text []             | {jane.doe@email.com, john.smith@email.com} | Array     | Accepts multiple values                               |
| phone                            | text []             | 99999999            | Array                  | Accepts multiple values                               |
| gender                           | text                |                     |                        |                                                      |
| ethnicity                        | text []             |                     | Array                  | Accepts multiple values                               |
| languages_spoken                 | text []             |                     | Array                  | Accepts multiple values                               |
| languages_written                | text []             |                     | Array                  | Accepts multiple values                               |
| extending_existing_business      | boolean             |                     |                        | Is the user extending an existing business            |
| customer_regions_by_neighborhoods| text []             |                     | Array                  | Accepts multiple values                               |
| current_business_description     | text                |                     |                        | Description of current business                       |
| prospective_business_description | text                |                     |                        | Description of prospective business                   |
| nominal_current_revenue          | numeric             | 9999                |                        | Current business revenue                              |
| desired_funding                  | numeric             | 9999                |                        | Amount of funding desired                             |
| business_role                    | text                |                     |                        | Current role of business owner                        |
| how_many_years_in_current_business| numeric             | 99                  |                        | Number of years in business                           |
| additional_comments              | text                |                     |                        | Comments                                              |
| uuid                             | varchar(32)         | 368addfbe8524b00bfe0bf0c5427ac01 | Unique id generated from the application |       |
| is_veteran                       | boolean             | true or false       |                        | Identifies if user is a veteran                       |
| insert_dts                       | timestamp default now() | 2022-10-01 hh:mm:ss |                        | Date and time of record creation                      |
| update_dts                       | timestamp           | 2022-10-01 hh:mm:ss |                        | Modification of record date and time                  |
| home_city                        | text                |                     |                        |                                                      |
| home_state                       | text                |                     |                        |                                                      |
| home_zip                         | text                |                     |                        |                                                      |
| biz_city                         | text []             |                     | Array                  | Accepts multiple values                               |
| biz_state                        | text                |                     |                        | Business state                                        |
| biz_zip                          | text []             |                     | Array                  | Accepts multiple values                               |
| home_street_address              | text                |                     |                        |                                                      |
| biz_street_address               | text                |                     |                        |                                                      |
| planned_fund_use                 | text                |                     |                        | Planned use of desired funds                          |
