from odoo import http
from odoo.http import request
import json

class MainHospital(http.Controller):
    @http.route('/hospital/new_visit', type='json', methods=['POST'], auth='none', csrf=False)
    def add_new_visit(self, **post):
        print('params)',post)
        print('http.request.params',http.request.params)
        res = request.env['hospital.visit'].add_new_visit(post)
        return json.dumps(res)
