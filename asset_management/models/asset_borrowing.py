from odoo import api, fields, models
from odoo.exceptions import ValidationError

def _default_user(self):
    return self.env.user

class AssetBorrowing(models.Model):
    _name = "asset.master.borrow"
    _description = "Asset Borrowing"
    _rec_name = "borrowing_id"
    _order = "borrowing_id, id"

    borrowing_id = fields.Char(string="Borrowing ID", required=True)
    borrowed_asset_name = fields.Many2one('asset.master.main', string="Asset Name", required=True)
    borrower_employee_name = fields.Many2one('res.users', string='Borrower', default=_default_user)
    borrowing_quantity =  fields.Integer(string="quantity", required=True)
    borrowed_at = fields.Date(string="Borrow Date", required=True, default=fields.Date.context_today)
    returned_at = fields.Date(string="Return Date")
    asset_borrowing_status = fields.Selection(selection=[('returned', 'Returned'),('borrowed', 'Borrowed'),], 
                                              string='Borrowing Status', 
                                              default='borrowed')

    _unique_category_code = models.Constraint(
        "UNIQUE (borrowing_id)",
        "The asset code must be unique.",
    )

    @api.constrains(
        'borrowed_asset_name',
        'borrowing_quantity',
        'asset_borrowing_status',
    )
    ## Checking available quantity
    def _check_borrowing_quantity(self):
        for borrowing in self:

            ## If the proposed quantity is below zero, raise will alert the user
            if borrowing.borrowing_quantity <= 0:
                raise ValidationError("Borrowing quantity must be greater than zero.")

            ## Skips any data with asset_borrowing_status that do not have value = borrowed.
            if borrowing.asset_borrowing_status != 'borrowed':
                continue

            ## Variable named asset is taking data of the name for the asset 
            asset = borrowing.borrowed_asset_name

            ## Sum the data according to the statement
            borrowed_quantity = sum(
                record.borrowing_quantity
                ## Taking all borrowing IDs attached to asset name take by variable 'asset'
                for record in asset.borrowing_ids
                ## filtering asset_borrowing_status to only value = borrowed
                if record.asset_borrowing_status == 'borrowed'
            )

            ## If borrowed quantity is more than total quantity, raise will alert the user.
            if borrowed_quantity > asset.total_quantity:
                raise ValidationError("Borrowing quantity exceeds the asset's available quantity.")

    ## Logic for return button
    def return_asset(self):
        for record in self:

            ## Skip if asset_borrowing_status is already = returned
            if record.asset_borrowing_status == 'returned':
                continue

            ## Write update status to 'returned' and fill the return date
            record.write({
                'asset_borrowing_status': 'returned',
                'returned_at': fields.Date.context_today(record),
            })