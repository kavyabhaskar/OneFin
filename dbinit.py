from user_schema import User
from collections_schema import Collection 

userdoc = User(username = "User1", password = "Password1").save()
colldoc = Collection(title = "1st collection", description = "New collection", movies = []).save()