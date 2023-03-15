from odoo import models, fields, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError

class DiseaseType(models.Model):
    _name = 'disease.type'

    _description = 'Disease type'

    name = fields.Char()
    symptoms = fields.Html('Symptoms')
    treatment = fields.Html('Treatment')


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    name = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    specialization = fields.Html()


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital patient'
    name = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    attending_doctor = fields.Many2one('hospital.doctor', string="Attending doctor")

    complaint = fields.Html('Complaints')
    treatment = fields.Html('Treatments')


class DiseaseType(models.Model):
    _name = 'hospital.visit'

    _description = 'Patient Visit'

    state = fields.Selection([('plan', 'Planned'), ('in_action', 'In action'), ('happen', 'Happen')], default="plan")
    date = fields.Datetime(string="Visit date/time", default=fields.Datetime.now)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    complaint = fields.Html('Complaints')
    diagnosis = fields.Html('Diagnosis')
    treatment = fields.Html('Treatments')

    def action_in_action(self):
        self.write({'state': 'in_action'})

    def action_happen(self):
        self.write({'state': 'happen'})

    def action_plan(self):
        self.write({'state': 'plan'})

    def _block_delete_archive(self):
        if self.diagnosis:
            return True
        else:
            return False

    def unlink(self):
        if self._block_delete_archive():
            raise ValidationError(_('You cannot delete / archive visit with diagnosis'))
        return super().unlink()

    def get_plan_visit_date(self):

       return  datetime.now() + timedelta(days=10)

    def add_new_visit(self, params):
      # params - dict = {'patient': 'Name' , 'phone': 'Phone'}
       if not params:
           return {'success': False, 'description': 'No pacient name and phone number to register visit'}
       for check in ['patient', 'phone']:
           if not params.get(check, False):
               return {'success': False, 'description': 'No %s name to register visit'%(check)}
       patient = self.env['hospital.patient'].sudo().search([('phone','=', params.get('phone'))])
       if not patient:
           patient_vals ={'name': params['patient'], 'phone': params['phone']}
           patient = self.env['hospital.patient'].sudo().create(patient_vals)
       visit_vals = {'patient_id': patient.id, 'state': 'plan', 'date': self.get_plan_visit_date()}
       new_visit = self.env['hospital.visit'].sudo().create(visit_vals)

       return {'success': True, 'visit_id': new_visit.id, 'visit_date': new_visit.date.strftime('%Y-%m-%d')}


