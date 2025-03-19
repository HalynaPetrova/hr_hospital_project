from odoo import models, fields, api


class Person(models.AbstractModel):
    _name = "hospital.person"
    _description = "Abstract Hospital Person"
    _inherit = ["image.mixin"]

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Name", compute="_compute_full_name", store=True)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
    ], string="Gender")
    country_id = fields.Many2one("res.country", string="Country")
    city = fields.Char("City")
    address = fields.Char("Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    image_1024 = fields.Binary(string="Photo")

    _sql_constraints = [
        ("email_unique", "UNIQUE(email)", "Email must be unique!"),
        ("phone_unique", "UNIQUE(phone)", "Phone number must be unique!"),
    ]

    @api.depends("first_name", "last_name")
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}".strip()
