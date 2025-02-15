cd path/to/your/project
import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN, RAPIDAPI_KEY

# লোগিং সেটআপ
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🎥 RapidAPI IMDb API থেকে তথ্য আনা
def get_movie_info(movie_name):
    url = "https://imdb8.p.rapidapi.com/title/find"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    params = {"q": movie_name}

    response = requests.get(url, headers=headers, params=params).json()
    
    try:
        movie = response["results"][0]
        return {
            "title": movie["title"],
            "year": movie.get("year", "N/A"),
            "rating": "N/A",  # RapidAPI থেকে সরাসরি রেটিং পাওয়া যায় না
            "plot": movie.get("plotOutline", {}).get("text", "No description available."),
            "poster": movie.get("image", {}).get("url", None),
        }
    except (KeyError, IndexError):
        return None

# 🔎 মুভি সার্চ ফাংশন (গ্রুপে কেউ মুভির নাম লিখলে)
async def search_movie(update: Update, context):
    movie_name = update.message.text
    movie_data = get_movie_info(movie_name)

    if not movie_data:
        await update.message.reply_text("⚠ মুভি খুঁজে পাওয়া যায়নি! অন্য নাম দিয়ে চেষ্টা করুন।")
        return

    # 📌 IMDb তথ্য তৈরি করা
    reply_text = f"🎬 **{movie_data['title']} ({movie_data['year']})**\n"
    reply_text += f"⭐ IMDb: {movie_data['rating']}/10\n"
    reply_text += f"📖 {movie_data['plot']}\n"

    # 🎭 পোস্টার সহ রেসপন্স পাঠানো (পুরনো বটের আগেই মেসেজ যাবে)
    if movie_data["poster"]:
        await update.message.reply_photo(photo=movie_data["poster"], caption=reply_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(reply_text, parse_mode="Markdown")

# 🏃 বট চালানো
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # সার্চ কমান্ড হ্যান্ডলার (গ্রুপে আগে দেখানোর জন্য priority বেশি)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie), group=-1)

    logging.info("📡 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
