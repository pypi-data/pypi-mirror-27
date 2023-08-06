import sqlite3
from pkg_resources import resource_filename
# if kenessa.db doesn't exists it creates it
conn = sqlite3.connect(resource_filename(__name__, 'kenessa.db'))
#conn = sqlite3.connect('kenessa.db')


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
        query = "SELECT District.id,District.name \
                FROM District INNER JOIN Province ON District.province_id = Province.id \
                WHERE Province.id IN ({seq})".format(seq=','.join(['?'] * len(province)))
        self.c.execute(query, province)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_sector(self, district):
        query = "SELECT Sector.id,Sector.name \
                FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                WHERE District.id IN ({seq})".format(seq=','.join(['?'] * len(district)))
        self.c.execute(query, district)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_cell(self, sector):
        query = "SELECT Cell.id,Cell.name\
                FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                WHERE Sector.id IN ({seq})".format(seq=','.join(['?'] * len(sector)))
        self.c.execute(query, sector)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output

    def get_village(self, cell):
        query = "SELECT Village.id,Village.name \
                FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                WHERE Cell.id IN ({seq})".format(seq=','.join(['?'] * len(cell)))
        self.c.execute(query, cell)
        data = self.c.fetchall()
        fields = [description[0] for description in self.c.description]
        output = [dict(zip(fields, d)) for d in data]
        return output