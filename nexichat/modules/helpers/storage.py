import random
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# لینک اتصال به پایگاه داده مونگو
MONGO_URL = "mongodb+srv://gpsfardi:mohaMmoha900@cluster0.fj1u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ایجاد اتصال به پایگاه داده
VIPBOY = MongoCli(MONGO_URL)
chatdb = VIPBOY.Anonymous
chatai = chatdb.Word.WordDb
storeai = VIPBOY.Anonymous.Word.NewWordDb
