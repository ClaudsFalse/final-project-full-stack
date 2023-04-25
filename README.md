# Groove Networking 
Groove Networkig is a brand new platform pioneered by Groove Systems Productions, to allow DJs and venues to be find each other for gigs and collaborations. 

# General Specifications
## Models 
Models will include at least:
- Two classes with primary keys at at least two attributes each ✅
    - Artists {id, name, genres[],productions[at a certain venue], rate} 
    - Venues {id, name, genres[], productions[at a certain venue], rate} 
- [Optional but encouraged] One-to-many or many-to-many relationships between classes ✅

## Endpoints
Endpoints will include at least:
- Two GET requests ✅
    - GET artists 
    - GET venues
- One POST request ✅
    - add artist 
- One PATCH request ✅
    - edit artist
- One DELETE request ✅
    - delete artist

## Roles
Roles will include at least:
- Two roles with different permissions ✅
    - artist
    - venue manager
- Permissions specified for all endpoints ✅
    - artist: crud on artist
    - venue manager: crud on venues 

## Tests
Tests will include at least:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

# Project Rubric
Your project should meet all rubric requirements to pass the project. The link is provided here: [Project Rubric.](https://review.udacity.com/#!/rubrics/5091/view)