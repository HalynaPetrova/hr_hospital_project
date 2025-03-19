from odoo import models, fields, api


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Hospital Patient Diagnosis"
    _rec_name = "disease_id"

    patient_id = fields.Many2one(
        "hospital.patient",
        string="Patient",
        required=True
    )
    doctor_id = fields.Many2one(
        "hospital.doctor",
        string="Doctor",
        required=True
    )
    disease_id = fields.Many2one(
        "hospital.disease.directory",
        string="Disease",
        ondelete="cascade"
    )
    disease_type = fields.Many2one(
        related="disease_id.parent_id",
        string="Disease Type",
        store=True,
        readonly=True
    )
    recommendation = fields.Text(string="Recommendation")

    @api.model
    def _set_diagnosis_date(self):
        return fields.Date.today()

    diagnosis_date = fields.Date(
        string="Diagnosis Date",
        default=_set_diagnosis_date,
        required=True
    )

    visit_id = fields.Many2one(
        "hospital.visit",
        string="Visit Information"
    )

    test_id = fields.Many2one(
        "hospital.research.category",
        string="Lab Test Name",
        ondelete="set null"
    )
    test_category = fields.Many2one(
        related="test_id.parent_id",
        string="Lab Test Category"
    )
