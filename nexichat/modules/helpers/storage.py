import random
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

CHAT_STORAGE = [
    "mongodb+srv://ranger:mohaMmoha900@cluster2.24a45.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2",
    
]

VIPBOY = MongoCli(random.choice(CHAT_STORAGE))
chatdb = VIPBOY.Anonymous
chatai = chatdb.Word.WordDb
storeai = VIPBOY.Anonymous.Word.NewWordDb
