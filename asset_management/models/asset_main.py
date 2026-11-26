from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ITAsset(models.Model):
    _name = "asset.master.main"
    _description = "Asset Main CRUD"
    _rec_name = "asset_name"
    _order = "asset_code, id"

    asset_code = fields.Char(string="Asset Code", required=True)
    asset_name = fields.Char(string="Asset Name", required=True)
    asset_category = fields.Many2one('asset.master.category', string="Asset Category", required=True)
    total_quantity = fields.Integer(string="Total Quantity", required=True)
    borrowing_ids = fields.One2many(
        'asset.master.borrow',
        'borrowed_asset_name',
        string="Borrowings",
    )
    available_quantity = fields.Integer(
        string="Available Quantity",
        compute="_compute_available_quantity",
        store=True,
    )

    ## Getting borrowed quantity
    def _get_borrowed_quantity(self):

        ## Ensuring 'self' only has one record
        self.ensure_one()

        ## Initialize borrowed quantity with 0
        borrowed_quantity = 0

        ## Iterate through all borrowing records attached to the asset
        for borrowing in self.borrowing_ids:

            ## Only process records with asset_borrowing_status = 'borrowed'
            if borrowing.asset_borrowing_status == 'borrowed':

                ## Add borrowing_quantity from the current borrowing record
                borrowed_quantity += borrowing.borrowing_quantity

        ## Return the total borrowed quantity
        return borrowed_quantity

    ## Telling the system that a computed field depeneds on fields listed
    @api.depends(
        'total_quantity',
        'borrowing_ids.borrowing_quantity',
        'borrowing_ids.asset_borrowing_status',
    )

    ## Counting available asset
    def _compute_available_quantity(self):
        ## Counting assets separately
        for asset in self:
            asset.available_quantity = (asset.total_quantity - asset._get_borrowed_quantity())


    @api.constrains('total_quantity') ## Validating when 'total_quantity' is being updated or set through relevant ORM operation
    def _check_total_quantity(self):

        ## Temporarily storing all 'asset' records found in 'self' on variable "asset"
        for asset in self:

            ## Checking whether the value of total quantity is less than the quantity assets borrowed
            if asset.total_quantity < asset._get_borrowed_quantity():

                # Raise alerts user of the error they made
                raise ValidationError("Total quantity cannot be less than the quantity currently borrowed.")

    _unique_category_code = models.Constraint(
        "UNIQUE (asset_code)",
        "The asset code must be unique.",
    )
