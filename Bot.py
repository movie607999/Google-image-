
import time
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

IMDB_API_KEY = "import requests

IMDB_API_KEY = "ca6dbf9407msh61bd2e5c7e991dap1de329jsn47ad675ee76d"

def get_movie_details(movie_name):
    url = f"https://imdb8.p.rapidapi.com/auto-complete?q={movie_name}"
    headers = {
        "X-RapidAPI-Key": IMDB_API_KEY,
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "d" in data:
            movie = data["d"][0]
            title = movie["l"]
            rating = movie.get("rank", "N/A")
            image = movie.get("i", {}).get("imageUrl", "No image available")
            return title, rating, image
    return None, None, None

# টেস্ট করতে চাইলে:
movie_name = "Inception"
title, rating, image = get_movie_details(movie_name)
print(f"Title: {title}\nRating: {rating}\nImage: {image}")"
TELEGRAM_BOT_TOKEN = "AAHN7bOTRnjStdedu1wtce-7qHbXC4AqBFo"

# IMDb API থেকে মুভির তথ্য আনার ফাংশন
def get_movie_info(movie_name):
    url = f"https://imdb8.p.rapidapi.com/title/find?q={movie_name}"
    
    headers = {
        "X-RapidAPI-Key": IMDB_API_KEY,
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            movie = data['results'][0]
            title = movie.get('title', 'N/A')
            image = movie.get('image', {}).get('url', 'No Image')
            rating = movie.get('rating', 'N/A')
            
            return f"🎬 {title}\n⭐ IMDb Rating: {rating}", image
        except IndexError:
            return "মুভি পাওয়া যায়নি!", None
    else:
        return "API Error!", None

# টেলিগ্রাম মেসেজ হ্যান্ডলার (Delay সহ)
def handle_message(update: Update, context: CallbackContext):
    movie_name = update.message.text.strip()
    update.message.reply_text(f"🔎 মুভি খোঁজা হচ্ছে: {movie_name}...")

    movie_info, image_url = get_movie_info(movie_name)
    
    if image_url:
        update.message.reply_photo(photo=image_url, caption=movie_info)
    else:
        update.message.reply_text(movie_info)

    # **ডিলে যোগ করা (যাতে IMDb বট আগে রিপ্লাই দেয়)**
    time.sleep(3)  # 3 সেকেন্ড অপেক্ষা করবে (তোমার মুভি বট পরে রিপ্লাই দেবে)

# বট চালানোর ফাংশন
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
