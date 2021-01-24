from django.urls import path
from restaurantmanager.restaurant.views import MenuDetailsAPI, RestaurantDetailsAPI, UserDetailsAPI

urlpatterns = [ 
    path('users/', view=UserDetailsAPI.as_view({'get': 'get_app_users'})),
    path('users/create_user/', view=UserDetailsAPI.as_view({'post': 'create_user'})),
    path('restaurants/meta_data/',view=RestaurantDetailsAPI.as_view({'get': 'restaurant_meta_data'})),
    path('restaurants/my_dashboard/', view=RestaurantDetailsAPI.as_view({'get': 'manage_restaurant_details'})),
    path('restaurants/<int:restaurant_id>/',view=RestaurantDetailsAPI.as_view({'get': 'get_restaurant_data'})),
    path('restaurants/add/',view=RestaurantDetailsAPI.as_view({'post': 'add_restaurant_details'})),
    path('restaurants/edit/<int:restaurant_id>/',view=RestaurantDetailsAPI.as_view({'post': 'edit_restaurant_details'})),
    path('restaurants/verify/', view=RestaurantDetailsAPI.as_view({'post': 'update_restaurant_verification'})),
    path('menu/meta_data/',view=MenuDetailsAPI.as_view({'get': 'get_menu_types'})),
    path('restaurants/menu/<int:restaurant_id>/',view=MenuDetailsAPI.as_view({'post': 'add_update_menu_item'}))
]