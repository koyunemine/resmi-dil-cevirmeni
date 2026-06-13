import streamlit as st
import google.generativeai as genai

# Sayfa ayarlarını yapıyoruz 
st.set_page_config(page_title="Resmi Dil Çevirmeni", page_icon="👔", layout="centered")

# Arayüz Başlıkları
st.title("👔 Resmi Dil Çevirmeni")
st.write("Günlük dilde veya aceleyle yazdığınız mesajları, anında akademik ve kurumsal kurallara uygun resmi e-postalara dönüştürün.")
st.divider() 

# GİZLİ API ANAHTARIMIZ BURADA
# Tırnakların içine kendi şifreni yapıştır:
genai.configure(api_key=st.secrets["API_KEY"])

# 1. Adım: Alıcı Türü Seçimi 
alici = st.selectbox("1. Adım: E-posta kime gönderilecek?", 
                     ["Akademisyen / Profesör", "Yönetici / Patron", "Resmi Kurum / Şirket", "Müşteri"])

# 2. Adım: Ham Metin Girişi
ham_metin = st.text_area("2. Adım: Söylemek istediğiniz şeyi yazın (Hatalı veya samimi olabilir):", 
                         placeholder="Örn: Hocam selam, ben dün vizeye giremedim elektrik kesildi de, telafi sınavı ne zaman yaparsınız?", 
                         height=150)

# Dönüştürme Butonu
if st.button("Profesyonel E-postaya Çevir ✨", use_container_width=True):
    if not ham_metin:
        st.warning("Lütfen dönüştürmek istediğiniz mesajı boş bırakmayın.")
    else:
        with st.spinner("Yapay zeka e-postanızı hazırlıyor..."):
            try:
                # Gemini bağlantısını kuruyoruz
                genai.configure(api_key=st.secrets["API_KEY"])
                
                # --- YENİ EKLENEN KISIM: MODELİ OTOMATİK BULMA ---
                # Hata almamak için Google'a bağlanıp şifremizde çalışan en güncel modeli otomatik seçiyoruz
                dogru_model_adi = None
                for m in genai.list_models():
                    # Hem metin üretebilen hem de güncel (flash veya pro) bir model arıyoruz
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name or 'pro' in m.name:
                            dogru_model_adi = m.name
                            break # Çalışan modeli bulduğumuz an aramayı bırak
                
                if not dogru_model_adi:
                    st.error("Sistemde çalışan bir yapay zeka modeli bulunamadı.")
                    st.stop()
                    
                # Bulduğumuz o sorunsuz modeli sisteme tanımlıyoruz
                model = genai.GenerativeModel(dogru_model_adi)
                # ---------------------------------------------------
                
                # Yapay zekaya verilecek kusursuz yönlendirme
                prompt = f"""
                Sen profesyonel bir kurumsal iletişim ve akademi uzmanısın. 
                Aşağıdaki ham metni, bir '{alici}' kişisine gönderilmek üzere kusursuz, son derece saygılı, imla kurallarına uygun ve resmi bir Türkçe e-posta formatına dönüştür.
                
                Kurallar:
                1. Çıktıda mutlaka net ve profesyonel bir 'Konu:' başlığı olsun.
                2. E-posta gövdesi saygılı bir hitapla başlasın ve kurumsal bir dille bitsin.
                3. Sadece hazır e-posta metnini ver, başında veya sonunda 'İşte e-postanız' gibi ekstra açıklama veya yorum yazma.
                
                Dönüştürülecek Ham Metin: {ham_metin}
                """
                
                # Cevabı alıyoruz
                response = model.generate_content(prompt)
                
                # Sonucu ekrana basıyoruz
                st.success("E-postanız başarıyla oluşturuldu!")
                st.markdown("### 📝 Sonuç (Kopyalayabilirsiniz):")
                st.code(response.text, language="markdown")
                
            except Exception as e:
                st.error(f"Bir hata oluştu. Lütfen kodun içindeki API anahtarınızı kontrol edin. Hata: {e}")
