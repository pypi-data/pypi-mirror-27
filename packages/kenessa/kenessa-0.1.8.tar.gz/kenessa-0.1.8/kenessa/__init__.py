import sqlite3
# from exellento import Excellento

conn = sqlite3.connect('./kenessa.db')  # if kenessa.db doesn't exists it creates it
c = conn.cursor()
#
#
# def create_tables():
#     c.execute('CREATE TABLE IF NOT EXISTS Province(id integer PRIMARY KEY , name TEXT)')
#     c.execute('CREATE TABLE IF NOT EXISTS District(id integer PRIMARY KEY, name TEXT, province_id integer, FOREIGN KEY(province_id) REFERENCES Province(id))')
#     c.execute('CREATE TABLE IF NOT EXISTS Sector(id integer PRIMARY KEY, name TEXT, district_id integer, FOREIGN KEY(district_id) REFERENCES District(id))')
#     c.execute('CREATE TABLE IF NOT EXISTS Cell(id integer PRIMARY KEY, name TEXT, sector_id integer, FOREIGN KEY(sector_id) REFERENCES Sector(id))')
#     c.execute('CREATE TABLE IF NOT EXISTS Village(id integer PRIMARY KEY, name TEXT, cell_id integer, FOREIGN KEY(cell_id) REFERENCES Cell(id))')
#
#
# def data_entry():
#     province_list = Excellento('./data/Provinces.xls').json_data()
#     district_list = Excellento('./data/Districts.xls').json_data()
#     sector_list = Excellento('./data/Sectors.xls').json_data()
#     cell_list = Excellento("./data/Cell.xls").json_data()
#     village_list = Excellento("./data/Village.xls").json_data()
#
#     # Provinces
#     for i in range(len(province_list)):
#         province_id = province_list[i]['prov_id']
#         province_name = province_list[i]['name']
#
#         c.execute("INSERT INTO Province(id, name) VALUES(?,?)", (province_id, province_name))
#
#     # Districts
#     for i in range(len(district_list)):
#         district_id = district_list[i]['dist_id']
#         district_name = district_list[i]['name']
#         province_id = district_list[i]['prov_id']
#
#         c.execute("INSERT INTO District(id, name, province_id) VALUES(?, ?, ?)",
#                   (district_id, district_name, province_id))
#
#     # Sectors
#     for i in range(len(sector_list)):
#         sector_id = sector_list[i]['sect_id']
#         sector_name = sector_list[i]['name']
#         district_id = sector_list[i]['dist_id']
#
#         c.execute("INSERT INTO Sector(id, name, district_id) VALUES(?, ?, ?)",
#                   (sector_id, sector_name, district_id))
#
#     # Cells
#     for j in range(len(cell_list)):
#         cell_id = cell_list[j]['cell_id']
#         cell_name = cell_list[j]['name']
#         sector_id = cell_list[j]['sect_id']
#         c.execute("INSERT OR IGNORE INTO Cell(id, name, sector_id) VALUES(?, ?, ?)",
#                   (cell_id, cell_name, sector_id))
#
#     # Villages
#     for i in range(len(village_list)):
#         village_id = village_list[i]['village_id']
#         village_name = village_list[i]['name']
#         cell_id = village_list[i]['cell_id']
#         c.execute("INSERT INTO Village(id, name, cell_id) VALUES(?,?,?)",
#                   (village_id, village_name, cell_id))
#
#     conn.commit()


def get_province():
    c.execute('SELECT * FROM Province')
    return(c.fetchall())


def get_district(province):
    if province == 'all':
        c.execute('SELECT id, name FROM District')
        return(c.fetchall())
    else:
        c.execute('SELECT District.id,District.name \
                    FROM District INNER JOIN Province ON District.province_id = Province.id \
                    WHERE Province.name = (?)', (province,))
        return(c.fetchall())


def get_sector(district):
    if district == 'all':
        c.execute('SELECT id,name FROM Sector')
        return(c.fetchall())
    else:
        c.execute('SELECT Sector.id,Sector.name \
                    FROM Sector INNER JOIN District ON Sector.district_id = District.id \
                    WHERE District.name = (?)', (district,))
        return(c.fetchall())


def get_cell(sector):
    if sector == 'all':
        c.execute('SELECT id,name FROM Cell')
        return(c.fetchall())
    else:
        c.execute('SELECT Cell.id,Cell.name\
                    FROM Cell INNER JOIN Sector ON Cell.sector_id= Sector.id \
                    WHERE Sector.name = (?)', (sector,))
        return(c.fetchall())


def get_village(cell):
    if cell == 'all':
        c.execute('SELECT id,name FROM Village')
        return(c.fetchall())
    else:
        c.execute('SELECT Village.id,Village.name \
                    FROM Village INNER JOIN Cell ON Village.cell_id = Cell.id \
                    WHERE Cell.name = (?)', (cell,))
        return(c.fetchall())

# create_tables()
# data_entry()

# c.close()
# conn.close()
