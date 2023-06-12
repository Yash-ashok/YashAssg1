import time
import os
import pyodbc
from flask import Flask, render_template, request, flash
from azure.storage.blob import BlobServiceClient, ContentSettings

app = Flask(__name__)
app.config["image_folder"] = "./static/"
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif']
app.secret_key = "Secret Key"

DRIVER = '{ODBC Driver 17 for SQL Server}'
SERVER = 'dbcyash.database.windows.net'
DATABASE = 'YashAssignment1'
USERNAME = 'YashAshok'
PASSWORD = 'Cyesar@2010'

cnxn = pyodbc.connect(
    'Driver={ODBC Driver 18 for SQL Server};Server=tcp:dbcyash.database.windows.net,1433;Database=YashAssignment1;Uid=YashAshok;Pwd=Cyesar@2010;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
)
#cnxn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
# # Configuration
# DRIVER = '{ODBC Driver 18 for SQL Server}'
# SERVER = 'dbcyash.database.windows.net'
# DATABASE = 'YashAssignment1'
# USERNAME = 'YashAshok'
# PASSWORD = 'Cyesar@2010'
#
# # Establish connection
# cnxn = pyodbc.connect(
#     f"DRIVER={DRIVER};"
#     f"SERVER={SERVER};"
#     f"DATABASE={DATABASE};"
#     f"UID={USERNAME};"
#     f"PWD={PASSWORD};"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )
crsr = cnxn.cursor()

connection_string = "Server=tcp:dbcyash.database.windows.net,1433;Initial Catalog=YashAssignment1;Persist Security Info=False;User ID=YashAshok;Password={your_password};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
image_container = "yashassign1"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/people', methods=['GET', 'POST'])
def people():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    peoplequery = "select num,name, comments from dbo.datan"
    crsr.execute(peoplequery)
    peoplelist = crsr.fetchall()
    print(peoplelist)
    # for i in peoplelist:
    #     print(i[6])
    #     if i[6]== None:
    #         i[6]="Image not found"
    count = len(peoplelist)
    count=count
    # return render_template('people.html', count=count, list1=peoplelist, link=link)
    return render_template('dataAll.html', count=count, list1=peoplelist, link=link)

@app.route('/speople', methods=['GET', 'POST'])
def speople():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    peoplequery = "select name,year, picture from dbo.datan"
    crsr.execute(peoplequery)
    peoplelist = crsr.fetchall()
    print(peoplelist)
    # for i in peoplelist:
    #     print(i[6])
    #     if i[6]== None:
    #         i[6]="Image not found"
    count = len(peoplelist)
    count=count
    # return render_template('people.html', count=count, list1=peoplelist, link=link)
    return render_template('showAll.html', count=count, list1=peoplelist, link=link)    


# @app.route('/displaypic', methods=['GET', 'POST'])
# def displaypic():
#     link = "https://yashassign1.blob.core.windows.net/yashassign1/"
#     name=str(request.form.get("namedata"))
#     print(name)
#     peoplequery = "select name, year, picture from dbo.datan where Name='{}'".format(name)
#     crsr.execute(peoplequery)
#     nameandpiclist = crsr.fetchall()
#     print(nameandpiclist)
#     for i in nameandpiclist:
#         if i[1]=='':
#             i[1]="Image not found"
#     return render_template('displaypic.html', name=name, list2=nameandpiclist, link=link)

@app.route('/displaypic', methods=['GET', 'POST'])
def displaypic():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    name=str(request.form.get("namedata"))
    print(name)
    peoplequery = "select name, year, picture from dbo.datan "
    crsr.execute(peoplequery)
    nameandpiclist = crsr.fetchall()
    print(nameandpiclist)
    # for i in nameandpiclist:
    #     if i[1]=='':
    #         i[1]="Image not found"
    return render_template('displaypic.html',list2=nameandpiclist, link=link)

@app.route('/salgreaterthan', methods=['GET', 'POST'])
def salgreaterthan():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    salquery = "select Picture from dbo.people where salary > 90000"
    crsr.execute(salquery)
    sallist = crsr.fetchall()
    return render_template('sallist.html', list3=sallist, link=link)

@app.route('/uploadpic', methods = ['GET', 'POST'])
def uploadpic():
    if request.method == 'POST':
        personname = request.form.get("namedatapic")
        image =  request.files["image"]
        checkext = image.filename.split(".")
        if checkext[1] not in app.config['UPLOAD_EXTENSIONS']:
            flash("Please check the file extension and try again.")
        else:
            uploadpicquery = "UPDATE dbo.people set Picture='{}' where Name='{}'".format(image.filename, personname)
            crsr.execute(uploadpicquery)
            image.save(os.path.join(app.config["image_folder"], image.filename))
            local_filepath=os.path.join(app.config["image_folder"], image.filename)
            blob_service_client =  BlobServiceClient.from_connection_string(cnxn)
            blob_client = blob_service_client.get_blob_client(container=image_container, blob=image.filename)
            image_content_setting = ContentSettings(content_type='image/jpeg')
            with open(local_filepath, "rb") as data:
                blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
                time.sleep(2)
            flash("File Upload Successfully")
    return render_template('index.html')

@app.route('/deleterecord', methods=['GET', 'POST'])
def deleterecord():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
   # https://yashassign1.blob.core.windows.net/yashassign1/
    nameone=str(request.form.get("namedataone"))
    deletepeoplequery = "Delete from dbo.people where Name='{}'".format(nameone)
    crsr.execute(deletepeoplequery)
    peoplequery = "Select * from dbo.people"
    crsr.execute(peoplequery)
    peoplelist = crsr.fetchall()
    count = len(peoplelist)
    return render_template('deleterecord.html', count=count, list4=peoplelist, link=link, nameone=nameone)

@app.route('/changesal', methods=['GET', 'POST'])
def changesal():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    namesal=str(request.form.get("namedatasal"))
    personsal = str(request.form.get("persal"))
    com= str(request.form.get("percom"))
    salquery = "UPDATE dbo.datan set num={} where Name='{}'".format(personsal, namesal)
    comquery = "UPDATE dbo.datan set comments={} where Name='{}'".format(com, namesal)

    crsr.execute(salquery)
    personquery = "Select * from dbo.people where Name='{}'".format(namesal)
    crsr.execute(personquery)
    personlist = crsr.fetchall()
    return render_template('changesal.html', list5=personlist, namesal=namesal, link=link)


@app.route('/keyword', methods=['GET', 'POST'])
def keyword():
    link = "https://yashassign1.blob.core.windows.net/yashassign1/"
    namechng=str(request.form.get("namechange"))
    keywor= str(request.form.get("keychange"))
    updatequery = "UPDATE dbo.people set Keywords='{}' where Name='{}'".format(keywor, namechng)
    crsr.execute(updatequery)
    keyquery = "select * from dbo.people where Name='{}'".format(namechng)
    crsr.execute(keyquery)
    size = crsr.fetchall()
    print(size)
    return render_template('changekeyword.html', list6=size, link=link, namechng=namechng)


if __name__ == "__main__":
    app.run(port=5500,debug=True)
