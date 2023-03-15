from odoo import api, fields, models, tools


class SaleReport(models.Model):
    _name = "hospital.report"
    _description = "Pacient Visits Report"
    _auto = False

    date = fields.Datetime('Visit Date', readonly=True)
    patient_id = fields.Many2one('hospital.patient', 'Patient', readonly=True)
    doctor_id = fields.Many2one('hospital.doctor', 'Doctor', readonly=True)
    visit_id = fields.Integer('Visit #', readonly=True)
    visit_state = fields.Char('Visit State', readonly=True)
    visit_qty = fields.Integer('Qty', readonly=True)

    def _query(self):
        query_desc = """
            SELECT
                MIN(hv.id) AS id,
                hv.date date,
                hv.patient_id patient_id,
                hv.id as visit_id,
                hv.doctor_id as doctor_id,
                hv.state visit_state,
                COUNT(hv.id) as visit_qty
            FROM hospital_visit hv
            GROUP BY  hv.date,
                hv.patient_id, visit_id, doctor_id, visit_state
        """
        return query_desc

    @property
    def _table_query(self):
        return self._query()
