from odoo import models, fields, api
from odoo.exceptions import UserError


class Visit(models.Model):
    _name = "hospital.visit"
    _description = "Doctor Visit"
    _order = "visit_datetime desc"
    _rec_name = "visit_code"

    VISIT_TYPE_SELECTION = [
        ("primary", "Primary Visit"),
        ("follow_up", "Follow-up Visit"),
    ]

    visit_code = fields.Char(string="Visit Code", compute="_compute_visit_code")
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    visit_type = fields.Selection(VISIT_TYPE_SELECTION, string="Type")
    visit_date = fields.Date(string="Date", store=True)
    visit_time = fields.Char(string="Time", store=True)
    visit_datetime = fields.Datetime(string="Time")
    schedule_id = fields.Many2one("hospital.schedule", string="Schedule", required=True)
    recommendation = fields.Char(string="Recommendation")
    is_doctor_intern = fields.Boolean(string="Is Doctor Mentor", related="doctor_id.is_intern")
    mentor_note = fields.Text(string="Mentor Note")
    state = fields.Selection(
        [
            ("started", "Started"),
            ("waiting_for_results", "Waiting for Lab Test Results"),
            ("return_visit_scheduled", "Return Visit Scheduled"),
            ("waiting_for_diagnosis", "Waiting for Diagnosis"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="Visit Status",
        default="started",
    )
    symptom_ids = fields.Many2many("hospital.symptom", string="Symptoms")
    complaints = fields.Text(string="Complaints")
    tests_ids = fields.One2many("hospital.research", "visit_id", string="Tests")
    diagnosis_ids = fields.One2many("hospital.diagnosis", "visit_id", string="Diagnosis")

    @api.depends("visit_date", "patient_id")
    def _compute_visit_code(self):
        for record in self:
            if record.visit_date and record.patient_id:
                visit_count = 1
                record.visit_code = f"{record.visit_date.strftime('%Y%m%d')}-{record.patient_id.id}-{visit_count}"
                visit_count += 1
            else:
                record.visit_code = ""

    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise UserError("It is not possible to delete an appointment that has diagnoses.")
        return super(Visit, self).unlink()

    def _change_state(self, new_state, error_message):
        for record in self:
            if record.state == new_state:
                raise UserError(error_message)
            record.state = new_state

    def action_visit_cancel(self):
        self._change_state(
            "completed", "This visit has already been completed and cannot be cancelled."
        )
        self._change_state("cancelled", "This visit has already been cancelled.")

    def action_completed_visit(self):
        self._change_state(
            "cancelled", "This visit has been cancelled and cannot be marked as completed."
        )
        self._change_state("completed", "This visit has already been completed.")

    def action_assign_test(self):
        self._change_state(
            "completed", "This visit has already been completed. You cannot assign a test to a completed visit."
        )
        self._change_state(
            "cancelled", "This visit has been cancelled. You cannot assign a test to a cancelled visit."
        )
        for record in self:
            record.state = "waiting_for_results"
        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.research",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_doctor_id": self.doctor_id.id,
                "default_patient_id": self.patient_id.id,
                "default_visit_id": self.id,
            },
        }

    def action_follow_up_scheduled(self):
        self._change_state(
            "completed", "This visit has already been completed. You cannot schedule a follow-up appointment."
        )
        self._change_state(
            "cancelled", "This visit has been cancelled. You cannot schedule a follow-up appointment for a cancelled visit."
        )
        for record in self:
            record.state = "return_visit_scheduled"
        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.schedule",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_doctor_id": self.doctor_id.id,
                "default_patient_id": self.patient_id.id,
            },
        }

    def action_confirm_diagnosis(self):
        for record in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "hospital.diagnosis",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_doctor_id": record.doctor_id.id,
                    "default_patient_id": record.patient_id.id,
                    "default_visit_id": record.id,
                },
            }
