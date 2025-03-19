from odoo import models, fields, api
from odoo.exceptions import UserError


class Doctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["hospital.person"]
    _description = "Hospital Doctor"
    _rec_name = "full_name"

    speciality_id = fields.Many2one(
        "hospital.doctor.speciality",
        string="Speciality"
    )
    experience = fields.Integer(string="Experience")
    education = fields.Char(string="Education")
    certificates = fields.Text(string="Certificates and Achievements")
    patient_ids = fields.One2many(
        "hospital.patient",
        "doctor_id",
        string="Patients"
    )
    is_intern = fields.Boolean(string="Intern", default=False)
    mentor_id = fields.Many2one(
        "hospital.doctor",
        string="Mentor",
        domain=[("is_intern", "!=", "False")],
        help="Doctor who mentors the intern."
    )
    schedule_ids = fields.One2many(
        "hospital.schedule",
        "doctor_id",
        string="Doctor's Schedule"
    )
    visit_ids = fields.One2many(
        "hospital.visit",
        "doctor_id",
        string="Visits"
    )
    working_hours = fields.Char(
        string="Working Hours",
        default="08:00 - 18:00"
    )
    available_days = fields.Char(
        string="Available Days",
        default="Mon-Fri"
    )
    patient_count = fields.Integer(
        string="Patient Count",
        compute="_compute_patient_count"
    )

    @api.depends("patient_ids")
    def _compute_patient_count(self):
        for rec in self:
            rec.patient_count = len(rec.patient_ids)

    @api.constrains("is_intern", "mentor_id")
    def _check_intern_mentor(self):
        for rec in self:
            if rec.is_intern and not rec.mentor_id:
                raise UserError("An intern must have a mentor.")
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise UserError("An intern cannot be selected as a mentor.")


class Specialty(models.Model):
    _name = "hospital.doctor.speciality"
    _description = "Doctor Specialty"

    name = fields.Char(string="Doctor Speciality")
