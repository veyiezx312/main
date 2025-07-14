from telethon import TelegramClient, events
import re
import asyncio
from datetime import datetime

api_id = 26666446
api_hash = '8bffd2731971ce8e3298efb31cda5252'

client = TelegramClient('user', api_id, api_hash).start()

# Hata raporunu dosyaya yazma fonksiyonu
def write_error_report(error_message, first_name, last_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("rapor.txt", "a", encoding="utf-8") as error_file:
        error_file.write(f"{timestamp}: {first_name} {last_name} - {error_message}\n")

# Kullanıcı bilgilerini kaydetme fonksiyonu (ad, soyad, kullanıcı adı, ID, telefon numarası)
def save_user_info(first_name, last_name, username, user_id, phone_number):
   timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
   with open("numara.txt", "a", encoding="utf-8") as user_file:
       user_file.write(f"Tarih ve Saat: {timestamp}, Ad: {first_name}, Soyad: {last_name}, Kullanıcı Adı: {username}, Kullanıcı ID: {user_id}, Numara: {phone_number}\n")

# Mesajları kaydetme fonksiyonu
def save_message_info(first_name, last_name, username, user_id, phone_number, message_info):
    with open("mesaj.txt", "a", encoding="utf-8") as message_file:
        message_file.write(f"Ad: {first_name}, Soyad: {last_name}, Kullanıcı Adı: {username}, Kullanıcı ID: {user_id}, Numara: {phone_number}, Mesaj: {message_info}\n")

# Küfür loglama fonksiyonu
def log_kufur(first_name, last_name, kufur_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("küfürlog.txt", "a", encoding="utf-8") as kufur_file:
        kufur_file.write(f"{timestamp}: {first_name} {last_name} - Küfür: {kufur_message}\n")

# Banlı kullanıcıları takip edecek bir küme
banned_users = set()

# Dolandırıcıları takip edecek bir küme
scammers = set()

# Küfürleri içeren dosyanın adı
kufur_dosyasi = "küfür.txt"

# Güzel kelimelerin içeren dosyanın adı
guzel_dosyasi = "güzel.txt"

special_characters = ''

def özel_karakter_var_mı(cümle):
    return any(char in special_characters for char in cümle)

# Türkçe yazı kontrolü fonksiyonu
async def turkce_yazi_kontrol(client, text, sender_id):
    turkce_regex = re.compile("[A, B, C, Ç, D, E, F, G, Ğ, H, I, İ, J, K, L, M, N, O, Ö, P, R, S, Ş, T, U, Ü, V, Y, Z, a, b, c, ç, d, e, f, g, ğ, h, ı, i, j, k, l, m, n, o, ö, p, r, s, ş, t, u, ü, v, y, z]+")
    return bool(turkce_regex.fullmatch(text))

# Küfürleri oku ve bir liste olarak sakla
with open(kufur_dosyasi, "r", encoding="utf-8") as file:
    kufur_kelimeleri = [line.strip() for line in file]

# Güzel kelimeleri oku ve bir liste olarak sakla
with open(guzel_dosyasi, "r", encoding="utf-8") as file:
    guzel_kelimeler = [line.strip() for line in file]

message_template = """
Merhaba Hoş Geldiniz Fiyat Listesi 
Ekran Resmi Şimdi Gönderiliyor.
Ekran Resmi Gelmez ise Aşadaki Link Tıklayarakta Görebilirsiniz..
https://ezglobalyazillim.com/kart.html


"""

message2 = """
👉Türkiyede İlk Ve Tek Hile Satışlarından Para Kazandıran Tek Yer!💷💸
👉Nasıl Para Kazanırım? Nasıl Teslim Alabilirim? Müşteri Referanslar Var mı?
Tüm Sorularınız Cevabı Altaki Video'da Mevcut✅
https://youtu.be/Hy_D60WV8mQ
💳Ödeme Yöntemleri:Papara, İninal, Tosla, Paycell
💳veya Epin Sultan Site Kuponu ile Burdan Alışveriş Yapabilirsin🛍🛒
https://www.epinsultan.com/site-bakiyesi
NeXus PiXel ANONİM ŞİRKETİ©️
"""

# Gönderilen mesajları takip eden bir küme (set)
sent_messages = set()
image_sent = False  # Resmin gönderilip gönderilmediğini takip etmek için

# Hoş geldiniz mesajının ve yardım mesajının gönderilip gönderilmediğini kontrol etmek için bir bayrak (flag)
welcome_message_sent = set()
help_message_sent = set()

# Kullanıcının yanıt verip vermediğini kontrol etmek için bir bayrak (flag)
user_response_received = set()

# Kullanıcı telefon numaralarının durumu
user_phone_numbers = {}

# Dolandırıcı kullanıcıları dolandırıcılar.txt dosyasından oku
def load_scammers():
    with open("dolandırıcılar.txt", "r") as file:
        for line in file:
            line = line.strip()  # Satırın başındaki ve sonundaki boşlukları kaldır
            if line:  # Satır boş değilse
                try:
                    scammers.add(int(line))  # Sayıya çevirip ekle
                except ValueError:
                    print(f"Geçersiz ID: {line}")  # Hata durumunda bildirim

load_scammers()

async def handle_kufur(client, sender_id, event, first_name, last_name):
    # Engellenen mesajı al
    blocked_message = event.message.text

    # Küfürü log dosyasına yaz
    log_kufur(first_name, last_name, blocked_message)

    # Engellenen mesajı alıcıya gönder
    await client.send_message(sender_id, f"Master Coder :❌️ Yasaklı Kelime Algılandı")

    # Mesajı silerek engelle
    await event.delete()

# Numara açma uyarısı gönderilen kullanıcıları takip eden bir küme
numara_uyarisi_verilenler = set()
# Numara açma uyarısı gönderilen kullanıcıları takip eden bir küme
numara_uyarisi_verilenler = set()
scammer_notified = set()  # Dolandırıcılara gönderilen mesajlar için bir set


scammer_notified = set()  # Dolandırıcılara gönderilen mesajlar için bir set
# Dosya içeriğini düzenlemek için
def duzenle_dosyayi(dosya_adi):
    with open(dosya_adi, 'r') as dosya:
        icerik = dosya.read()
    
    # Boşluk veya yan yana yazılmış ID'leri ayırmak için boşluk ve newline karakterlerine göre ID'leri böler
    idler = icerik.split()
    
    # Her ID'yi yeni bir satıra yazar
    with open(dosya_adi, 'w') as dosya:
        for id in idler:
            dosya.write(id + '\n')

# Kullanım
duzenle_dosyayi('dolandırıcılar.txt')
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender_id = event.sender_id
    user = await event.get_sender()
    
    # Telefon numarası gizli mi?
    phone_number = user.phone
    
    # Eğer kullanıcı dolandırıcı olarak işaretlenmişse
    if sender_id in scammers:
        # Eğer bu kullanıcıya daha önce mesaj gönderilmediyse
        if sender_id not in scammer_notified:
            # Dolandırıcı mesajını kaydet
            if event.message.text:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message_info = f"Tarih: {timestamp}, Kullanıcı ID: {sender_id}, Mesaj: {event.message.text}"
                first_name = user.first_name if user.first_name else 'Bilinmiyor'
                last_name = user.last_name if user.last_name else 'Bilinmiyor'
                username = user.username if user.username else 'Bilinmiyor'
                phone_number = user.phone if user.phone else 'Bilinmiyor'
                save_message_info(first_name, last_name, username, sender_id, phone_number, message_info)

            # Mesajı sadece bir kez gönder
            await client.send_message(sender_id, "🛑ORUSPU ÇOCUĞU ve Anesini Amını Siktiğim Algılandı Artık Mesaj Yazamasın Bacını Siktiğim")
            scammer_notified.add(sender_id)  # Mesajın gönderildiğini kaydet

        await event.delete()  # Mesajı sil
        await client.delete_dialog(sender_id)  # Sohbeti bot tarafından siler
        return

    # Mesajın içeriğini kontrol et
    if event.message.text or event.message.media:
        message_text = event.message.text.lower()  # Gelen mesajın metnini küçük harfe çevirin

        user = await event.get_sender()
        first_name = user.first_name if user.first_name else 'Bilinmiyor'
        last_name = user.last_name if user.last_name else 'Bilinmiyor'
        username = user.username if user.username else 'Bilinmiyor'
        user_id = sender_id

        user_info = f"Ad: {first_name}, Soyad: {last_name}, Kullanıcı Adı: {username}, Kullanıcı ID: {user_id}"

        # Kullanıcı bilgilerini ve numarasını yakala ve kaydet
        phone_number = user.phone
        if phone_number:
            if sender_id not in user_phone_numbers or user_phone_numbers[sender_id] != phone_number:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_user_info(first_name, last_name, username, user_id, phone_number)
                user_phone_numbers[sender_id] = phone_number
                await client.send_message(sender_id, """
 --Numaranız Onaylandı✅ ve Güvenlik Sebebiyle Kaydedildi✅
-------Kuralarımız---------- 
1.Uyarı(Bunlarıda Sakın Yapma)
-⚠️🛑üste sizlere şuan satın almicaksanız rahtsız etmemeniz hakında sizlere bilgilendirme yapıldı🛑
-⚠️🛑Aynı Zamanda Üste Yazılanlar Okudunuz mu Diyede Soruldu!✅
-⚠️🛑Bunlara Rağmen Satın Alıcam Diyip Sahtekarların Yaptığı Gibi Fake Atarsan
Çekilen Numaran İle Başın Cok Bela Girer Burası Aynı Zamanda Telegram Apisine Sahiptir İp Adresinize Kadar Çekim Yapmaktadır.
Bunu Açık Olarakta Sizlere Yazıyorum Üzülmek İstemiyorsan Saygılı ve Dürüst Ol!
Sonrası Olucaklardan Sorumlu Deilim.
-------------------------------------------
2.Uyarı(Bunlarıda Sakın Yapma)
-⚠️🛑 Sakın Bana (Görüldü Atma) Müsait Deilsen Mutlaka Belirt! 
-⚠️🛑 5 Dakika Bekleticem Diyip Kacıp Gitmek 
-⚠️🛑 Akşam Alıcam Diyip Sonra Almamak Kacıp Gitmek
🛑Master Coder Ahmet Ayhan = Burdaki Uyarıları Lütfen
Ciddiye Al Edepli Saygılı Olan Herkes Başım Üstünde Yeri Vardır
Her Müşterim Para İade Garantisi Vardır işimi Hakıyla Yapıyorum
lütfen Sizlerde Sözünüzün Eri Olun (Alıcaksanız Alın)
(Almicaksanız da üste yazılanlar ragmen rahtsız etmeyin)
Birzdan Müsait Olunduğunda -Kurucu Sn.Ahmet AYHAN  Bağlantı Sağlicak✅

Teşekür Ederim

NeXus PiXel ANONİM ŞİRKETİ©️
""")
                # Özel karakter kontrolü
        if özel_karakter_var_mı(message_text):
            await handle_kufur(client, sender_id, event, first_name, last_name)
            return

        # Harf tekrarı sayısını kontrol et
        repeat_letters = re.search(r'(\w)\1{2,}', message_text)

        # Eğer aynı kişi aynı harf tekrarını bulursa uyarı ver
        if repeat_letters:
            await handle_kufur(client, sender_id, event, first_name, last_name)
            return

        # Küfür kontrolü
        for kufur in kufur_kelimeleri:
            if re.search(r'\b{}\b'.format(re.escape(kufur)), message_text, flags=re.IGNORECASE):
                await handle_kufur(client, sender_id, event, first_name, last_name)
                return

            if re.search(r'(?<!\S){}(?!\S)'.format(re.escape(kufur)), message_text.replace(' ', ''), flags=re.IGNORECASE):
                await handle_kufur(client, sender_id, event, first_name, last_name)
                return

        # Mesajı mesaj.txt dosyasına ekle
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_info = f"Tarih: {timestamp}, Kullanıcı ID: {sender_id}, Mesaj: {message_text}"
        save_message_info(first_name, last_name, username, user_id, phone_number, message_info)
        
        # İlk mesaj akışını tamamlayın
        if event.message.reply_to_msg_id is None and sender_id not in sent_messages:
            sent_messages.add(sender_id)

            await client.send_message(sender_id, f"Müşterinin {user_info}")
            await client.send_message(sender_id, message_template)
            await client.send_file(sender_id, 'valo.jpg')

            global image_sent
            if not image_sent:
             
               image_sent = True  # Resmin gönderildiğini işaretle
            await client.send_message(sender_id, message2)

        else:
            if sender_id not in welcome_message_sent:
                await client.send_message(sender_id, """🕊🧑🏻‍💻 Yetkili Bağlandı: Merhaba, hoş geldiniz!

Hangi ödeme yöntemleriyle ürün alacaksınız? 💳

Ödeme Yöntemleri:

Papara
İninal
Tosla
Paycell
Epin Sultan Site Kuponu
Eğer Banka İban İle Ödeme Yapıcaksanız
https://www.epinsultan.com/site-bakiyesi
Burdan Alıcanız Ürün Fiyat Eşdeğer Epin Sultan Site Kuponu Almanız Yeterli Olur
Detaylı Bilgi Üsteki Videomuza Bakabilirsiniz!
NeXus PiXel ANONİM ŞİRKETİ©️""")
                welcome_message_sent.add(sender_id)

            # Kullanıcı yanıt verirse, yanıtı bekleyin
            if sender_id in welcome_message_sent and sender_id not in help_message_sent:
                if sender_id in user_response_received:
                    await client.send_message(sender_id, """🕊🧑🏻‍💻 Yetkili: Sizleri şimdi bilgilendireceğim ancak öncelikle şunu düzeltmeniz gerekiyor.

👉 Telegram profilinize baktım, telefon numaranızı gizlediğinizi görmekteyim. Lütfen numaranızı açık hale getirin.
🛑👉 Sadece numarası açık müşterilere hizmet vermekteyiz. ✅

Neden böyle bir kural var?
Fake numaralar ile hesap açıp rahatsız edenlerden dolayı bu önlemi alıyoruz.""")
                    help_message_sent.add(sender_id)

                    await client.send_message(sender_id, """🕊🧑🏻‍💻 Sadece numarası açık olan müşterilere hizmet vermekteyiz.

Eğer bu durum sizin için uygun değilse, farklı şirketlerden satın alım yapabilirsiniz.

👉 Numaramı nasıl açarım?

Ayarlar
Gizlilik ve Güvenlik
Telefon Numarası
Herkese Açık
Bu kadar kolay! ✅""")
                    help_message_sent.add(sender_id)

                else:
                    user_response_received.add(sender_id)

        # Mesaj akışı tamamlandıktan sonra telefon numarasını kontrol et
        if not phone_number and sender_id in user_response_received:
            if sender_id in help_message_sent:  # Bu, numara açma talimatlarının gönderildiği kullanıcıları kontrol eder
                   await client.send_message(sender_id, """🛑 Numaranız hala gizli. Lütfen numaranızı açmadınız. Hizmet almak için numaranızın açık olması gerekiyor. numaranız açtıktan sonra bilgilendiriniz!""")


@client.on(events.NewMessage(pattern='q'))
async def banla_handler(event):
    # Admin kullanıcı ID'sini belirleyin
    ADMIN_USER_ID = 5968404422
    
    # Komutu sadece admin kullanabilir
    if event.sender_id != ADMIN_USER_ID:
        await event.reply("Bu komutu kullanma izniniz yok.")
        return

    # Kullanıcıdan komutu ve hedef kullanıcıyı al
    command_parts = event.message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await event.reply("Bir kullanıcı ID'si belirtmelisiniz.")
        return

    target = command_parts[1].strip()

    try:
        # Hedef kullanıcıyı bulma
        if target.isdigit():
            # Eğer hedef bir ID ise
            target_id = int(target)
            target_user = await client.get_entity(target_id)
        else:
            # Eğer hedef bir kullanıcı adı ise
            target_user = await client.get_entity(target)
            target_id = target_user.id

        # Kullanıcıyı banla ve ekle
        banned_users.add(target_id)

        # Dolandırıcılar listesine de ekle
        scammers.add(target_id)
        with open("dolandırıcılar.txt", "a", encoding="utf-8") as scam_file:
            scam_file.write(f"{target_id}\n")

        # Yasaklı kullanıcıya uyarı mesajı gönder
        await client.send_message(target_id, "Kullanıcı Verileri Çekildi Sorgu Yapıldı Telefon Modeli Öğrenildi web sürümü öğrenildi✅ İP Adres Sorgusu Başarılı✅ Anesi Sikilmeye Müsait ✅ ")

        await event.reply(f"{target_user.username if target_user.username else 'Kullanıcı'} Aptal Oruspunun Çocuğu Almicaksan Üste Yazılanlara Rağmen Ne Diye Yazıyorsun Ananı Kundakta Sikiçem Şimdi")
    except Exception as e:
        await event.reply(f"Hata oluştu: {str(e)}")

@client.on(events.NewMessage(pattern='x'))
async def id_handler(event):
    # Admin kullanıcı ID'sini belirleyin
    ADMIN_USER_ID = 5968404422
    
    # Komutu sadece admin kullanabilir
    if event.sender_id != ADMIN_USER_ID:
        await event.reply("Bu komutu kullanma izniniz yok.")
        return

    # Sohbetin tüm kullanıcı ID'lerini almak için
    chat = await event.get_chat()
    participants = await client.get_participants(chat)
    
    # Kullanıcı ID'lerini listele
    ids = [str(participant.id) for participant in participants]

    # Admin'e kullanıcı ID'lerini gönder
    await event.reply("q\n" + "\n".join(ids))
@client.on(events.NewMessage(pattern='-'))
async def reminder_handler(event):
    # Admin kullanıcı ID'sini belirleyin
    ADMIN_USER_ID = 5968404422

    # Komutu sadece admin kullanabilir
    if event.sender_id != ADMIN_USER_ID:
        await event.reply("Bu komutu kullanma izniniz yok.")
        return

    # Hatırlatma mesajları
    reminder_message_1 = "Hatırlatma: epinsultan site kuponu aldığınızda direk buraya iletiniz, detaylı bilgi üstteki videoda gösterilmiştir."
    reminder_message_2 = "Merhaba, epinsultan kupon kodunuz hazır mı?"

    # Mesajları sırayla gönder
    await event.reply(reminder_message_1)
    await event.reply(reminder_message_2)

# Kodu çalıştır
try:
    client.run_until_disconnected()
except Exception as e:
    error_message = f"Hata oluştu: {str(e)}"
    write_error_report(error_message, 'Bilinmiyor', 'Bilinmiyor')
