# Groove Networking 
Groove Networkig is a brand new platform pioneered by Groove Systems Productions, to allow DJs and venues to be find each other for gigs and collaborations. 

# General Specifications
## Models 
Models will include at least:
- Two classes with primary keys at at least two attributes each ✅
    - Artists {id, name, genres[],productions[at a certain venue], rate} 
    - Venues {id, name, genres[], productions[at a certain venue], rate} 
    - gigs 
- [Optional but encouraged] One-to-many or many-to-many relationships between classes ✅

## Endpoints
Endpoints will include at least:
- Two GET requests:
    - GET artists 
    - GET venues
    - GET gigs ✅
- One POST request ✅
    - post gig ✅
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


'''
How to use 
There are two roles that can be used to login:
- Artist login: artist@groove.com - password: Artistlogin2023
- Venue manager login: venue-manager@groove.com - password: Managerlogin2023
''''''
How to use 
There are two roles that can be used to login:
- Artist login: artist@groove.com - password: Artistlogin2023
- Venue manager login: venue-manager@groove.com - password: Managerlogin2023
'''