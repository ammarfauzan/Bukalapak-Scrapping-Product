import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import os.path

#Inisiasi File CSV
filename = "BukalapakFix1.csv"
daftar = [] 
link_list = []
#Variable Support
j=0
#Open Each Page
for i in range (1,10):
	my_url = "https://www.bukalapak.com/products/s?brand_badge=false&campaign_name=&page=" + str(i) + "&search%5Bkeywords%5D=baju+batik+pria"
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("div", {"class":"product-card"})
	#Open Each Product
	for contain in containers:
		tanggal = datetime.date.today()
		waktu = datetime.datetime.now().time()
		j += 1
		print("hal :" + str(i))
		nama_produk = contain.article["data-name"].replace("\n","")
		id_produk = contain.article["data-id"]
		daftar.append(id_produk)
		try:
			review = contain.find("a",{"class","review__aggregate"}).text
		except AttributeError:
			review = 0	
		print("id :" + id_produk, str(review))
		harga_produk = contain.find("span", {"class":"amount positive"}).text.replace(".","")
		harga_diskon = contain.find("div",{"class":"product-price"})
		harga_diskon1 = harga_diskon["data-reduced-price"]
		diskon = (int(harga_produk) - int(harga_diskon1))/int(harga_produk)
		diskon1 = "{:.0%}".format(diskon)
		url_produk = "https://www.bukalapak.com" + contain.article.div.a["href"]
		link_list.append(url_produk)
		uClient = uReq(url_produk)
		page_html = uClient.read()
		uClient.close()
		page_soup_prod = soup(page_html, "html.parser")
		pelapak = page_soup_prod.find("a", {"class":"c-user-identification__name qa-seller-name"}).text
		#pelapak1 = pelapak[0]["title"]
		jumlah_pengiriman = page_soup_prod.findAll("td", {"class":"qa-seller-shipping-courier-value"})
		jum_ship = len(jumlah_pengiriman)
		try:
			pelanggan = page_soup_prod.find("td",{"class","qa-seller-subscriber-value"}).text.replace(" orang","")
		except AttributeError:
			pelanggan = 0	
		print(pelapak, str(pelanggan))
		cek = page_soup_prod.find("dd",{"class":"c-deflist__value qa-pd-category-value qa-pd-category"})
		if cek is None:
			kategori = "tidak tersedia"
		else:
			kategori = page_soup_prod.find("dd",{"class":"c-deflist__value qa-pd-category-value qa-pd-category"}).text.replace("\n","").replace(";","")
		cek2 = page_soup_prod.find("dd", {"class":"c-deflist__value qa-pd-sold-value"})
		if cek2 is None:
			terjual = 0
		else:
			terjual = page_soup_prod.find("dd", {"class":"c-deflist__value qa-pd-sold-value"}).text.replace("\n","")
		cek3 = page_soup_prod.find("dd", {"class":"c-deflist__value qa-pd-seen-value js-product-seen-value"})
		if cek3 is None:
			dilihat = 0
		else:	
			dilihat = page_soup_prod.find("dd", {"class":"c-deflist__value qa-pd-seen-value js-product-seen-value"}).text.replace("\n","")
		#Inser Data Scraping into CSV
		file_exists = os.path.isfile(filename)
		with open(filename, "a") as csvfile:
			headers = 'no; tanggal;waktu;pelapak;pelanggan; id_produk; kategori; nama_barang; harga normal;harga diskon;diskon; terjual; dilihat;review; alternatif_pengiriman\n'
			if not file_exists:
				csvfile.write(headers)
			csvfile.write(str(j) + ";" + str(tanggal) +";"+ str(waktu) +";"+pelapak + ";" + str(pelanggan)+";"+ str(id_produk) + ";"+ kategori + ";" + nama_produk + ";" + harga_produk + ";" + str(harga_diskon1) +";"+ str(diskon1) +";"+str(terjual) + ";" + str(dilihat) + ";" + str(review) +";"+str(jum_ship) + "\n")
		csvfile.close()	
#print(daftar)
print(link_list)	