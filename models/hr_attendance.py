from odoo import models, fields, api, _
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def attendance_manual(self, next_action, entered_pin=None):
        self.ensure_one()
        now = fields.Datetime.now()
        
        last_attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', self.id)
        ], order='create_date desc', limit=1)

    
        if last_attendance:
            last_action_time = last_attendance.check_out or last_attendance.check_in
            if last_action_time + timedelta(minutes=3) > now:
                time_left = (last_action_time + timedelta(minutes=3) - now).total_seconds() / 60
                action_type = "salida" if last_attendance.check_out else "entrada"
                message = _("Error:¡No puede registrarse mas de una vez").format(action_type, time_left)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Advertencia'),
                        'message': message,
                        'type': 'warning',
                        'sticky': False,
                        'next': {
                            'type': 'ir.actions.client',
                            'tag': 'reload',
                        },
                    }
                }

        return super(HrEmployee, self).attendance_manual(next_action, entered_pin)