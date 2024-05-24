from main import * 
model, tokenizer = load_model_and_tokenizer("./bot_model.h5")
pred = predict_class("saya sakit", tokenizer, model)
print(pred)