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
- Docker Engine, Docker compose
- Postman : To Test APIs

Installation guide

1. git clone <REPO URL>
2. cd RestaurantManager/
2. docker build .
3. docker-compose up
4. docker exec -it restaurantmanager_web_1 bash
6. Load fixtures :
    - python manage.py loaddata restaurantmanager/fixtures/*.json

To Run Test Cases:
``` python manage.py test ```

APIs available for following features:
- Create User
- Fetch users registered -
	  if admin : can view all users
	  others: can view only self
- Add Restaurant : Add new restaurant
- Restaurant Dashboard : Admin can view all restaurants, managers can view only thier restaurants
- Verify Restaurant : Admin can verify an published restaurant
- MenuCategory and type added by admin : offline
- Add MenuItems for restaurant : only by manager
- View Restarant details on click : menu + reviews
- Add/Edit Reviews
