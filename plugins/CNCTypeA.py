# Simple CNC Data Processing Plugin implementation 
class CNCTypeA:
    def __init__(self, data, db_manager):
        print(f"Calling [CNCTypeA] Plugin for handling data: {data}")
        try:
            fields = ['cnc_id', 'part_program', 'timestamp','json_data']
            values = [data['cnc_id'], data['part_program'], data['timestamp'],data['payload']]
            db_manager.insert('cnc_data', fields, values)
        except Exception as e:
            print(f"[ERROR] CNCTypeA Plugin failed to process: {e}")
