import streamlit as st
import pandas as pd 
import numpy as np
import joblib
import sklearn







def main():
    
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..',["Tahmin Yap"])

    st.markdown(
        """
        Bu proje makine öğrenmesi dersi için oluşturulmuştur. Bir e-ticaret sitesi üzerinden 1176 adet laptop verisi çekilmiş
        ve incelenmiştir. Bu veriler kullanılarak makine öğrenmesi modelleri eğitilmiş ve projeye dahil edilmiştir.
            
        """)
    st.info("Tahmin yapmak için sol tarafta bulunan menüyü kullanınız.")

    if selected_page == "Tahmin Yap":
        predict()



def predict():
    markalar = load_data()

    # Kullanıcı arayüzü ve değer alma
    st.title('Merhaba, hoşgeldiniz, fiyatını tahmin etmek istediğiniz laptop özelliklerini aşağıda doğru bir şekilde doldurunuz. 👨‍💻')
    
    selected_marka = st.selectbox('Marka Seçiniz..', markalar)
    st.write("Seçilen Marka:", selected_marka)
    # Marka tahminini al
    predicted_marka = marka(selected_marka)
    st.write("Seçilen Marka:", predicted_marka)

    selected_ekran_boyutu = st.number_input('Ekran Boyutu',min_value=0.0,max_value=25.0)
    st.write("Ekran Boyutu: "+str(selected_ekran_boyutu)+" İnç")

    def ekran_kartı():
        selected_ekran_kartı = st.radio("Ekran Kartı Seçiniz..", ('Nvidia', 'AMD', 'Intel', 'Apple', 'Dahili Ekran Kartı'))
        if selected_ekran_kartı == 'Nvidia':
            return 4
        elif selected_ekran_kartı == 'AMD':
            return 0
        elif selected_ekran_kartı == 'Intel':
            return 3
        elif selected_ekran_kartı == 'Apple':
            return 1
        else:
            return 2
    selected_ekran_kartı = ekran_kartı()

    hz_values = [60,90,120,144,165,240,360,480]
    selected_yenileme_hızı = st.select_slider('Ekran Yenileme hızı (Hz) Seçiniz:', options=hz_values)
    st.write("Ekran Yenileme hızı (Hz): "+str(selected_yenileme_hızı)+" Hz")

    hdd_values = [0,32,64,120,128,240,256,500,512,1024,2048]
    selected_hard_disk = st.select_slider('Hard Disk Kapasitesi:', options=hdd_values)
    st.write("Hard Disk Kapasitesi: "+str(selected_hard_disk)+" GB")

    def klavye():
        selected_klav = st.radio("Klavye Seçeneği", ('Aydınlatmalı (RGB)', 'Aydınlatmasız'))
        if selected_klav == "Aydınlatmalı (RGB)":
            return 1
        else:
            return 0    

    selected_klav = klavye()

    def amac():
        selected_kullanım = st.radio("Kullanım Amacı",('Ofis - İş', 'Oyun', 'Ev - Okul'))
        if selected_kullanım == 'Ofis - İş':
            return 1
        elif selected_kullanım == 'Oyun':
            return 2
        else:
            return 0
    selected_kullanım = amac()

    ram_values = [3,4,8,12,16,18,24,32,36,40,48,64]
    selected_ram = st.select_slider('RAM Kapasitesi Seçiniz:', options=ram_values)
    st.write("Seçtiğiniz RAM Kapasitesi: " +str(selected_ram)+ " GB")

    def ram_tip():
        selected_ram_tipi = st.radio("RAM Tipi Seçiniz",('DDR4', 'DDR5', 'DDR3'))
        if selected_ram_tipi == 'DDR4':
            return 1
        elif selected_ram_tipi == 'DDR5':
            return 2
        else:
            return 0
    selected_ram_tipi = ram_tip()

    ssd_values = [32,64,120,128,240,256,500,512,1024,2048,4096]
    selected_ssd = st.select_slider('SSD Kapasitesi Seçiniz:', options=ssd_values)
    st.write("SSD Kapasitesi: "+str(selected_ssd)+" GB")

    cozunurluk = load_coz()
    selected_cozunurluk = st.selectbox("Çözünürlük Standartı Seçiniz..", cozunurluk)
    st.write("Seçilen Çözünürlük Standartı: ", selected_cozunurluk)
    predicted_cozunurluk = Standart(selected_cozunurluk)
    st.write("Seçilen Çözünürlük:", predicted_cozunurluk)

    selected_islemci_nesli = st.number_input('İşlemci Nesli Giriniz',min_value=1,max_value=12)
    st.write("İşlemcş Nesli: "+str(selected_islemci_nesli)+".Nesil")

    islemci = load_islemci()
    selected_islemci = st.selectbox("İşlemci Seçiniz..", islemci)
    st.write("Seçilen İşlemci: ", selected_islemci)
    predict_islemci = islemcid(selected_islemci)
    st.write("Seçilen İşlemci Değeri:",predict_islemci)

    cekirdek_values = [1,2,4,5,6,8,10,12,14,16,24]
    selected_cekirdek = st.select_slider('İşlemci Çekirdek Sayısı Seçiniz:', options=cekirdek_values)
    st.write("Seçtiğiniz Çekirdek Sayısı: ", selected_cekirdek)

    def isletim_sistemi():
        selected_isletim_sis = st.radio("İşletim Sistemi Seçiniz.. ",('Free Dos', 'Windows', 'Mac Os', 'Linux'))
        if selected_isletim_sis == 'Free Dos':
            return 0
        elif selected_isletim_sis == 'Windows':
            return 3
        elif selected_isletim_sis == 'Mac Os':
            return 2
        else:
            return 1
    selected_isletim_sis = isletim_sistemi()



    prediction_value = create_prediction_value(predicted_marka,selected_ekran_boyutu,selected_ekran_kartı,selected_yenileme_hızı,selected_hard_disk,
                                               selected_klav,selected_kullanım,selected_ram,selected_ram_tipi,selected_ssd,
                                               predicted_cozunurluk,selected_islemci_nesli,predict_islemci,selected_cekirdek,selected_isletim_sis)    
    prediction_model = load_models()
    
    
    if st.button("Tahmin Yap"):
        result = predict_models(prediction_model,prediction_value)
        if result != None:
            st.success('Tahmin Başarılı')
            st.balloons()
            st.write("Tahmin Edilen Fiyat: "+ result + "TL")
        else:
            st.error('Tahmin yaparken hata meydana geldi..!')




def load_data():
    markalar = ['HP', 'Lenovo', 'Apple', 'Huawei', 'Casper', 'Asus', 'ACER', 'MSI', 'Monster', 'Dell', 'Everest', 'Toshiba', 'Samsung', 'Gigabyte', 'Xiaomi']
    return markalar

def marka(selected_marka):
    marka_dict = {'HP': 7, 'Lenovo': 9, 'Apple': 1, 'Huawei': 8, 'Casper': 3, 'Asus': 2, 'ACER': 0, 'MSI': 10, 'Monster': 11, 'Dell': 4, 'Everest': 5, 'Toshiba': 13, 'Samsung': 12, 'Gigabyte': 6, 'Xiaomi': 14}
    
    # Eğer seçilen marka sözlükte yoksa None döndür
    return marka_dict.get(selected_marka)

def load_coz():
    cozunurlukk = ['Full HD (FHD)', 'Retina', 'QHD+', 'Ultra HD 4K (UHD)', 'WQHD', 'WUXGA', 'QHD', 'WQXGA', 'OLED 2.8K', 'Dokunmatik']   
    return cozunurlukk

def Standart(selected_cozunurluk):
    cozunurluk_dict = {'Full HD (FHD)': 0, 'Retina': 2, 'QHD+': 3, 'Ultra HD 4K (UHD)': 4, 'WQHD': 7, 'WUXGA': 9, 'QHD': 5, 'WQXGA': 8, 'OLED 2.8K': 6, 'Dokunmatik': 10}
    return cozunurluk_dict.get(selected_cozunurluk)

def load_islemci():
    islemcitip = ['M2', 'M1','M3', 'Intel Celeron', 'Intel Core i5', 'Intel Core i7', 'Intel Core i3', 'Intel Core i9','AMD Ryzen 9', 'AMD Ryzen 7', 'AMD Ryzen 5', 'AMD Ryzen 3']
    return islemcitip

def islemcid(selected_islemci):
    islemci_dict = {'M2': 10, 'M1': 9, 'M3': 11, 'Intel Celeron': 4, 'Intel Core i5': 6, 'Intel Core i7': 7, 'Intel Core i3': 5, 'Intel Core i9': 8,'AMD Ryzen 9': 3, 'AMD Ryzen 7': 2, 'AMD Ryzen 5': 1, 'AMD Ryzen 3': 0}
    return islemci_dict.get(selected_islemci)


def create_prediction_value(predicted_marka,selected_ekran_boyutu,selected_ekran_kartı,selected_yenileme_hızı,selected_hard_disk,
                            selected_klav,selected_kullanım,selected_ram,selected_ram_tipi,selected_ssd,
                            predicted_cozunurluk,selected_islemci_nesli,predict_islemci,selected_cekirdek,selected_isletim_sis):
    res = pd.DataFrame(data=
                       {"marka": [predicted_marka], "ekran_boyutu": [selected_ekran_boyutu], "ekran_kartı": [selected_ekran_kartı],
                        "ekran_yenileme_hızı": [selected_yenileme_hızı],
                        "hard_disk_kapasitesi": [selected_hard_disk], "klavye": [selected_klav], "kullanım_amacı": [selected_kullanım],
                        "ram_sistem_bellegi": [selected_ram], "ram_tipi": [selected_ram_tipi], "ssd_kapasitesi": [selected_ssd],
                        "cozunurluk_standartı": [predicted_cozunurluk], "islemci_nesli": [selected_islemci_nesli],
                        "islemci_tipi": [predict_islemci],
                        "islemci_cekirdek_sayisi": [selected_cekirdek], "isletim_sistemi": [selected_isletim_sis]})
    return res

def load_models():
    rf_model = joblib.load("random_forest_model.pkl")
    return rf_model

def predict_models(model,res):
    result = str((model.predict(res))).strip('[]')
    return result

if __name__ == "__main__":
    main()