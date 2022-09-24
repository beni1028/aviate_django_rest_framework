# Exerice by Aviate

## The following repository consist of a Django Rest Framework app for a Job Review Application System(jars)

### AIM: 
1. TO CREATE A BACKED FOR CRUD AND LISTING OF SAID DATA (APPLICANTS). ABILITY TO BOOL AS SELECTED OR REJECT APPLICANTS.
2. LISTING SHOULD ALLOW FILTERING AND RETRIVING.
3. DOCUMENTATION VIA SWAGGER DOCS


### ASSUMPTIONS:
1. BACK-OFFICE USERS WILL BE CREATING THE APPLICATIONS FOR THE APPLICANTS WITH CRUD ABILITY
2. BACK-OFFICE USERS WILL BE SELECTING OR REJECTING APPLICANTS


### REUIRED FUNCTIONALITIES:
1. CRUD
2. FILTERING 
3. BOOL
4. SWAGGER DOCUMENTATIONS
5. PAGINATION ON FILTERING


### OTHER FUNCTINALITIES
1. APPLICANT UID TO BE CREATED VIA SIGNAL ON CREATION OF APPLCANT
2. APP BOOL TO BE AUTO UPDATED AS APPLICANT ENUM STATUS IS UPDATED
3. EMAIL SMTP AVAILABLE BUT REDUCED TO CONSOLE LOGGING
4. LIMIT OFFSET PAGINATION GLOBALLY

### MODELS
1. USER MODEL (CUSTOM USER MODEL)
2. APPLICANT MODEL

### ADDTIONAL REQUIREMENTS
1. DOCKER

### HOW TO RECREATE
1. CLONE REPO 
2. FOR WINDOWS
    - START DOCKER DESKTOP
3. FOR LINUX 
    - sudo systemctl start docker
    OR
    - sudo service docker start
4. OPEN CLI IN WORKING DIRECTORY AND ENTER COMMANDS AS FOLLOWS:
    - docker-compose -f ./docker-compose.yml up
5. OPEN SECOND CLI 
    - docker-compose run app python manage.py makemigrations
    - docker-compose run app python manage.py migrate
    - docker-compose run app python manage.py createsuperuser

### FINAL APIs
1. Create
    - /api/applicant/create/
    - Post Request
2. Read-Update-Delete
    - /api/applicant/profile/
    - Get, Patch, Put and Delete
3. Update Applicant Status
    - /api/applicant/app_status/
    - Get, Patch and Put
4. Search
    - /api/applicant/search/
    - Get Request
    - Page Number Pagination
5. Swagger
    - /swagger/schema/
    - /redoc/schema/

### OTHER APIs
1. Invidual Applicant Details
    - /api/applicant/detail/
    - /api/applicant/detail/v2/
    - Get methods with differnt implementations

2. Search
    - /api/applicant/search/custom/
    - Post Request
    - Different Implementation

3. Update
    - /api/applicant/update/
    - Get, Put and Patch

4. Delete
    - /api/applicant/delete/
    - Get and Delete 


    



