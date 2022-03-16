import mysql.connector

# Jared home user/pass = root
# Broken, Tired, WIP
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="Zimp"
)

zimpDB = mydb.cursor()

zimpDB.execute("IF DATABASE EXISTS DROP Zimp")
zimpDB.execute("CREATE DATABASE IF NOT EXISTS Zimp")
zimpDB.execute("CREATE TABLE IF NOT EXISTS Items(itemID int NOT NULL AUTO_INCREMENT, itemName CHAR(255), itemAttack int, itemWeapon bool, itemDesc varchar(255), itemUsable bool)")
zimpDB.execute("CREATE TABLE IF NOT EXISTS Tile(tileID int NOT NULL AUTO_INCREMENT, tileName varchar(255), tileEffect varchar(255), tileX int, tileY int, doorNorth bool, doorEast bool, doorSouth bool, doorWest bool)")
zimpDB.execute("CREATE TABLE IF NOT EXISTS DevCard(devID int NOT NULL AUTO_INCREMENT, nineEffect varchar(255), tenEffect varchar(255), elevenEffect varchar(255), item varchar(255), numZombies int)")

zimpDB.execute("SHOW TALES")
for x in zimpDB:
    print(x)