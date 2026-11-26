from odoo import fields, models


class AssetCategory(models.Model):
    _name = "asset.master.category"
    _description = "Asset Category"
    _rec_name = "category_name"
    _order = "category_code, id"

    category_code = fields.Char(string="Category Code", required=True)
    category_name = fields.Char(string="Category Name", required=True)

    _unique_category_code = models.Constraint(
        "UNIQUE (category_code)",
        "The category code must be unique.",
    )
