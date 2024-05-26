from main import * 
import datetime

# model, tokenizer = load_model_and_tokenizer("./bot_model.h5")
# pred = predict_class("saya sakit", tokenizer, model)
# print(pred)

# get_data = get_data_pegawai()
# print(get_data)

# tanggal_sekarang = datetime.datetime.now()

# # Mengonversi objek datetime menjadi string dengan format yang diinginkan
# tanggal_sekarang_string = tanggal_sekarang.strftime("%Y-%m-%d")
# insert_absensi(77, tanggal_sekarang_string, "wwkwwwk", "test", "test22")
# print(datetime.datetime.now())


data = read_json()

# for i in range(len(data['intents'])):
print(data['intents'][0]['input'])