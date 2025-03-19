from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class Schedule(models.Model):
    _name = "hospital.schedule"
    _description = "Doctor's Schedule"
    _order = "schedule_datetime desc"
    _rec_name = "doctor_id"

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    state = fields.Selection([
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ], string="Status", default="scheduled")
    schedule_time = fields.Selection([
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("13:00", "13:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
    ], string="Time", required=True)
    schedule_datetime = fields.Datetime(string="Appointment Date & Time", compute="_compute_schedule_datetime", store=True)
    day_of_week = fields.Char(string="Day of Week", compute="_compute_day_of_week", store=True)

    @api.model
    def _set_schedule_date(self):
        return fields.Date.today()

    schedule_date = fields.Date(string="Date", default=_set_schedule_date)

    @api.depends("schedule_date")
    def _compute_day_of_week(self):
        for record in self:
            if record.schedule_date:
                record.day_of_week = record.schedule_date.strftime("%A")
            else:
                record.day_of_week = False

    @api.depends("schedule_date", "schedule_time")
    def _compute_schedule_datetime(self):
        for record in self:
            if record.schedule_date and record.schedule_time:
                schedule_time = (datetime.strptime(record.schedule_time, "%H:%M") - timedelta(hours=2)).time()
                record.schedule_datetime = datetime.combine(record.schedule_date, schedule_time)
            else:
                record.schedule_datetime = False

    @api.constrains("schedule_datetime")
    def _check_schedule_datetime(self):
        for record in self:
            if record.schedule_datetime:
                now = datetime.now()
                if record.schedule_datetime < now:
                    raise UserError("Appointment date and time cannot be in the past.")
                if record.schedule_datetime.weekday() in [5, 6]:
                    raise UserError("Doctor does not work on weekends (Saturday and Sunday)")
                existing_schedules = self.search([
                    ("schedule_datetime", "=", record.schedule_datetime),
                    ("id", "!=", record.id),
                ])
                if existing_schedules:
                    raise UserError(
                        "An appointment already exists for this date and time. Please choose another time."
                    )
                patient_schedules = self.search([
                    ("schedule_datetime", "=", record.schedule_datetime),
                    ("patient_id", "=", record.patient_id.id),
                    ("id", "!=", record.id),
                ])
                if patient_schedules:
                    raise UserError(
                        "You already have an appointment scheduled for this time. Please choose another date or time."
                    )

    def action_create_visit(self):
        if self.state == "cancelled":
            raise UserError("You cannot create an appointment for a cancelled schedule.")
        if self.state == "completed":
            raise UserError("You cannot create an appointment for a completed schedule.")

        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.visit",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_doctor_id": self.doctor_id.id,
                "default_patient_id": self.patient_id.id,
                "default_visit_date": self.schedule_datetime,
                "default_visit_time": self.schedule_time,
                "default_visit_datetime": self.schedule_datetime,
                "default_schedule_id": self.id,
            },
        }

    def action_schedule_cancel(self):
        for record in self:
            record.state = "cancelled"

    @api.constrains("patient_id", "schedule_date", "schedule_time")
    def _check_patient_schedule_conflict(self):
        for record in self:
            conflict = self.env["hospital.schedule"].search([
                ("patient_id", "=", record.patient_id.id),
                ("schedule_date", "=", record.schedule_date),
                ("schedule_time", "=", record.schedule_time),
                ("id", "!=", record.id)
            ])
            if conflict:
                raise UserError("The patient already has an appointment for this day and time. Please choose a different time.")

    @api.model
    def create(self, vals):
        new_record = super(Schedule, self).create(vals)
        new_record._check_patient_schedule_conflict()
        return new_record

    def write(self, vals):
        for record in self:
            if record.state in ["completed", "cancelled"]:
                if ("schedule_date" in vals or
                        "schedule_time" in vals or
                        "doctor_id" in vals or
                        "patient_id" in vals):
                    raise UserError("It is not possible to change the data for an appointment that has already taken place.")

        res = super(Schedule, self).write(vals)
        self._check_patient_schedule_conflict()
        return res

    def auto_complete_schedules(self):
        now = datetime.now()
        schedules_to_update = self.search([
            ("schedule_datetime", "<", now),
            ("state", "!=", "completed")
        ])
        for schedule in schedules_to_update:
            schedule.state = "completed"
