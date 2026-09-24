# Turkcha Test Bot
# Python 3.11+ / python-telegram-bot 21+
# Tokenni kodga yozmang. Hostingda BOT_TOKEN environment variable yarating.

import os
import random
import sqlite3
from datetime import datetime, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN", "").strip()
DB_PATH = os.getenv("DB_PATH", "turkcha_test.sqlite3")

# =========================================================
# LUG'AT — foydalanuvchi yuborgan A1 PDF asosida
# =========================================================
WORDS = {
1: [
("Merhaba","Salom"),("Benim adım....","Mening ismim…"),("Memnun oldum","Mamnun bo’ldim"),
("Ben de memnun oldum","Men ham mamnun bo’ldim"),("Günaydın","Xayrli tong"),
("iyi günler","Xayrli kun"),("iyi akşamlar","Xayrli oqshom"),("iyi geceler","Xayrli tun"),
("Sizin adınız ne","Sizning ismingiz nima"),("Nasılsınız","Qandaysiz"),
("Teşekkür ederim, iyim","Raxmat , yaxshiman"),("Bende iyim","Men ham yaxshiman"),
("Adınız ne?","Ismingiz nima"),("Tanıştırayım …","Tanishtiray…"),
("Tanıştığımıza memnun oldum","Tanishganimizdan mamnun bo’ldim"),("Görüşmek üzere","Ko’rushguncha"),
("Güle güle","Xayr"),("Hoşça kal","Yaxshi qoling"),("Hoş geldiniz","Xush kelibsiz"),
("Hoş bulduk","Xush ko’rdik"),("Elveda!","Alvido!"),("Afiyet olsun!","Osh bo’lsin!"),
("Affedersiniz","Uzr"),("Acaba","Mabodo"),("Peki","Xo’p"),("Maalesef","Afsuski"),
("Lütfen","Iltimos / Marhamat"),("Buyurun","Marhamat"),("Önemli değil","Hech qisi yo’q"),
("Özür dilerim","Kechirim so’rayman"),("Eline sağlık","Qo’lingiz dard ko’rmasin"),
("Haydi tanışalım","Keling, tanishaylik"),("Arkadaş","O’rtoq"),("Çanta","Sumka"),
("Okul","Maktab"),("Kedi","Mushuk"),("Bebek","Bola"),("Ayakkabı","Oyoq kiyimi"),
("Bardak","Stakan"),("Bilgisayar","Komputer"),("Ne","Nima"),("Televizyon","Televizor"),
("Cep telefonu","Mobil telefon"),("Fotoğraf makinesi","Foto apparati"),("Çorap","Paypoq"),
("Nereli?","Qayerlik?"),("Öğrenci","O’quvchi"),("Öğretmen","O’qituvchi"),("Şoför","Haydovchi"),
("Hemşire","Hamshira"),("Balıkçı","Baliqchi"),("Bahçıvan","Bog’bon"),("Memur","Ma’mur"),
("Var","Bor"),("Yok","Yo’q"),("Sınıf","Sinif"),("Herkes","Hamma"),("Sıra","Navbat , parta"),
("Kanepe","Divan"),("Sandalye","Stul"),("Masa","Stol"),("Lamba","chiroq"),("Harita","Xarita"),
("Silgi","O’chirg’ich"),("Askı","Ilgich"),("Cetvel","Chizg’ich"),("Polis","Politsiyachi"),
("Top","Koptok"),("Kalem","Qalam"),("Evet","Ha"),("Hayır","Yo’q"),("Değil","Emas"),
("Açık","1.Yoniq 2. ochiq"),("Kapalı","1.O’chiq 2. yopiq"),("Uzun","uzun"),
("Kısa","Qisqa , kalta"),("İnce","Yupqa"),("Kalın","Qalin"),("Büyük","Kata"),
("Küçük","Kichik"),("Sözlük","Lug’at"),("Bavul","Chemadan"),("Saksı","Tuvak"),
("Gözlük","Ko’zoynak"),("Cüzdan","Hamyon"),("Ev","Uy"),("Ekmek","Non"),
("Kahvaltı","Ertalabki nonushta"),("Başka","Boshqa"),("Şey","Narsa"),("Çay","Choy"),
("Peynir","Pushloq"),("Yumurta","Tuxum"),("Bal","Asal"),("Zeytin","Zaytun"),
("Reçel","Murabbo"),("Kızarmış ekmek","Qizartirilgan non"),("Tereyağı","Sariyog’"),
("Pasta","Tort"),("Kümes","Tovuqxona"),("Boş yer","Bo’sh joy"),("Dil","Til"),
("Meslek","Kasb"),("Numara","Raqam"),("Terzi","Tikuvchi"),("Doğum yeri","Tug’ilgan joy"),
("Doğum tarihi","Tug’ilgan vaqti"),("E-posta","e-mail"),("Yetkili","Rasmiy xodim"),
("Müşteri","Mijoz"),("Yanlış","Xato"),("Bulmak","Topmoq"),("Hangisi?","Qaysi biri?")
],
2: [
("Kaç?","Nechta?"),("Nerede?","Qayerda?"),("Kardeş","Aka-uka"),("Ağabey","Aka"),
("Çok","1.Juda 2.ko’p"),("Lise","Litsey"),("Baba","Dada"),("Ev hanımı","Uy Bekasi"),
("Kız kardeş","Qiz ukasi"),("Avukat","Advokat"),("Koca","Er"),("Çocuk","Bola,farzand"),
("Aile","Oila"),("Karı","Rafiqa"),("Yeğen","Jiyan"),("Damat","Kuyov"),("Dede","Bobo"),
("Anneanne","Buvi"),("Abla","Apa"),("Hala","Amma"),("Teyze","Xola"),("Enişte","Yazna"),
("Ne söylüyor","Nima deyayapti?"),("Tahta","Doska"),("Bakmak","Qaramoq"),
("Göstermek","Ko’rsatmoq"),("Sağ","O’ng"),("Sol","Chap"),("İleri","Oldin"),("Geri","Orqa"),
("Gitmek","Ketmoq"),("Dönmek","Qaytmoq"),("Güzel","Chiroyli"),("Yatak odası","Yotoqxona"),
("Genç odası","Yoshlar o’tiradigan xona"),("Mutfak","Oshxona"),("Salon","Salon"),
("Elbise dolabı","Kiyim jovoni"),("Koltuk","Kreslo"),("Takım","Nabor ,komplekt ,guruh"),
("Sehpa","Qahva stoli"),("Buzdolabı","Muzlatgich"),("Oturma odası","Mehmonxona"),
("Çalışma masası","Ish stoli"),("Gardırop","Shkaf,garderob"),("Tablo","Tablo(devorga ilingan rasm)"),
("Halı","Gilam"),("Küvet","Vanna"),("Havlu","Sochiq"),("Perde","Parda"),("Fırın","Duxovka"),
("Ayna","Ko’zgu"),("Tencere","Qozon"),("Sepet","Savat"),("Ağaç","Daraxt"),("Meyve","Meva"),
("Hastane","Kasalxona"),("Beyaz","Oq"),("Sarı","Sariq"),("Kırmızı","Qizil"),("Mavi","Ko’k"),
("Yeşil","Yashil"),("Siyah","Qora"),("Turuncu","Olov rang(sabzi rang)"),("Mor","To’q qizil"),
("Kahverengi","Jigarrang"),("Gri","kulrang"),("Lacivert","Quyuq ko’krang"),("Pembe","Pushti"),
("Kiraz","Gilos"),("Yaprak","Barg"),("Bahçe","Bog’"),("Et","Go’sht"),("Pişirmek","Pishirmoq"),
("Hazırlamak","Tayyorlamoq"),("Yardım etmek","Yordam bermoq"),("Mutlu","Xursand"),
("Yapmak","Bajarmoq"),("Koşmak","Yugurmoq"),("Söylemek","Aytmoq"),("Yazmak","Yozmoq"),
("Uyumak","Uxlamoq"),("Yazı","Yozuv"),("Şarkı","Qo’shiq"),("Maç","O’yin"),("Başlamak","Boshlamoq"),
("Kumanda","Pult"),("Sayın","Xurmatli"),("Seyirci","Tomoshabin"),("Pota altı","Basketbol Savati tagi"),
("Yakalamak","Tutib olmoq"),("Pas atmak","Raqiblarni aylanib o’tib to’pni uzatish"),
("Tutmak","1. biror narsani ushlamoq / 2. jamoa a’zosi bo’lish"),("Seyretmek","Ko’rmoq"),
("Gelmek","Kelmoq"),("Oturmak","1.biror narsaning ustiga / 2.yashamoq"),("Ağlamak","Yig’lamoq"),
("Gülmek","Kulmoq"),("Beklemek","Kutmoq"),("Atlamak","Sakramoq"),("Satranç","Shaxmat"),
("Sabah","Ertalab"),("erken","Barvaqt"),("Önce","Oldin"),("Sonra","Keyin"),
("Öğleyin","Tushlik vaqti"),("Öğle yemeği","Tushlik"),("Bitmek","Tugamoq"),
("Hep birlikte","Birgalikda"),("Misafir odası","Mehmon xona"),("Banyo","Yuvinish xonasi"),
("Cadde","Katta ko’cha"),("Site","Hudud"),("Fincan","Chashka"),("Yaşlı","Qari"),("Çift","Juft"),
("İçmek","Ichmoq"),("Çiçek","Gul"),("Gül","Tuvakdagi gul"),("Satmak","Sotmoq"),
("Taşımak","Tashimoq"),("Koklamak","Hidlamoq"),("Sulamak","Suv bermoq (gullarga)"),
("Havuç","Sabzi"),("Çizme","Etik"),("Giymek","Kiymoq"),("Yıkamak","Yuvmoq"),
("Sinema","Kinoteatr"),("Postane","Pochta"),("Müze","Muzey"),("Çıkmak","Chiqmoq"),
("Nine","Buvi"),("Amca","Amaki"),("Aynı","Xuddi"),("Apartman","Ko’p qavatli bino"),
("Gibi","Kabi , dek"),("Önemli","Muhim"),("Sokak","Ichki ko’cha"),("Mağaza","Magazin"),
("Pencere","Oyna"),("Dışarı","Tashqari"),("Armut","Nok"),("Kucak","Quchoq"),
("Düşmek","1.Yiqilmoq / 2. Tushmoq"),("Dayı","Tog’a")
],
3: [
("Günlük hayat","Kundalik turmush"),("Dün","Kecha"),("Ne zaman?","Qachon?"),
("Hafta sonu","Hafta oxiri (Shanba va yakshanba)"),("Otobüs","Avtobus"),("Hemen","Darhol"),
("Şanslısınız!","Omadlisiz!"),("Uçak kalkıyor","Samalyot uchyapdi"),("Şimdi","Hozir"),
("Anlamak","Anglamoq"),("Tek kişilik","Bir kishilik"),("Yolculuk …. sürüyor","Yo’lchilik …davom etadi"),
("Yaklaşık","Qariyb"),("Ulaşmak","Yetishmoq"),("İyi yolculuklar!","Safaringiz bexatar bo’lsin!"),
("Egzersiz yapmak","Sport mashqlari bajarmoq"),("Yüzmek","Suzmoq"),("Dönmek","Qaytmoq"),
("Banyo yapmak","Dush qabul qilmoq"),("Ulaşım aracı","Transport vositalari"),
("Para çekmek","Pul yechib olmoq"),("Çalışmak","Ishlamoq"),("Yine","Yana"),("Rapor","Hisobot"),
("Toplantı","Majlis , yig’ilish"),("Yorulmak","Charchamoq"),("Daha sonra","Keyinroq"),
("..le / ile","Bilan"),("Mühteşem","Muhtasham"),("Heyecanlı","Hayajonli"),("Fırçalamak","Shotkalamoq"),
("Banka","Bank"),("Geçmek","O’tmoq"),("Çarşı","Usti yopiq bozor"),("Güneş açtı","Quyosh charaqladi"),
("Tren","Poyezd"),("Vapur","Yo’lovchi tashuvchi kema"),("Başbakan","Prezident"),("İş yeri","Ish joyi (ofis)"),
("Kırtasiye","Kanselyariya do’koni"),("Muz","Banan"),("Elma","Olma"),("Pantolon","Shim"),
("Gömlek","Ko’ylak"),("Gemi","Kema"),("Ütü","Dazmol"),("Ütülemek","Dazmollamoq"),
("Kapı","Eshik"),("Anahtar","Kalit"),("Valiz","Chamadon"),("Gelin","Kelin"),("Balon","Shar"),
("Karpuz","Tarvuz"),("Katmak","Qo’shmoq"),("Tuzsuz","Tuzsiz"),("Tuzlu","Tuzli"),
("Tuzluk","Tuzdon"),("fıstık","Xandon pista"),("Şekerlik","Shakardon"),
("Limonluk","Limonni suvini chiqaradigan"),("Evli","Uylangan/turmush qurgan"),
("Bekar","Bo’ydoq /turmush qurmagan"),("Pazartesi","Dushanba"),("Salı","Seshanba"),
("Çarşamba","Chorshanba"),("Perşembe","Payshanba"),("Cuma","Juma"),("Cumartesi","Shanba"),
("Pazar","Yakshanba"),("Hafta içi","Hafta ichi"),("Ayakkabılık","Oyoq kiyimlarini qo’yadigan jovon"),
("Arkası","Orqasi"),("Solmak","So’lmoq"),("Yeni","Yangi"),("Hediye etmek","Sovg’a qilmoq"),
("Kira","Ijara"),("Aramak","Qidirmoq"),("Özgeçmiş","Cv (rezyume)"),("Saat kaç?","Soat nechchi?"),
("Manav","Meva sabzavot sotuvchisi"),("Patates","Kartoshka"),("Hanımefendi","Xonim"),
("Borc","Qarz"),("Para üstü","Qaytim"),("Soğan","Piyoz"),("Şalgam suyu","Sholg’om suvi"),
("Bunlar","Bular"),("Kangal","O’ram"),("Demet","Bog’"),("Kalıp","Qolip"),("Adet","Dona"),
("Dilim","Tilim , bo’lak"),("Salkım","Shingil"),("Makarna","Makaron"),("Kumaş","Mato"),
("Arası","Orasi"),("Kuruş","Tiyin"),("Alışveriş","Xarid"),("Dolu","To’liq"),("Tepsi","Patnis"),
("Kuruyemiş","Qurutilgan meva va yong’oqlar"),("Misafir","Mehmon"),("Gözünüz aydın!","Ko’zingiz oydin!"),
("Sağ olun","Sog’ bo’ling (dard ko’rmang ma’nosida)"),("Kuzu","Qo’zichoq"),("Taze","Toza (svejiy)"),
("Kaça?","Qanchaga?"),("Peşin","Oldindan"),("Ucuz","Arzon"),("Pahalı","Qimmat"),("Erken","Barvaqt"),
("Mağaza","Xarid markazi(magazin)"),("Altın","Oltin"),("Gümüş","Kumush"),("Ama","Ammo, lekin"),
("Göstermek","Ko’rsatmoq"),("Kazak","Jemfer"),("Sohbet etmek","Suhbatlashmoq"),("Yarın","Ertaga"),
("Kolay gelsin!","Xormang!"),("Taksitli","Bo’lib-bo’lib to’lash"),("Hal","Ahvol"),
("Dunyaya gelmek","Dunyoga kelmoq"),("An","On, dam, lahza"),("Konser","Konsert"),
("İndirim","Chegirma"),("Ünlü","Mashhur"),("Uzun uzun","Uzun uzun"),("Alkışlamak","Olqishlamoq"),
("Eşleştirmek","Juftlashtirmoq"),("Dolaşmak","Aylanmoq(bozor)"),("Plan yapmak","Reja tuzmoq"),
("İçerı","ichkari"),("Lokanta","Restaurant"),("Yurt","Talabalar turar joyi"),("Mevsim","Fasl"),
("İlkbahar","Bahor"),("Sonbahar","Kuz"),("Yaz","Yoz"),("Kış","Qish"),("Şort","Shortik"),
("Ceket","Kurtka"),("Terlik","Shippak"),("Yelek","Nimcha"),("Atkı","Sharf"),("Eldiven","Qo’lqop"),
("Hırka","Kardigan(tugmalik jemfer)"),("Tişört","Futbolka"),("Yazlık","Yozlik"),("Kışlık","Qishlik"),
("Mevsimlik","Mavsumiy"),("Giysi","Kiyim"),("Tercih etmek","Afzal ko’rmoq"),("Koyu","Quyuq"),
("Güle güle kullan!","Yaxshi kunlaringda foydalan!"),("Bereket versin!","Barakat bersin!"),
("Üstü kalsın","Qaytimi shartmas"),("Yıl","Yil"),("Sene","Yil"),("Çorba","Sho’rva"),
("Sıcak","Issiq"),("Soğuk","Sovuq"),("Beğenmek","Yoqtirmoq")
],
4: [
("Çevremiz","Atrofimiz"),("Sokak","Ko’cha"),("Daire","Xonadon"),("Yönetici","Boshqaruvchi"),
("Büfe","Bufet"),("Gazete","Gazeta"),("Muhtar","Boshliq"),("Muhtarlık","Boshliq idora"),
("Kat","Qavat"),("Karşı","Qarama qarshı"),("Rahatsız etmek","Bezovta qilmoq"),("Aşağı","Past"),
("Rica ederim","Arzimaydi"),("Düzenli","Tartibli (odatiy)"),("Başlıklı","Kapyushonlik"),
("Civciv","Jo’ja"),("İlk","Ilk , dastlabki"),("Çalışkan","Ishchan"),("Futbol takımı","Futbol guruhi"),
("Kantin","Kafeteriy"),("Kültür merkezi","Madaniyat markazi"),("Bakkal","Market"),("Bulvar","Xiyobon"),
("Vazo","Vaza"),("Arası","Orasi"),("Önü","Old tarafi"),("Yönler","Taraflar"),("Kuzey","Shimol"),
("Doğu","Sharq"),("Batı","G’arb"),("Güney","Janub"),("Üzeri","Usti"),("Yan yana","Yonma – yon"),
("Kredi","Kredit"),("İdare","Idora"),("Sonu","Oxiri"),("Dan a kadar","Dan gacha"),("Tezgah","Rasta"),
("Pazarcı","Bozorchi"),("Sebze","Sabzavot"),("Poşet","Paket(salafan)"),("Tamamen","Butunlay"),
("Asansör","Lift"),("İlişki","Aloqa"),("Hırsızlık","O’g’rilik"),("Müsait","Bo’sh"),
("Kuru fasulye","Quruq loviya"),("Pilav","Osh"),("Kadın","Ayol"),("Ev sahibi","Uy egasi"),
("Köpek","It"),("Türbe","Masjid"),("Köy","Qishloq"),("Eğitim","Ta’lim"),("Gibi","Kabi"),
("Çeşitli","Turli xil"),("Yetiştirdi","Yetishtirmoq"),("Karnım acıktı","Qornim och qoldi"),
("Hepimizin","Hammamizning"),("Ödemek","To’lamoq"),("Bendensiniz","Men bilansiz"),
("Ne arzu edersiniz?","Ko’nglingiz nimani tusayapdi?"),("Patlıcan","Baqlajon"),
("Maden suyu","Mineral suv"),("Acılı","Achchiq"),("Sipariş","Buyurtma"),("Not etmek","Yozib olmoq"),
("Tatlı","1.Shirinlik 2.shirin"),("Karar vermek","Qaror qilmoq"),("Yenge","Yanga"),("Bedava","Bepul"),
("Obez","Haddan tashqari semizlik(kasallik)"),("Sayı","Son"),("Hızla","Tezlik bilan"),
("Artmak","Ortmoq"),("Tedavi etmek","Davolamoq"),("Boş durmak","Bo’sh o’tirmoq"),
("Saygılı","Xurmatli"),("Davranmak","Muomalada bo’lmoq"),("Okşamak","Silamoq"),
("Hediye","Hadiya (sovg’a)"),("Yalan","Yolg’on"),("Garson","Ofitsiant"),("Hesap","Hisob"),
("Yazar","Yozuvchi"),("Bisiklet","Velosiped")
],
5: [
("Evladım","Bolajonim"),("Mühendis","Muhandis"),("Çocukluğumda","Bolaligimda"),
("Birçok defa","Bir necha marta"),("Anaokul","Bog’cha"),("İlkokul","Boshlang’ich maktab"),
("Mezun olmak","Tugatmoq (o’qishni)"),("Etrafında","Atrofida"),("Zayıf","Ozg’in"),("Çelimsiz","Nimjon"),
("Kenar","Chet"),("Ödev","Uyga vazifa"),("Pek","Ancha"),("Çimen","Gazon"),("Yalnız","Yolg’iz"),
("Canım …. istemiyor","Jonim ……tusamayabdi"),("Daha çok var","Hali ancha bor"),
("Susam","Simit donasi (bir susam simit)"),("Cam","Oyna"),("Sivri","O’tkir"),("Kıvırcık","Jingalak"),
("Çabuk","Tez"),("Avlu","Hovli"),("Bir de","Yana"),("Üzüntü","Hafagarchilik"),("Örtü","Yopinchiq"),
("Kaybetmek","Yo’qotmoq"),("Duvar","Devor"),("Alet","Asbob ,jihoz"),("Müdür","Mudir"),
("Bilin bakalım","Topingchi"),("Eczacı","Aptekachi"),("Sunucu","Teledasturni e’lon qiluvchi"),
("Berber","Erkaklar sartaroshi"),("Hasta","Kasal"),("Muayene","Ko’rik"),("İlaç","Dori"),("Eşya","Buyum"),
("Reçete","Doktor retsepti"),("Bilgi vermek","Ma’lumot /Xabar bermoq"),("Saç kesmek","Soch kestirish"),
("Kıyı","Qirg’oq"),("Göl","Ko’l"),("Baraj","Suv ombori"),("Uzun bir süre","Uzoq vaqt davomida"),
("Değiştirmek","Almashtirmoq"),("Kazanç","Topish – tutish"),("Seçmek","Tanlamoq"),
("Savunmak","Himoya qilmoq"),("Kutsal","Qutlug’ , muborak"),("Avukat","Advokat"),("Düdük","Hushtak"),
("Makas","Qaychi"),("İğne","1.Ukol 2. Igna"),("Boğazım acıyor","Tomog’im og’riyapti"),
("Ateş ölçmek","Haroratini o’lchamoq"),("Ciğer","O’pka"),("Bol bol","Ko’p ko’p"),
("Geçmiş olsun","O’tgani bo’lsin(o’tgani rost bo’lsin)"),("Geniş","Keng"),("En son","Eng oxirgi"),
("Sırt organ","Tashqi organ"),("Tavşan","Quyon"),("Kaş","Qosh"),("Baş","Bosh"),("Saç","Soch"),
("Göz","Ko’z"),("Ağız","Og’iz"),("Kulak","Quloq"),("Burun","Burun"),("Gövde","Gavda"),
("Boyun","Bo’yin"),("Göğüs","Ko’ks"),("Karın","Qorin"),("Bacak","Son(tizzadan yuqori qisim)"),
("Ayak","Oyoq"),("Diz","Tizza"),("Tırnak","Tirnoq"),("Kol","Qo’l"),
("El","Bilakkacha bo’lgan qo’l qismi"),("Omuz","Yelka"),("Dirsek","Tirsak"),("Parmak","Barmoq"),
("Armut","Nok"),("Zürafa","Jirafa"),("Zor","Qiyin"),("Yarasa","Ko’rshapalak"),("Eşofman","Sport kiyimi"),
("Üniforma","Yuniforma"),("Genellikle","Odatda"),("Uygun","Mos"),("Göre","Ko’ra"),("Yönetmen","Rejissyor"),
("Bilim adamı","Olim"),("Arkeolog","Arxeolog"),("Aşçı","Oshpaz"),("İtfaiyeci","O’t o’chiruvchi"),
("Marangoz","Duradgor"),("Mesleğimizin dışında","Kasbimizdan tashqarida"),("Evcil hayvan","Uy hayvoni"),
("Film izlemek","Film ko’rmoq"),("Canım sıkıldı","Zerikdim"),("Sinirlenmek","Asabiylashmoq"),
("Düzenlemek","Tayyorlamoq"),("Acele etmek","Shoshilmoq"),("Sakin","Sokin"),("Karamsar","Pessimist"),
("Ela","Qo’yko’z (to’q jigarrang)"),("Bulaşık yıkamak","Idish tovoq yuvmoq"),
("Kaydetmek","Qayd etmoq"),("Kopyalamak","Nusxalamoq"),("Yapıştırmak","Yopishtirmoq"),
("Sayfa","Sahifa"),("Öz geçmiş","Biografiya"),("İlgi alanı","Qiziqish aurasi"),
("Kuaför","Ayollar sartaroshi"),("İkram etmek","Ikrom etmoq(kelgan mehmonga choy yoki qahva berish)"),
("Yakışmak","Yarashmoq"),("Anlaştık!","Kelishdik!"),("Harika","Ajoyib"),("..Da / …de","Ham"),
("Geleneksel","Odatiy"),("Bakırcılık","Misgarlik"),("Süs","Bezak"),("Dağcılık","Tog’chilik"),
("Web sayfa","Veb sahifa"),("Neşeli","Kayfiyati chog’ (xursand)"),
("Çaydanlık","Chovgun (choy qaynatish uchun ishlatiladigan kata choynik)"),
("Uygarlık","Yodgorlik , tarihiy topilma")
],
6: [
("Ulaşım","Transport"),("Sayılı","Sanoqli"),("Uçuş modu","Uchish rejimi(avtopolyot)"),
("Kaydırak","Sirpanchiq"),("Basınç","Bosim"),("Oksijen","Kislorod"),("Topuklu","Poshnali"),
("Herhangi bir","Istalgan bir"),("Acil","1.Tez 2.tez yordam"),("Salıncak","Arg’imchoq"),
("Şenlik","Festival"),("Savaş","Urush"),("Cep","Cho’ntak (Kisa)"),("Özellik","Xususiyat"),
("İptal olmak","Bekor bo’lmoq"),("Röter","Kechikish (samalyot yoki poyezd)"),("Öyleyse","Unday bo’lsa"),
("Kibar","Xushmuomala"),("Gecikme","Kechikish"),("Havaalanı","Aeroport"),("Sıkışık","Tiqilinch"),
("Emniyet kuralları","Yo’l harakati qoidalari"),("Hostes","styuardessa"),
("Emniyet kemeri","Xavfsizlik Kamari"),("Çıkış kapısı","Chiqish eshigi"),("Kolay","Oson"),
("Şehir merkezi","Shahar markazi"),("Yaklaşık","Qariyb"),("Basamak","1.Zina 2.bosqich ,etap"),
("Tercih","Tanlov"),("Niçin?","Nima uchun?"),("Yükselmek","Ko’tarilmoq"),("Hazırlık","Tayyorgarlik"),
("Yarışma","Musobaqa"),("Dolmuş","Marshrutka"),("Otomobil","Avtomobil"),("Durum","Vaziyat , ahvol"),
("Şemsiye","Zontik"),("Esmek","Esmoq"),("Sisli","Tumanli"),("Sağanak yağışlı","Yomg’ir sepalashi"),
("Rüzgarlı","Shamolli"),("Fırtınalı","Bo’ronli"),("Dondurma","Muzqaymoq"),("Sararmak","Sarg’aymoq"),
("Uçurtma","Varrak"),("Dondurucu","Sovuq qottiradigan"),("Ilık","Iliq"),("Bunaltıcı","Aynigan"),
("Kalabalık","Gavjum"),("Gök gürledı","Osmon gumburladi"),("Gökkuşağı","Kamalak"),("Karışık","Aralash"),
("Emlakçı","Mulk agenti"),("Kullanımdan kalktı","Iste’moldan chiqdi"),("Fayton","Ot arava"),
("Tekerlek","G’ildirak"),("Yasak","Cheklov"),("Temel","Asosiy"),("Serin","Salqin"),
("Kartopu","Qor to’pi"),("Etkilemek","Ta’sir ko’rsatmoq"),("Raf","Polka"),("Parçalı bulutlu","Parcha bulutlik")
],
7: [
("İletişim","Aloqa"),("Haberleşmek","Habarlashmoq"),("Sık sık","Tez -tez"),("Doğum günü","Tug’ilgan kuni"),
("Kutlamak","Qutlamoq"),("İcat etmek","Ijod qilmoq"),("Telefon hattı","Telefon liniyasi"),
("Sadece","Faqatgina"),("Kısaltmak","Qisqartirmoq"),("Diyerek","Deb"),("Karşılık vermek","Javob ko’rsatmoq"),
("Sesi yukseldi","Baqirib gapirdi"),("Çekmek","Tortmoq"),("Hiç","Aslo , hech qancha"),("Veya","Yoki"),
("Merak etmiyor","Qiziqmoq (birovni ahvoli bilan , nima qilayatgani bilan qiziqmoq)"),
("Ortaya çıkmak","Fosh bo’lmoq"),("İletişim araçları","Aloqa vositalari"),("Duman","Tutun"),
("Güvercin","kabutar"),("Manyetolu telefon","Magnitli telefon"),
("Çevirmeli telefon","Go’shakli telefon(raqamlarni bitta bitta aylantirib qo’ng’iroq qiladigan telefon)"),
("Tuşlu telefon","Tugmali telefon"),("Tuşlu cep telefonu","Tugmali mobil telefon"),
("Dokunmatik cep telefonu","Sensor telefon"),("Telefon etmek","Qo’ng’iroq qilmoq"),
("Telefon çalmak","Qo’ng’iroq kelmoq"),("Telefonla aramak","Telefon bilan qo’ng’iroq qilmoq"),
("Telefonla görüşmek","Telefon bilan gaplashmoq"),("Telefonla konuşmak","Telefon bilan gaplashmoq"),
("Tabii","Albatta(tabiiy)"),("Konuşma kesildi","Suhbat kesildi"),("Değil mi?","Emasmi?"),
("Hala","Haliyam"),("Şarji bitti","Quvvati tugadi (telefonning)"),("Hatırlamak","Eslamoq"),
("Gidiş- dönüş","Borish-qaytish"),("Tekrar","Takror"),("İletişim kurmak","Aloqa qurmoq"),
("Mesaj","Xat"),("Mesaj göndermek","Xat yubormoq"),("Daha","Ancha"),("Vitrin","Vitrina(reklama)"),
("Böyle","Shunday"),("Elbette","Albatta"),("Ayrıca","Bundan tashqari"),("O halde","Unday bo’lsa"),
("Nakit","Naqd"),("Dayanıklı","Chidamli"),("Batarya","Batareya"),("Bence","Menimcha …a göre …ga ko’ra"),
("Yorgun","Xorg’in (charchagan)"),("Birkaç","Bir nechta"),("Satır","Satr"),("Çalıştırmak","Ishlatmoq"),
("Kasa","Kassa"),("Kablo","Kabel"),("Klavye","Klaviatura"),("Fare","Sichqoncha"),
("Hoparlör","Karnay(kalonka)"),("Monitör","Monitor(ekran)"),("Saldırgan","Hujum qiladigan (hayvon)"),
("Yavaş","Sekin"),("Hızlı","Tez"),("Sabırlı","Sabirli"),("Zehirli","Zaharli"),("Sonuç","Natija"),
("Belli olmak","Aniq bo’lmoq"),("Kolay","Oson"),
("Bilgi kirliliği","Ma’lumotdan zaharlanish(keraksiz ma’lumotlarning inson ongiga yomon ta’sir qilishi)"),
("Mutluluk duymak","Xursand bo’lmoq"),("Eğlenmek","O’ynab kulmoq"),("İyİkİ doğdun!","Tug’ilgan kuning bilan!"),
("Değerli","Qadirli"),("Yan","Yon taraf"),("Davetiye","Taklifnoma"),("Eksik","Eksik (yetishmaydigan)"),
("Bilgi","Ma’lumot"),("Gerçekten","Haqiqattan"),("Devamlı","Davomli"),("Kendisi","O’zi"),
("İddiaya girmek","Garov o’ynamoq"),("Düğün","To’y"),("Aslında","Aslida"),("Kusura bakma!","Aybga buyurma!"),
("Yoğun","Band"),("Zaten","Zotan"),("Bu yüzden","Shuning uchun"),("Hazır","Tayyor"),("Tam zamanı","Ayni vaqti"),
("Söyle artık!","Aytaqol endi!"),("Tek tek","Bir bir"),("Sakin olmak","Tinchlanmoq"),("Aday","Nomzod"),
("Açıklamak","Oydinlik kiritmoq"),("Belli","Aniq"),("Postacı","Xat tashuvchi"),("Haberci","Habar yetkazuvchi"),
("Haberleşme","Habarlashmoq"),("Tek başına","Yolg’iz (bir o’zi)"),("Haber götürdü","Habar olib bordi"),
("Haber taşıdı","Habar tashidi(yetkazdi)"),("Görev","Vazifa"),("Acil haber","shoshilinch habar"),
("Normal","Normal"),("Ulak","Xabarchi"),("Nadiren","Kamdan kam"),("Seyrek","Kamdan kam"),
("Kaygılı","Havotirlangan"),("Öfkeli","Jahldor"),("Balina","Kit (baliq)")
],
8: [
("Fıkra","Latifa"),("Komik","Kulgili"),("Ulaşmak","Yetib bormoq , yetmoq"),("Bulmak","Topmoq"),
("Fotoğraf çektirmek","Rasmga tushirmoq"),("Tur","Tur"),("Gezi","Sayohat"),("Doğa","Tabiat"),
("Keşf","Kashf"),("Olur","Mayli"),("Semt","Okrug(tuman)"),("İlçe","Tuman"),("Mola vermek","Dam bermoq"),
("Yayla","Tepalik"),("Sincap","Olmaxon"),("Cevizli","Yong’oqli"),("Halay çekmek","Halay raqsiga tushmoq"),
("Misket oynamak","Misket o’ynamoq (ko’cha o’yini …toshni toshga urib o’ynash)"),
("Şimdilik","Hozirchalik"),("Acenta","Agentlik"),("Yemek de dahil","Ovqatlanishi ham ichida"),
("Yöresel yemekler","Hududlararo (milliy)"),("Yüksek","Yuksak"),("Misafirperver","Mehmondo’st"),
("Peribacaları","Qoyaliklar (vodiylardan oqib kelgan suvlarning yerni yemirishidan paydo bo’lgan qoyaliklari)"),
("Ailece","Oilaviy"),("Pusula","kompass"),("Kamp çadırı","Kampus (sayohat chodiri)"),
("Böylece","Shunday qilib"),("Daha iyi","Ancha yaxshi"),("Bu kez","Bu safar"),("Doya doya","To’yib to’yib"),
("Doğru","To’g’ri"),("Hoplamak","Sakramoq"),("Daha pek çok","Yanada köp"),("Kumsal","Qumlik"),
("Güneşlenmek","Quyoshda toblanmoq"),("Buz gibi","Muzdek"),("Keyfini çıkarmak","Rohatlanmoq"),
("Kar adam","Qordan odam (qordan yasalgan qorbobo)"),("Şömine","Kamin"),
("Kendini geliştirmek","O’zini kelishtirmoq"),("İncelemek","Ko’rib chiqmoq"),("İlgili","Tegishli"),
("Her şeyin başı sağlık","Hamma ishning boshi sog’lik"),("Neyi?","Nimani?"),
("Katkı sağlamak","O’z hissasini qo’shmoq"),("Pansiyon","Hostel"),("Harçlık","Bayram puli"),
("Tamam tamam","Bo’ldi bo’ldi (gap yo’q)"),("Diyet","Dieta"),("Zil çaldı","Eshik qo’ng’irog’i chalindi"),
("Nice senelere!","Uzoq yillar uchun!"),("Seslenme","chaqirmoq"),("Sevgili","Sevgili , aziz"),
("Yalnız","1.Faqat 2.yolg’ız"),("Melek","Farishta"),("Üzmeyelim!","Xafa qilmaylik!"),
("Ara sıra","Ora sira"),("Hüzünlü","Xafa"),("Uyan!","Uyg’on!"),("Haydi, kalk!","Qani, tur!"),
("Birden","Birdan"),("Kendime geldim","O’zimga keldim"),("Abdest","Tahorat"),("Komşu","Qo’shni"),
("Değişik","Farqli, boshqacha"),("Şeker","Konfet"),("Çekmece","Tortma")
]
}

ALL_WORDS = [w for unit in WORDS.values() for w in unit]

# =========================================================
# DATABASE
# =========================================================
def connect():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            tests INTEGER DEFAULT 0,
            correct INTEGER DEFAULT 0,
            wrong INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            joined TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS group_scores(
            chat_id INTEGER,
            user_id INTEGER,
            first_name TEXT,
            username TEXT,
            correct INTEGER DEFAULT 0,
            wrong INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            PRIMARY KEY(chat_id,user_id)
        )""")

def save_user(user):
    if not user:
        return
    with connect() as c:
        c.execute("""INSERT INTO users(user_id,first_name,username,joined)
                     VALUES(?,?,?,?)
                     ON CONFLICT(user_id) DO UPDATE SET
                     first_name=excluded.first_name, username=excluded.username""",
                  (user.id, user.first_name or "Foydalanuvchi", user.username or "",
                   datetime.now(timezone.utc).isoformat()))

def add_result(user_id, correct, wrong):
    with connect() as c:
        c.execute("""UPDATE users SET tests=tests+1, correct=correct+?,
                     wrong=wrong+?, points=points+? WHERE user_id=?""",
                  (correct, wrong, correct * 10, user_id))

def add_group_score(chat_id, user, is_correct):
    save_user(user)
    with connect() as c:
        c.execute("""INSERT INTO group_scores(chat_id,user_id,first_name,username,correct,wrong,points)
                     VALUES(?,?,?,?,?,?,?)
                     ON CONFLICT(chat_id,user_id) DO UPDATE SET
                     first_name=excluded.first_name, username=excluded.username,
                     correct=correct+excluded.correct,
                     wrong=wrong+excluded.wrong,
                     points=points+excluded.points""",
                  (chat_id, user.id, user.first_name or "Foydalanuvchi", user.username or "",
                   1 if is_correct else 0, 0 if is_correct else 1, 10 if is_correct else 0))

# =========================================================
# MENYULAR
# =========================================================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Test boshlash", callback_data="test"),
         InlineKeyboardButton("📚 Unit tanlash", callback_data="units")],
        [InlineKeyboardButton("🎲 Aralash test", callback_data="random"),
         InlineKeyboardButton("🏆 Reyting", callback_data="ranking")],
        [InlineKeyboardButton("📊 Natijalarim", callback_data="results"),
         InlineKeyboardButton("👤 Profil", callback_data="profile")],
        [InlineKeyboardButton("👥 Guruh testi", callback_data="group"),
         InlineKeyboardButton("ℹ️ Yordam", callback_data="help")],
    ])

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Bosh menyu", callback_data="home")]])

def unit_menu(prefix="u"):
    rows = []
    for a in range(1, 9, 2):
        rows.append([
            InlineKeyboardButton(f"{a}️⃣ Unit {a}", callback_data=f"{prefix}:{a}"),
            InlineKeyboardButton(f"{a+1}️⃣ Unit {a+1}", callback_data=f"{prefix}:{a+1}")
        ])
    rows.append([InlineKeyboardButton("🔀 Barcha unitlar", callback_data=f"{prefix}:0")])
    rows.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="home")])
    return InlineKeyboardMarkup(rows)

def count_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("5 ta", callback_data="n:5"),
         InlineKeyboardButton("10 ta", callback_data="n:10"),
         InlineKeyboardButton("20 ta", callback_data="n:20")],
        [InlineKeyboardButton("30 ta", callback_data="n:30"),
         InlineKeyboardButton("50 ta", callback_data="n:50")],
        [InlineKeyboardButton("⬅️ Unitlarga", callback_data="units"),
         InlineKeyboardButton("🏠 Bosh menyu", callback_data="home")]
    ])

def direction_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇷 → 🇺🇿", callback_data="d:tu"),
         InlineKeyboardButton("🇺🇿 → 🇹🇷", callback_data="d:ut")],
        [InlineKeyboardButton("🔀 Aralash", callback_data="d:mix")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="home")]
    ])

# =========================================================
# TEST
# =========================================================
def pool_for(unit):
    return ALL_WORDS if unit == 0 else WORDS.get(unit, [])

def build_question(pair, direction):
    tr, uz = pair
    d = random.choice(["tu", "ut"]) if direction == "mix" else direction
    if d == "tu":
        question = f"🇹🇷 <b>{tr}</b>\n\nBu so‘zning o‘zbekcha ma’nosi qaysi?"
        correct = uz
        wrong_pool = list(dict.fromkeys(x[1] for x in ALL_WORDS if x[1] != uz))
    else:
        question = f"🇺🇿 <b>{uz}</b>\n\nBuning turkcha tarjimasi qaysi?"
        correct = tr
        wrong_pool = list(dict.fromkeys(x[0] for x in ALL_WORDS if x[0] != tr))
    choices = random.sample(wrong_pool, min(3, len(wrong_pool))) + [correct]
    random.shuffle(choices)
    return question, correct, choices

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)
    text = (
        "🇹🇷 <b>TURKCHA TEST BOT</b> 🇺🇿\n\n"
        "A1 darajadagi turkcha–o‘zbekcha lug‘at bo‘yicha test.\n\n"
        "Kerakli bo‘limni tugma orqali tanlang 👇"
    )
    await update.effective_message.reply_text(text, reply_markup=main_menu(), parse_mode="HTML")

async def send_next_private(query, context):
    s = context.user_data.get("quiz")
    if not s:
        await query.message.reply_text("Test topilmadi.", reply_markup=main_menu())
        return
    if s["index"] >= len(s["questions"]):
        correct, wrong = s["correct"], s["wrong"]
        add_result(query.from_user.id, correct, wrong)
        total = correct + wrong
        pct = round(correct * 100 / total) if total else 0
        context.user_data.pop("quiz", None)
        await query.message.reply_text(
            f"🏁 <b>Test tugadi!</b>\n\n"
            f"✅ To‘g‘ri: <b>{correct}</b>\n"
            f"❌ Xato: <b>{wrong}</b>\n"
            f"🎯 Natija: <b>{pct}%</b>\n"
            f"⭐ Ball: <b>{correct * 10}</b>",
            reply_markup=main_menu(), parse_mode="HTML")
        return

    pair = s["questions"][s["index"]]
    qtext, correct, choices = build_question(pair, s["direction"])
    s["answer"] = correct
    s["locked"] = False
    s["index"] += 1

    rows = [[InlineKeyboardButton(ch, callback_data=f"a:{i}")]
            for i, ch in enumerate(choices)]
    s["choices"] = choices
    await query.message.reply_text(
        f"📝 <b>Savol {s['index']}/{len(s['questions'])}</b>\n\n{qtext}",
        reply_markup=InlineKeyboardMarkup(rows), parse_mode="HTML")

async def begin_private(query, context):
    s = context.user_data.get("setup", {})
    unit = s.get("unit", 0)
    count = s.get("count", 10)
    direction = s.get("direction", "mix")
    pool = pool_for(unit)
    count = min(count, len(pool))
    questions = random.sample(pool, count)
    context.user_data["quiz"] = {
        "questions": questions, "index": 0, "correct": 0, "wrong": 0,
        "direction": direction, "answer": None, "choices": [], "locked": False
    }
    await query.message.reply_text("🚀 Test boshlandi!")
    await send_next_private(query, context)

# =========================================================
# CALLBACK
# =========================================================
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    save_user(q.from_user)
    data = q.data

    if data == "home":
        await q.edit_message_text("🇹🇷 <b>TURKCHA TEST BOT</b> 🇺🇿\n\nBo‘limni tanlang 👇",
                                  reply_markup=main_menu(), parse_mode="HTML")
        return

    if data in ("test", "units"):
        context.user_data["setup"] = {}
        await q.edit_message_text("📚 <b>Qaysi unitdan test ishlaysiz?</b>",
                                  reply_markup=unit_menu("u"), parse_mode="HTML")
        return

    if data == "random":
        context.user_data["setup"] = {"unit": 0}
        await q.edit_message_text("🔢 <b>Savollar sonini tanlang:</b>",
                                  reply_markup=count_menu(), parse_mode="HTML")
        return

    if data.startswith("u:"):
        context.user_data.setdefault("setup", {})["unit"] = int(data.split(":")[1])
        await q.edit_message_text("🔢 <b>Savollar sonini tanlang:</b>",
                                  reply_markup=count_menu(), parse_mode="HTML")
        return

    if data.startswith("n:"):
        context.user_data.setdefault("setup", {})["count"] = int(data.split(":")[1])
        await q.edit_message_text("🔄 <b>Test yo‘nalishini tanlang:</b>",
                                  reply_markup=direction_menu(), parse_mode="HTML")
        return

    if data.startswith("d:"):
        context.user_data.setdefault("setup", {})["direction"] = data.split(":")[1]
        await begin_private(q, context)
        return

    if data.startswith("a:"):
        s = context.user_data.get("quiz")
        if not s or s.get("locked"):
            return
        idx = int(data.split(":")[1])
        if idx >= len(s["choices"]):
            return
        chosen = s["choices"][idx]
        correct = s["answer"]
        s["locked"] = True
        if chosen == correct:
            s["correct"] += 1
            result = "✅ <b>To‘g‘ri!</b>"
        else:
            s["wrong"] += 1
            result = f"❌ <b>Xato.</b>\n\n✅ To‘g‘ri javob: <b>{correct}</b>"
        await q.edit_message_reply_markup(reply_markup=None)
        await q.message.reply_text(
            result,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➡️ Keyingi savol", callback_data="next")],
                [InlineKeyboardButton("🏠 Testni tugatish", callback_data="home")]
            ]),
            parse_mode="HTML")
        return

    if data == "next":
        try:
            await q.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        await send_next_private(q, context)
        return

    if data == "results":
        with connect() as c:
            r = c.execute("SELECT * FROM users WHERE user_id=?", (q.from_user.id,)).fetchone()
        tests = r["tests"] if r else 0
        correct = r["correct"] if r else 0
        wrong = r["wrong"] if r else 0
        points = r["points"] if r else 0
        total = correct + wrong
        pct = round(correct * 100 / total) if total else 0
        await q.edit_message_text(
            f"📊 <b>Natijalarim</b>\n\n📝 Testlar: <b>{tests}</b>\n"
            f"✅ To‘g‘ri: <b>{correct}</b>\n❌ Xato: <b>{wrong}</b>\n"
            f"🎯 Aniqlik: <b>{pct}%</b>\n⭐ Ball: <b>{points}</b>",
            reply_markup=back_menu(), parse_mode="HTML")
        return

    if data == "profile":
        with connect() as c:
            r = c.execute("SELECT * FROM users WHERE user_id=?", (q.from_user.id,)).fetchone()
        name = q.from_user.first_name or "Foydalanuvchi"
        username = f"@{q.from_user.username}" if q.from_user.username else "yo‘q"
        points = r["points"] if r else 0
        await q.edit_message_text(
            f"👤 <b>Profil</b>\n\n👤 Ism: <b>{name}</b>\n"
            f"🔗 Username: <b>{username}</b>\n🆔 ID: <code>{q.from_user.id}</code>\n"
            f"⭐ Umumiy ball: <b>{points}</b>",
            reply_markup=back_menu(), parse_mode="HTML")
        return

    if data == "ranking":
        with connect() as c:
            rows = c.execute("SELECT * FROM users ORDER BY points DESC, correct DESC LIMIT 10").fetchall()
        text = "🏆 <b>TOP 10</b>\n\n"
        if not rows:
            text += "Hali natijalar yo‘q."
        else:
            medals = ["🥇","🥈","🥉"]
            for i, r in enumerate(rows, 1):
                mark = medals[i-1] if i <= 3 else f"{i}."
                uname = f"@{r['username']}" if r["username"] else r["first_name"]
                text += f"{mark} {uname} — <b>{r['points']} ball</b>\n"
        await q.edit_message_text(text, reply_markup=back_menu(), parse_mode="HTML")
        return

    if data == "help":
        await q.edit_message_text(
            "ℹ️ <b>Yordam</b>\n\n"
            "📝 Test boshlash — unit va savollar sonini tanlaysiz.\n"
            "🎲 Aralash test — barcha unitlardan savol beradi.\n"
            "🇹🇷→🇺🇿 yoki 🇺🇿→🇹🇷 yo‘nalishni tanlash mumkin.\n"
            "🏆 Reyting — umumiy TOP 10.\n"
            "👥 Guruh testi — bot guruhda quiz-poll yuboradi.\n\n"
            "Guruhda <code>/grouptest</code> yuboring va tugmalardan unitni tanlang.",
            reply_markup=back_menu(), parse_mode="HTML")
        return

    if data == "group":
        if q.message.chat.type in ("group", "supergroup"):
            await q.edit_message_text("👥 <b>Guruh testi uchun unit tanlang:</b>",
                                      reply_markup=unit_menu("gu"), parse_mode="HTML")
        else:
            await q.edit_message_text(
                "👥 <b>Guruh testi</b>\n\nBotni guruhga qo‘shing, so‘ng guruhda "
                "<code>/grouptest</code> yuboring.\n\nBot quiz-poll shaklida savollar beradi.",
                reply_markup=back_menu(), parse_mode="HTML")
        return

    if data.startswith("gu:"):
        if q.message.chat.type not in ("group", "supergroup"):
            return
        unit = int(data.split(":")[1])
        context.chat_data["group_unit"] = unit
        await q.edit_message_text(
            f"👥 Unit: <b>{'Barchasi' if unit == 0 else unit}</b>\n\nSavollar sonini tanlang:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("5 ta", callback_data="gn:5"),
                 InlineKeyboardButton("10 ta", callback_data="gn:10"),
                 InlineKeyboardButton("20 ta", callback_data="gn:20")],
                [InlineKeyboardButton("🏠 Bosh menyu", callback_data="home")]
            ]), parse_mode="HTML")
        return

    if data.startswith("gn:"):
        if q.message.chat.type not in ("group", "supergroup"):
            return
        count = int(data.split(":")[1])
        unit = context.chat_data.get("group_unit", 0)
        pool = pool_for(unit)
        count = min(count, len(pool))
        context.chat_data["group_questions"] = random.sample(pool, count)
        context.chat_data["group_index"] = 0
        await q.edit_message_text(f"🚀 Guruh testi boshlandi! {count} ta savol.")
        await send_group_poll(q.message.chat_id, context)
        return

async def send_group_poll(chat_id, context):
    questions = context.chat_data.get("group_questions", [])
    idx = context.chat_data.get("group_index", 0)
    if idx >= len(questions):
        await context.bot.send_message(
            chat_id, "🏁 <b>Guruh testi tugadi!</b>\n\n🏆 Natijani ko‘rish uchun /grouptop",
            parse_mode="HTML")
        return

    tr, uz = questions[idx]
    wrongs = list(dict.fromkeys(x[1] for x in ALL_WORDS if x[1] != uz))
    options = random.sample(wrongs, 3) + [uz]
    random.shuffle(options)
    correct_idx = options.index(uz)

    msg = await context.bot.send_poll(
        chat_id=chat_id,
        question=f"{idx+1}/{len(questions)} — 🇹🇷 {tr}",
        options=options,
        type="quiz",
        correct_option_id=correct_idx,
        is_anonymous=False,
        explanation=f"To‘g‘ri javob: {uz}"
    )
    context.bot_data.setdefault("polls", {})[msg.poll.id] = {
        "chat_id": chat_id,
        "correct": correct_idx
    }
    context.chat_data["group_index"] = idx + 1
    # Keyingi savol tugmasi
    await context.bot.send_message(
        chat_id,
        "Javob bergach davom eting 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Keyingi savol", callback_data="g_next")]
        ])
    )

async def group_next_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    try:
        await q.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass
    await send_group_poll(q.message.chat_id, context)

async def poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = update.poll_answer
    info = context.bot_data.get("polls", {}).get(ans.poll_id)
    if not info or not ans.option_ids:
        return
    is_correct = ans.option_ids[0] == info["correct"]
    add_group_score(info["chat_id"], ans.user, is_correct)

async def grouptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)
    if update.effective_chat.type not in ("group", "supergroup"):
        await update.message.reply_text("Bu buyruqni guruh ichida ishlating.")
        return
    await update.message.reply_text("👥 <b>Guruh testi — Unit tanlang:</b>",
                                    reply_markup=unit_menu("gu"), parse_mode="HTML")

async def grouptop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ("group", "supergroup"):
        return
    with connect() as c:
        rows = c.execute("""SELECT * FROM group_scores WHERE chat_id=?
                            ORDER BY points DESC, correct DESC LIMIT 10""",
                         (update.effective_chat.id,)).fetchall()
    text = "🏆 <b>Guruh TOP 10</b>\n\n"
    if not rows:
        text += "Hali natijalar yo‘q."
    else:
        for i, r in enumerate(rows, 1):
            mark = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"{i}."
            name = f"@{r['username']}" if r["username"] else r["first_name"]
            text += f"{mark} {name} — <b>{r['points']}</b> ⭐ | ✅ {r['correct']} | ❌ {r['wrong']}\n"
    await update.message.reply_text(text, parse_mode="HTML")

async def special_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # g_next ni umumiy callbackdan oldin tutish uchun
    if update.callback_query.data == "g_next":
        await group_next_callback(update, context)
    else:
        await callback(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("ERROR:", context.error)

def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi. Tokenni kodga yozmang; hostingda BOT_TOKEN environment variable yarating."
        )
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("grouptest", grouptest))
    app.add_handler(CommandHandler("grouptop", grouptop))
    app.add_handler(CallbackQueryHandler(special_callback))
    from telegram.ext import PollAnswerHandler
    app.add_handler(PollAnswerHandler(poll_answer))
    app.add_error_handler(error_handler)
    print("Turkcha Test Bot ishga tushdi.")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=False)

if __name__ == "__main__":
    main()
