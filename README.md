# RestaurantManager

Application to manage Restaurants, thier menu and reviews

Tech Stack used: Django, Docker

Models:
- User: Application User, 
  ie. admin-who acts as superuser, reviewe- who can view all restaurants and add reviews, manager-who is allowed to add restaurant details and update menus
- Restaurant: Details of Restaurant like address, timings,.etc
- Menu: Different types of cuisines available

Dependencies:
- python 3.9
- Docker

Installation guide

1. git clone <REPO URL>
2. docker build .
3. docker-compose up
4. docker exec -it restaurantmanager_web_1 bash
6. Load fixtures : 
  1. python manage.py loaddata fixtures/users.json
  2. python manage.py loaddata fixtures/address.json
  3. python manage.py loaddata fixtures/restaurants.json
