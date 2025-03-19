from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class Research(models.Model):
    _name = "hospital.research"
    _description = "Patient Research"

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
    test_id = fields.Many2one(
        "hospital.research.category",
        string="Lab Test Name",
        ondelete="set null"
    )
    test_category = fields.Many2one(
        related="test_id.parent_id",
        string="Lab Test Category",
        store=True,
        readonly=True
    )
    sample_type = fields.Many2many(
        "hospital.sample.type",
        string="Sample Type"
    )
    test_date = fields.Date(
        string="Test Date",
        readonly=True
    )
    conclusion = fields.Text("Conclusion")
    visit_id = fields.Many2one(
        "hospital.visit",
        string="Visit Information"
    )
    status = fields.Selection([
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], string="Status", default="pending")

    @api.constrains("test_date")
    def _check_test_date(self):
        for record in self:
            if record.test_date and record.test_date > date.today():
                raise UserError("The test date cannot be in the future.")

    def action_cancel_test(self):
        for record in self:
            if record.status == "completed":
                raise UserError("This test has already been completed and cannot be cancelled.")
            elif record.status == "cancelled":
                raise UserError("This test has already been cancelled.")
            else:
                record.status = "cancelled"

    def action_completed_test(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("This test has been cancelled and cannot be marked as completed.")
            elif record.status == "completed":
                raise UserError("This test has already been completed.")
            else:
                record.status = "completed"
                if not record.test_date:
                    record.test_date = date.today()
                if record.visit_id and all(test.status == "completed" for test in record.visit_id.tests_ids):
                    record.visit_id.state = "waiting_for_diagnosis"


class LabTestDirectory(models.Model):
    _name = "hospital.research.category"
    _description = "Lab Test Directory"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Test Name",
        required=True
    )
    parent_id = fields.Many2one(
        "hospital.research.category",
        string="Lab Test Category",
        ondelete="cascade"
    )
