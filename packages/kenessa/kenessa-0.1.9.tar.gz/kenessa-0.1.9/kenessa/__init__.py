import sqlite3
from pkg_resources import resource_filename
conn = sqlite3.connect(resource_filename(__name__, 'kenessa.db'))  # if kenessa.db doesn't exists it creates it


class Kenessa:
    def __init__(self):
        self.c = conn.cursor()

    def get_province(self):
        self.c.execute('SELECT * FROM Province')
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_district(self, province):
        province = province.title()
        if province == 'All':
            self.c.execute('SELECT id, name FROM District')
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output
        else:
            self.c.execute('SELECT District.id,District.name \
                        FROM District INNER JOIN Province ON District.province_id = Province.id \
                        WHERE Province.id = (?)', (province,))
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output

    def get_sector(self, district):
        district = district.title()
        if district == 'All':
            self.c.execute('SELECT id,name FROM Sector')
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output

        else:
            self.c.execute('SELECT Sector.id,Sector.name \
                        FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                        WHERE District.id = (?)', (district,))
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output

    def get_cell(self, sector):
        sector = sector.title()
        if sector == 'All':
            self.c.execute('SELECT id,name FROM Cell')
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output
        else:
            self.c.execute('SELECT Cell.id,Cell.name\
                        FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                        WHERE Sector.id = (?)', (sector,))
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output

    def get_village(self, cell):
        cell = cell.title()
        if cell == 'All':
            self.c.execute('SELECT id,name FROM Village')
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output

        else:
            self.c.execute('SELECT Village.id,Village.name \
                        FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                        WHERE Cell.id = (?)', (cell,))
            data = self.c.fetchall()
            fields = [description[0] for description in self.c.description]
            output = [dict(zip(fields, d)) for d in data]
            return output
