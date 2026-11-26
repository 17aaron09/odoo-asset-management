{
    "name": "Asset Management",
    "summary": "Maintain asset, asset categories, borrowings",
    "version": "20.0.1.0.0",
    "category": "Operations",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
	    "security/asset_management_groups.xml",
        "security/ir.access.csv",
        "views/asset_main_views.xml",
        "views/asset_category_views.xml",
        "views/asset_borrowing_views.xml",
        "views/asset_management_menus.xml",
    ],
    "application": True,
    "installable": True,
}
