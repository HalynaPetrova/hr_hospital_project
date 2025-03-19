from odoo import models, fields


class Disease(models.Model):
    _name = "hospital.disease.directory"
    _description = "Disease Directory"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Disease Name",
        required=True
    )
    parent_id = fields.Many2one(
        "hospital.disease.directory",
        string="Disease Type",
        ondelete="cascade"
    )
