from odoo import models, fields


class SampleType(models.Model):
    _name = "hospital.sample.type"
    _description = "Sample Type"

    name = fields.Char(string="Sample Name", required=True)
    color = fields.Char(string="Color")
