from import_export import resources, fields, widgets
from restaurantmanager.restaurant.models import MenuItem, MenuItemType, Menu, Restaurant

class MenuItemResource(resources.ModelResource):
    name = fields.Field(column_name='Name', attribute='name')
    menu_item_type = fields.Field(column_name='Menu Item Type', attribute='menu_item_type',
                               widget=widgets.ForeignKeyWidget(MenuItemType, 'name'))
    menu = fields.Field(column_name='Menu', attribute='menu',
                               widget=widgets.ForeignKeyWidget(Menu, 'name'))
    restaurant = fields.Field(column_name='Restaurant', attribute='restaurant',
                               widget=widgets.ForeignKeyWidget(Restaurant, 'name'))
    description = fields.Field(column_name='Description', attribute='description')
    price = fields.Field(column_name='Price', attribute='price')
    type = fields.Field(column_name='Cuisine Type', attribute='type')

    class Meta:
        model = MenuItem

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # for row in dataset:
        # add validations
        pass
