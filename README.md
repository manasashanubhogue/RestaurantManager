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
5. python manage.py migrate

