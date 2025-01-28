import random
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

CHAT_STORAGE = [
    "mongodb+srv://m33537924:JLBRhGx8FLxy43c@cluster0.zy8ld.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://Yash_607:Yash_607@cluster0.r3s9sbo.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://gpsfardi:mohaMmoha900@cluster0.fj1u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
]

VIPBOY = MongoCli(random.choice(CHAT_STORAGE))
chatdb = VIPBOY.Anonymous
chatai = chatdb.Word.WordDb
storeai = VIPBOY.Anonymous.Word.NewWordDb
