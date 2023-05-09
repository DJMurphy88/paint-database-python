class Paint:
    def __init__(self, paint_id, paint_name, paint_type, pot_amount,
                 pot_status, paint_colour, hexcode, brand):
        self.paint_id = paint_id
        self.paint_name = paint_name
        self.paint_type = paint_type
        self.pot_amount = pot_amount
        self.pot_status = pot_status
        self.paint_colour = paint_colour
        self.hexcode = hexcode
        self.brand = brand

    def __str__(self):
        return f'ID: {self.paint_id} Name: {self.paint_name} Type: {self.paint_type}'

class Project:
    def __init__(self, project_id, project_name, system, parts=None):
        self.project_id = project_id
        self.project_name = project_name
        self.parts = parts
        self.system = system
