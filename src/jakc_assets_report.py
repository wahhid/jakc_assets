from openerp.osv import fields, osv
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class assets_detail_report(osv.osv_memory):
    _name = "assets.detail.report"
    _columns = {
        'start_date' : fields.date('Start Date', required=True),
        'end_date' : fields.date('End Date', required=True)
    } 
    
    def generate_report(self, cr, uid, ids, context=None):
        params = self.browse(cr, uid, ids, context=context)
        param = params[0]   
        serverUrl = 'http://172.16.139.139:8888/jasperserver'
        j_username = 'itms_operator'
        j_password = 'itms123'
        ParentFolderUri = '/itms'
        reportUnit = '/itms/asset_detail_report'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new' 
        }
        
asset_detail_report()

