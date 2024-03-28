import pypyodbc

# depoBakiye DATABASE'ne bağlanılır.
# Server bilgisine kendi Server bilginizi girmeyi unutmayın!!
database = pypyodbc.connect(
    "DRIVER={SQL Server};"
    "Server=ServerName;"
    "Database=depoBakiye;"
    "Trusted_Connection=True;"
)

cursor = database.cursor()


# depoBakiye_Create_Database.sql dosyasını çalıştırarak veri tabanını oluşturduktan sonra
# tablo oluşturmak ve veri girişleri yapmak için
# ilgili fonksiyonları kullanıp çalıştırarak çalışmaya devam edebilirsiniz.
# Gerekli tabloları oluşturalım
# Fonksiyonu çalıştırırsınız tüm tablolar oluşacaktır
def tabloOlustur():
    # depoların tutulduğu tablo olusturulur
    cursor.execute("CREATE TABLE depolar (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " depoAdi VARCHAR(35) UNIQUE)")

    # firmaların tutulduğu tablo olusturulur
    cursor.execute("CREATE TABLE firmalar (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " firmaAdi VARCHAR(35) UNIQUE)")

    # urunlerin tutulduğu tablo olusturulur
    cursor.execute("CREATE TABLE urunler (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " urunAdi VARCHAR(35) UNIQUE)")

    # depoların bakiye bilgilerinin ürünlere göre tutulduğu tablo olusturulur
    cursor.execute("CREATE TABLE depoBakiye (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " depoID INT,"
                   " urunID INT,"
                   " bakiye MONEY, "
                   " FOREIGN KEY (depoID) REFERENCES depolar (ID),"
                   " FOREIGN KEY (urunID) REFERENCES urunler (ID))")

    # depolara eklenen her ürünün bilgisini tutmayı sağlayacak tablo
    cursor.execute("CREATE TABLE stokTakip (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " depoID INT,"
                   " urunID INT,"
                   " eklenenBakiye MONEY,"
                   " eklenenTarih DATETIME, "
                   " FOREIGN KEY (depoID) REFERENCES depolar (ID),"
                   " FOREIGN KEY (urunID) REFERENCES urunler (ID))")

    # yapılan satışların firma, ürün, depo ve alım bakiye bilgileriyle tutulduğu tablo olusturulur
    cursor.execute("CREATE TABLE satıs (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   "firmaID INT, "
                   "depoID INT,  "
                   "urunID INT, "
                   "firmaAlımMiktari MONEY,"
                   "satilanTarih DATETIME,"
                   "FOREIGN KEY (firmaID) REFERENCES firmalar (ID),"
                   "FOREIGN KEY (depoID) REFERENCES depolar (ID),"
                   "FOREIGN KEY (urunID) REFERENCES urunler (ID))")
    cursor.commit()


# Veri ekleme işlemleri için fonksiyonlar;
def depoEkle(x):
    cursor.execute(f"INSERT INTO depolar (depoAdi) VALUES ({x})")
    cursor.commit()


def firmaEkle(x):
    cursor.execute(f"INSERT INTO firmalar (firmaAdi) VALUES ({x})")
    cursor.commit()


def urunEkle(x):
    cursor.execute(f"INSERT INTO urunler (urunAdi) VALUES ({x})")
    cursor.commit()


def bakiyeBilgiEkle(x, y, z):
    cursor.execute(f"INSERT INTO depoBakiye (depoID, urunID, bakiye) VALUES ({x}, {y}, {z})")
    cursor.commit()


# satıs tablosuna veri girişi yaptıktan sonra satıs tablosuna girilmiş en son ID bilgisini buluruz.
# Bunun sebebi depoBakiye tablosunda değişiklik yaparken satıs tablosundaki son işlem yapılan firmaAlımMiktari' na
# ihtiyacımız olmasıdır. Sonrasında yeni_Bakiye' yi hesaplarız bunun içinde satıs yapılan depo' nun urun' u için
# depoBakiye' deki bakiye miktarı ve satıs yapılan bakiye miktarı arasındaki fark hesaplanarak bulunur.
# Son olarak da eğer bakiye varsa depoBakiye tablosunda bakiye güncellenir. Eğer yoksa uyarı mesajı döndürür.
# Satış bilgileri girildikten sonra depoBakiye tablosunda ürün için bakiye güncellemesi yapılır.
def satisBilgiEkle(x, y, z, k):
    cursor.execute(f"INSERT INTO satıs "
                   f"(firmaID, depoID, urunID, firmaAlımMiktari, satilanTarih) VALUES ({x}, {y}, {z}, {k}, GETDATE())")

    maxID = cursor.execute("SELECT MAX(ID) FROM satıs").fetchone()[0]

    yeni_Bakiye = cursor.execute(f"SELECT (d.bakiye - s.firmaAlımMiktari) FROM satıs AS s "
                                 f"INNER JOIN depoBakiye AS d ON s.urunID = d.urunID AND s.depoID = d.depoID "
                                 f"WHERE s.ID = {maxID} "
                                 f"GROUP BY s.firmaAlımMiktari, d.bakiye").fetchone()[0]

    if yeni_Bakiye < 0:
        print("Satın alma işlemi yapamazsınız yeterli bakiye yoktur.")
    else:
        cursor.execute(f"UPDATE depoBakiye SET bakiye = {yeni_Bakiye} WHERE urunID = {z} AND depoID = {y}")

    cursor.commit()


# satıs işlemi yaparken yapılan işlemlerin aynısını gerçekleştiririz
# sadece burada yeni_Bakiye depoBakiye' deki bakiye miktarı ve stokTakip tablosundaki eklenenBakiye' nin toplamıdır.
# Yeni bir stok girildikten sonra depoBakiye tablosunda ürün için güncelleme yapılır.

def stokTakipBilgiEkle(x, y, z):
    cursor.execute(f"INSERT INTO stokTakip (urunID, depoID, eklenenBakiye, eklenenTarih) "
                   f"VALUES ({x}, {y}, {z}, GETDATE())")

    maxID = cursor.execute("SELECT MAX(ID) FROM stokTakip").fetchone()[0]

    yeni_Bakiye = cursor.execute(f" SELECT SUM(s.eklenenBakiye + d.bakiye) FROM stokTakip AS s "
                                 f" INNER JOIN depoBakiye AS d ON s.urunID = d.urunID AND s.depoID = d.depoID "
                                 f" WHERE s.ID = {maxID}"
                                 f" GROUP BY d.bakiye, s.eklenenBakiye").fetchone()[0]

    cursor.execute(f"UPDATE depoBakiye SET bakiye = {yeni_Bakiye} WHERE urunID = {x} AND depoID = {y}")
    cursor.commit()


# satıs tablosuna veri girmek için fonksiyonu çalıştırılır.
# satisBilgiEkle("3", "6", "3", "2.000")

# İstenilen tablonun tamamını çıktı olarak veren sorgu
a = cursor.execute("SELECT * FROM stokTakip ORDER BY ID").fetchall()
d = cursor.execute("SELECT * FROM depoBakiye ORDER BY ID").fetchall()

# depoların toplam satış bakiyesi
b = cursor.execute("SELECT  d.depoID, k.depoAdi, SUM(bakiye) FROM depoBakiye AS d "
                   "INNER JOIN depolar AS k ON d.depoID = k.ID GROUP BY d.depoID, k.depoAdi").fetchall()

# firmaların toplam alım miktarları
c = cursor.execute("SELECT  d.firmaID, k.firmaAdi, SUM(firmaAlımMiktari) FROM satıs AS d "
                   "INNER JOIN firmalar AS k ON d.firmaID = k.ID GROUP BY d.firmaID, k.firmaAdi").fetchall()

# Firma' nın hangi ürün' ü hangi depodan ne kadar miktarda aldığının bilgisini satış işlemi tarihiyle sorgular.
p = cursor.execute("SELECT f.firmaAdi, d.depoAdi, u.urunAdi, s.satilanTarih, SUM(s.firmaAlımMiktari) FROM satıs as s  "
                   "INNER JOIN urunler as u ON s.urunID = u.ID  "
                   "INNER JOIN firmalar as f ON s.firmaID = f.ID "
                   "INNER JOIN depolar as d ON s.depoID = d.ID "
                   "GROUP BY s.firmaID, s.urunID, u.urunAdi, d.depoAdi,f.firmaAdi, s.satilanTarih")

# Döngü sayesinde tabloları çıktı olarak alırız
for e in p:
    print(e)

database.close()
