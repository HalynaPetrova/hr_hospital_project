from odoo import models, fields
from odoo.exceptions import UserError


class ChangePersonalDoctorWizard(models.TransientModel):
    _name = "hospital.change.doctor.wizard"
    _description = "Change Personal Doctor Wizard"

    new_doctor_id = fields.Many2one("hospital.doctor", string="New Personal Doctor", required=True)

    def action_change_doctor(self):
        active_patients = self.env["hospital.patient"].browse(self.env.context.get("active_ids"))

        if not active_patients:
            raise UserError("No active patients selected.")

        for patient in active_patients:
            patient.write({
                "doctor_id": self.new_doctor_id.id,
            })

        return {"type": "ir.actions.act_window_close"}
