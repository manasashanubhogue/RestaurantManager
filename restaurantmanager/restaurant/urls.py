from django.urls import path
from restaurantmanager.restaurant.views import (
    MenuDetailsAPI, RestaurantDetailsAPI,
    ReviewAPI, UserDetailsAPI
)

urlpatterns = [
    path('users/', view=UserDetailsAPI.as_view({'get': 'get_app_users'}), name='get_app_users'),
    path('users/create_user/', view=UserDetailsAPI.as_view({'post': 'create_user'}), name='create_new_user'),
    path('restaurants/meta_data/',view=RestaurantDetailsAPI.as_view({'get': 'restaurant_meta_data'}), name='restaurant_meta_data'),
    path('restaurants/my_dashboard/', view=RestaurantDetailsAPI.as_view({'get': 'manage_restaurant_details'}), name='manage_restaurant_details'),
    path('restaurants/<int:restaurant_id>/',view=RestaurantDetailsAPI.as_view({'get': 'get_restaurant_details'}), name='get_restaurant_details'),
    path('restaurants/add/',view=RestaurantDetailsAPI.as_view({'post': 'add_restaurant_details'}), name='create_restaurant'),
    path('restaurants/edit/<int:restaurant_id>/',view=RestaurantDetailsAPI.as_view({'post': 'edit_restaurant_details'}), name='edit_restaurant_details'),
    path('restaurants/verify/', view=RestaurantDetailsAPI.as_view({'post': 'update_restaurant_verification'}), name='update_restaurant_verification'),
    path('menu/meta_data/',view=MenuDetailsAPI.as_view({'get': 'get_menu_types'}), name='get_menu_types'),
    path('restaurants/menu/<int:restaurant_id>/',view=MenuDetailsAPI.as_view({'post': 'add_update_menu_item'}), name='add_update_menu_item'),
    path('restaurants/review/<int:restaurant_id>/',view=ReviewAPI.as_view({'post': 'add_update_review'}), name='add_update_review')
]
