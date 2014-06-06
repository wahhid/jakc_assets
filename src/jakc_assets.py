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


class asset_software(osv.osv):
    _name = "asset.software"
    _description = "Asset Software"
    _columns = {
        'name': fields.char('Name', size=100, required=True),            
        'managed': fields.boolean('Managed'),            
    }    
asset_software()

class asset_location(osv.osv):
    _name = "asset.location"
    _description = "Asset Location"
    _columns = {
        'name': fields.char('Location', size=100, required=True),            
    }

asset_location()

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
        'barcode': fields.char('Barcode', size=20, readonly=True),            
        'name': fields.char('Name', size=100),                    
        'type': fields.many2one('asset.type','Type', required=True),
        'status': fields.many2one('asset.status','Status', required=True),
        'location': fields.many2one('asset.location','Location'),
        'label': fields.boolean('Labeled'),
        
        'image1': fields.binary('Image 1'),
        'image2': fields.binary('Image 2'),
        'image3': fields.binary('Image 3'),
        'image4': fields.binary('Image 4'),
        'image5': fields.binary('Image 5'),
        
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
        'repeat': fields.selection([('1','Daily'),('2','Monthly'),('3','Quaterly'),('4','Half Yearly'),('5','Yearly')],'Repeat'),
        'maint_day': fields.selection(get_day_selection,'Day'),        
        'maint_month': fields.selection(get_month_selection,'Month'),
        'maint_date': fields.date('Maintenance Date'),
        'pi_month': fields.selection(get_month_selection,'PI Month'),
        'pi_date': fields.date('PI Date'),        
    }        
    
    def _check_unique_insesitive(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 , [], context=context)
        lst = [x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context) if x.name and x.id not in ids]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.name and self_obj.name.lower() in  lst:
                return False
            return True
        
    _sql_constraints = [('asset_name_unique', 'unique(name)', 'Name already exists'),('asset_barcode_unique', 'unique(barcode)', 'Barcode already exists')]
    #_constraints = [(_check_unique_insesitive, 'Asset name already exists', ['name'])]
    
    def _get_company(self, cr, uid, id, context):
        obj = self.pool.get('itms.company')
        ids = []
        ids.append(id)
        return obj.read(cr, uid, ids,[], context)    
        
    def _get_department(self, cr, uid, id, context):				
        obj = self.pool.get('hr.department')
        ids = []
        ids.append(id)
        return obj.read(cr, uid, ids, [], context)    
    
    def _get_asset_type(self, cr, uid, id, context):				
        obj = self.pool.get('asset.type')
        ids = []
        ids.append(id)
        return obj.read(cr, uid, ids, [], context)      
    
    def _generate_barcode(self,cr,uid,values,context):    
        company_id = values['company']
        companys = self._get_company(cr,uid,company_id,context)
        company = companys[0]
        print company
        
        department_id = values['department']
        departments = self._get_department(cr,uid,department_id,context)        
        department = departments[0]
        
        type_id = values['type']
        types = self._get_asset_type(cr,uid,type_id,context)    
        type = types[0]
        
        return company['company_id'] + department['department_code'] + type['type_id']
        
    def create(self, cr, uid, values, context=None):		                        
        prefix = self._generate_barcode(cr,uid,values,context)    
        sequence = self.pool.get('ir.sequence').get(cr, uid, 'asset.barcode.sequence')    
        barcode = prefix + sequence
        name = values['name'].upper()
        values.update({'name':name})
        values.update({'barcode':barcode})
	return super(asset_assets, self).create(cr, uid, values, context = context)
    
    def write(self, cr, uid, ids, values, context):
        name = values['name'].upper()
        values.update({'name':name})
        return super(asset_assets, self).write(cr, uid, ids, values, context)
    
    def _maintenance_asset(self, cr, uid, context=None):
        print 'Start Maintenance Asset'
        ids = self.search(cr, uid, [('ismaintenance','=',True)])
        assets = self.read(cr, uid, ids, [], context)
        for asset in assets:
            print asset
                
asset_assets()
