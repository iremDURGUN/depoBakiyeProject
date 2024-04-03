### Ürün bakiyelerinin tutulduğu veri tabanı için 6 tablo oluşturulmuştur. 
#### Bu tablolar arasındaki bağlantılar;
```
depolar --> depoBakiye (bire – çoklu ilişki)
depolar --> satıs (bire – çoklu ilişki)
depolar --> stokTakip (bire – çoklu ilişki)
```
```
firmalar --> satıs (bire – çoklu ilişki)
```
```
urunler --> depoBakiye (bire – çoklu ilişki)
urunler --> satıs (bire – çoklu ilişki)
urunler --> stokTakip (bire – çoklu ilişki)
```

* depoBakiye veri tabanında bire – çoklu ilişki kullanarak tablolar oluşturulmuştur.
* Bire – Çoklu ilişki tablolar arasında tablonun birisinde verinin sadece bir kez yazılmasına (bulunmasına) ihtiyaç duyulur, diğer bağlandığı tabloda ise bu verinin birden fazla bulunması gerekmektedir.
Bu tarz veri tutmaya ihtiyaç duyarak bağladığımız tablolar arasında bire – çoklu ilişki olur. Örnek vermemiz gerekirse depolar tablosunda ID numarası 6 olan depodan depolar tablosunda bir tane olabilir
ama depoBakiye tablosunda ID numarası 6 olan deponun birden fazla veri girişi olabilir yani ID numarası 6 olan deponun farklı urunlere dair bakiye bilgileri depoBakiye tablosunda tutulabilir.

* Eğer tablolar arasındaki bağlantıların diagramını incelemek isterseniz [depoBakiyeDiagram](https://github.com/iremDURGUN/depoBakiyeProject/blob/main/depoBakiyeDiagram_%20-%20Microsoft%20SQL%20Server%20Management%20Studio%2028.03.2024%2013_11_47.png) dosyasına giderek inceleyebilirsiniz.
