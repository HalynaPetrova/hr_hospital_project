from datetime import date
from odoo import models, fields, api


class Patient(models.Model):
    _name = "hospital.patient"
    _inherit = "hospital.person"
    _description = "Hospital Patient"
    _rec_name = "full_name"

    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    passport = fields.Char(string="Passport Info")
    marital_status = fields.Selection([
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
    ], string="Marital Status")
    children = fields.Integer(string="Children Count")
    allergy_ids = fields.Many2many("hospital.patient.allergy", string="Allergies")
    insurance = fields.Boolean(string="Insured")
    insurance_company_id = fields.Many2one("res.partner", string="Insurance Company")
    policy_number = fields.Char(string="Insurance Policy Number", help="Enter the insurance policy number")
    doctor_id = fields.Many2one("hospital.doctor", string="Personal Doctor")
    doctor_speciality_id = fields.Many2one(
        "hospital.doctor.speciality",
        string="Doctor Speciality",
        related="doctor_id.speciality_id"
    )
    doctor_image_1024 = fields.Binary(string="Photo", related="doctor_id.image_1024")
    doctor_phone = fields.Char(string="Phone", related="doctor_id.phone")
    doctor_email = fields.Char(string="Email", related="doctor_id.email")
    schedule_ids = fields.One2many("hospital.schedule", "patient_id", string="Doctor's Schedule")
    visit_ids = fields.One2many("hospital.visit", "patient_id", string="Visits")
    diagnosis_ids = fields.One2many("hospital.diagnosis", "patient_id", string="Diagnoses")
    lab_tests_ids = fields.One2many("hospital.research", "patient_id", string="Tests")
    contact_person_id = fields.Many2one("hospital.contact.person", string="Contact Person")
    relation_to_patient = fields.Selection([
        ("father", "Father"),
        ("mother", "Mother"),
        ("husband", "Husband"),
        ("wife", "Wife"),
        ("child", "Child"),
        ("brother", "Brother"),
        ("sister", "Sister"),
        ("relative", "Relative"),
        ("friend", "Friend"),
        ("other", "Other")
    ], string="Relation to Patient")

    @api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                rec.age = (date.today() - rec.date_of_birth).days // 365
            else:
                rec.age = 0

    def action_create_schedule(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.schedule",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_doctor_id": self.doctor_id.id,
                "default_patient_id": self.id,
            },
        }


class PatientAllergy(models.Model):
    _name = "hospital.patient.allergy"
    _description = "Patient Allergies"

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color")


class ContactPerson(models.Model):
    _name = "hospital.contact.person"
    _inherit = "hospital.person"
    _description = "Contact Person"
    _rec_name = "full_name"
