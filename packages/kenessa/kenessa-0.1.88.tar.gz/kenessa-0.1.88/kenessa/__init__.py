import sqlite3
from pkg_resources import resource_filename
import json
conn = sqlite3.connect(resource_filename(__name__, 'kenessa.db'))  # if kenessa.db doesn't exists it creates it
c = conn.cursor()


def get_province():
    c.execute('SELECT * FROM Province')
    data = c.fetchall()
    fields = [description[0] for description in c.description]
    output = [dict(zip(fields, d)) for d in data]
    return(output)


def get_district(province):
    fields = [description[0] for description in c.description]
    province = province.title()
    if province == 'All':
        c.execute('SELECT id, name FROM District')
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
    else:
        c.execute('SELECT District.id,District.name \
                    FROM District INNER JOIN Province ON District.province_id = Province.id \
                    WHERE Province.name = (?)', (province,))
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return (output)


def get_sector(district):
    fields = [description[0] for description in c.description]
    district = district.title()
    if district == 'All':
        c.execute('SELECT id,name FROM Sector')
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return(c.fetchall())
    else:
        c.execute('SELECT Sector.id,Sector.name \
                    FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                    WHERE District.name = (?)', (district,))
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return (c.fetchall())


def get_cell(sector):
    fields = [description[0] for description in c.description]
    sector = sector.title()
    if sector == 'All':
        c.execute('SELECT id,name FROM Cell')
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return(c.fetchall())
    else:
        c.execute('SELECT Cell.id,Cell.name\
                    FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                    WHERE Sector.name = (?)', (sector,))
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return(c.fetchall())


def get_village(cell):
    fields = [description[0] for description in c.description]
    cell = cell.title()
    if cell == 'All':
        c.execute('SELECT id,name FROM Village')
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return(c.fetchall())
    else:
        c.execute('SELECT Village.id,Village.name \
                    FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                    WHERE Cell.name = (?)', (cell,))
        data = c.fetchall()
        output = [dict(zip(fields, d)) for d in data]
        return(output)
        # return(c.fetchall())
