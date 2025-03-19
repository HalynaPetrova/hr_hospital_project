from odoo import models, fields

class Symptom(models.Model):
    _name = "hospital.symptom"
    _description = "Symptoms"

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color")
