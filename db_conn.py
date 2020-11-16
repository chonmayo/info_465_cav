import pyodbc 
import request


def Conn():
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-J5364RA;"
        "Database=V2X;"
        "Trusted_Connection=yes;"
    )
    return conn
#returns an array of locations from the database
def Read(organ_class, bloodtype, age):
    conn = Conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Hospital_t.Hospital_x,Hospital_t.Hospital_y,Hospital_t.Hospital_name \
        FROM ((Organ_t RIGHT OUTER JOIN Hospital_t ON Organ_t.Hospital_ID=Hospital_t.Hospital_ID) \
        LEFT JOIN Donor_t ON Donor_t.Donor_ID=Organ_t.Donor_ID) \
        WHERE Donor_t.Donor_blood_type={bt} AND Donor_t.Donor_age={a} AND Organ_t.Organ_type={ot};".format(bt=bloodtype,a=age,ot=organ_class)
    )

    row = cursor.fetchone() 
    locations = []
    while row: 
        ##Create array of locations to return
        loc = request.Location(float(row[0]),float(row[1]),row[2])
        locations.append(loc)
        row = cursor.fetchone()
    conn.close()
    return locations


def Create(map, Table_t):
    conn = Conn()
    column_names = ""
    vals = ""

    for x in map:
        column_names+=','
        column_names+=(x)

        vals+=','
        vals+=str(map[x])
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO {t} ({columns}) \
        Values({values})".format(t=Table_t, columns=column_names[1:], values=vals[1:])
    )
    conn.commit()
    conn.close()

def Delete(Object_id, table_t):
    conn = Conn()
    cursor = conn.cursor()
    cursor.execute(
        "Delete from {table} where Organ_id={id}".format(table=table_t, id=Object_id)
    )
    conn.commit()
    conn.close()