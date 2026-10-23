import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# आपका HRIX Store का टोकन
TOKEN = '8809123081:AAFsGG-i-qzzof-buot91gJTMZ86LlbxFGM'
bot = telebot.TeleBot(TOKEN)

# Start कमांड - दुकान का मेन गेट
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    btn1 = InlineKeyboardButton("🛍️ हमारे प्रोडक्ट्स देखें (Catalog)", callback_data="show_products")
    btn2 = InlineKeyboardButton("📞 कस्टमर सपोर्ट", callback_data="support")
    markup.add(btn1, btn2)

    welcome_text = (
        "🎉 **HRIX Store** में आपका स्वागत है! 🎉\n\n"
        "यहाँ आपको मिलेंगे सबसे बेहतरीन और प्रीमियम प्रोडक्ट्स, वो भी शानदार डिस्काउंट पर。\n\n"
        "खरीदारी शुरू करने के लिए नीचे दिए गए बटन पर क्लिक करें 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# बटन्स के क्लिक को हैंडल करना
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "show_products":
        bot.answer_callback_query(call.id)
        
        # सैंपल प्रोडक्ट (स्मार्टवॉच)
        product_markup = InlineKeyboardMarkup()
        p_btn = InlineKeyboardButton("🛒 अभी खरीदें (Buy Now)", callback_data="buy_watch")
        product_markup.add(p_btn)
        
        caption = (
            "⌚ **Preator Smart Watch (Waterproof)**\n\n"
            "✨ फीचर्स: Bluetooth Calling, Heart Rate Monitor, Fitness Tracker\n"
            "💰 कीमत: **₹999** *(मार्केट प्राइस: ₹2,499)*\n\n"
            "ऑर्डर करने के लिए नीचे क्लिक करें:"
        )
        bot.send_message(call.message.chat.id, caption, reply_markup=product_markup, parse_mode='Markdown')
        
    elif call.data == "buy_watch":
        bot.answer_callback_query(call.id)
        
        # भुगतान के लिए बारकोड (QR Code) भेजने का कोड
        qr_image_url = "https://i.imgur.com/83qqqBu.png" 
        
        caption_text = (
            "📦 **ऑर्डर और पेमेंट प्रक्रिया:**\n\n"
            "1️⃣ ऊपर दिए गए **QR Code (बारकोड)** को स्कैन करके **₹999** का भुगतान करें।\n"
            "2️⃣ पेमेंट करने के बाद अपना **स्क्रीनशॉट, पूरा नाम, मोबाइल नंबर और पूरा डिलीवरी एड्रेस** एक ही मैसेज में टाइप करके नीचे भेजें:"
        )
        
        try:
            bot.send_photo(call.message.chat.id, qr_image_url, caption=caption_text, parse_mode='Markdown')
        except Exception:
            bot.send_message(call.message.chat.id, caption_text, parse_mode='Markdown')
            
        msg = bot.send_message(call.message.chat.id, "👇 कृपया अपना विवरण और स्क्रीनशॉट यहाँ भेजें:")
        bot.register_next_step_handler(msg, save_order)
        
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📞 किसी भी सहायता के लिए आप यहाँ मैसेज छोड़ सकते हैं।")

# ऑर्डर सेव करने का फंक्शन
def save_order(message):
    customer_info = message.text
    chat_id = message.chat.id
    
    # कस्टमर को कन्फर्मेशन
    bot.reply_to(message, "✅ **आपका ऑर्डर और पेमेंट डिटेल मिल गई है!**\n\nहम जल्द ही इसे वेरिफ़ाई करके आपका पार्सल डिस्पैच करेंगे। HRIX Store से खरीदारी के लिए धन्यवाद! 🙏", parse_mode='Markdown')
    
    # एडमिन (आपके) के पास ऑर्डर का अलर्ट भेजना
    admin_alert = f"🚨 **नया कन्फर्म्ड ऑर्डर आया है! (HRIX Store)**\n\nकस्टमर और पेमेंट विवरण:\n{customer_info}"
    bot.send_message(chat_id, admin_alert, parse_mode='Markdown')

print("HRIX Store bot live ho gaya hai!")
bot.polling()
