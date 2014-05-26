from openerp.osv import fields, osv
from datetime import datetime

class asset_category(osv.osv):
    _name = "asset.category"
    _description = "Asset Category"
    _columns = {
        'name': fields.char('Name', size=100, required=True),            
    }    
asset_category()

class asset_type(osv.osv):
    _name = "asset.type"
    _description = "Asset Type"
    _columns = {
        'type_id': fields.char('Type ID', size=2, required=True),            
        'name': fields.char('Name', size=100, required=True),            
    }    
asset_type()

class asset_status(osv.osv):
    _name = "asset.status"
    _description = "Asset Status"
    _columns = {
        'name': fields.char('Name', size=100, required=True),            
    }    
asset_status()

class asset_assets(osv.osv):
    _name = "asset.assets"
    _description = "Assets"
    def get_day_selection(self,cursor, user_id, context=None):
        return (
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6'),
            ('7','7'),
            ('8','8'),
            ('9','9'),
            ('10','10'),
            ('11','11'),
            ('12','12'),
            ('13','13'),
            ('14','14'),
            ('15','15'),
            ('16','16'),
            ('17','17'),
            ('18','18'),
            ('19','19'),
            ('20','20'),
            ('21','21'),
            ('22','22'),
            ('23','23'),
            ('24','24'),
            ('25','25'),
            ('26','26'),
            ('27','27'),
            ('28','28'),
            ('29','29'),
            ('30','30'),
            ('31','31'),
        )
    
    def get_month_selection(self,cursor, user_id, context=None):
        return(
            ('1','January'),
            ('2','February'),
            ('3','March'),
            ('4','April'),
            ('5','May'),
            ('6','June'),
            ('7','July'),
            ('8','August'),
            ('9','September'),
            ('10','October'),
            ('11','November'),
            ('12','December'),
        )    
    _columns = {
        'barcode': fields.char('Barcode', size=20, required=True),            
        'name': fields.char('Name', size=100, required=True),                    
        'type': fields.many2one('asset.type','Type', required=True),
        'status': fields.many2one('asset.status','Status', required=True),
        'label': fields.boolean('Labeled'),
        
        'model': fields.char('Model', size=200),            
        'serial_number': fields.char('Serial Number', size=200),            
        'vendor': fields.many2one('itms.vendor','Vendor'),
        
        'purchase_order': fields.char('Purchase Order #', size=20),
        'purchase_date': fields.date('Purchase Date'),
        'supplier': fields.many2one('res.partner','Supplier'),
        'warranty': fields.date('Warranty'),
        'decomission_date': fields.date('Decomission Date'),
        
        'company': fields.many2one('itms.company','Company', required=True),
        'department': fields.many2one('hr.department','Department', required=True),        
        'owner': fields.many2one('hr.employee','Owner'), 
        'login_name': fields.char('Login Name', size=30),
        
        'ismaintenance' : fields.boolean('Is Maintenance'),
        'maint_owner': fields.many2one('hr.employee','Technician'),
        'repeat': fields.selection([('01','Daily'),('02','Monthly'),('03','Quaterly'),('04','Half Yearly'),('05','Yearly')],'Repeat'),
        'maint_day': fields.selection(get_day_selection,'Day'),        
        'maint_month': fields.selection(get_month_selection,'Month'),
        'maint_date': fields.date('Maintenance Date'),
        'pi_month': fields.selection(get_month_selection,'PI Month'),
        'pi_date': fields.date('PI Date'),        
    }        
asset_assets()
