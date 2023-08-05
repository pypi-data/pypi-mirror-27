import sqlite3
import json
conn = sqlite3.connect('./kenessa.db')  # if kenessa.db doesn't exists it creates it
c = conn.cursor()


def get_province():
    c.execute('SELECT * FROM Province')
    return(c.fetchall())


def get_district(province):
    province = province.title()
    if province == 'All':
        c.execute('SELECT id, name FROM District')
        return(c.fetchall())
    else:
        c.execute('SELECT District.id,District.name \
                    FROM District INNER JOIN Province ON District.province_id = Province.id \
                    WHERE Province.name = (?)', (province,))
        return (c.fetchall())


def get_sector(district):
    district = district.title()
    if district == 'All':
        c.execute('SELECT id,name FROM Sector')
        return(c.fetchall())
    else:
        c.execute('SELECT Sector.id,Sector.name \
                    FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                    WHERE District.name = (?)', (district,))
        return (c.fetchall())


def get_cell(sector):
    sector = sector.title()
    if sector == 'All':
        c.execute('SELECT id,name FROM Cell')
        return(c.fetchall())
    else:
        c.execute('SELECT Cell.id,Cell.name\
                    FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                    WHERE Sector.name = (?)', (sector,))
        return(c.fetchall())


def get_village(cell):
    cell = cell.title()
    if cell == 'All':
        c.execute('SELECT id,name FROM Village')
        return(c.fetchall())
    else:
        c.execute('SELECT Village.id,Village.name \
                    FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                    WHERE Cell.name = (?)', (cell,))
        return(c.fetchall())
