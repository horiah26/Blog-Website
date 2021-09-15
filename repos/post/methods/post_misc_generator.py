import random

tagArray = ["Advice", "Android", "Apple", "Architecture", "Art", "Blogging", "Books",
            "Business", "Cars", "Comics", "Comedy", "Cooking", "Cosmetics", "Crafts", "Culture", "Design", "Education",
            "Fashion", "Food", "Health",
            "Humor", "Life", "Internet", "Music", "Marketing", "Movies", "News", "Photography", "Politics",
            "Technology", "Travel", "Writing"
            , "Nutrition", "Parenting", "Personal", "Photos", "Law", "Science", "Shopping", "Social", "Gossip", "Geek",
            "Landscape", "Management", "Pets", "Relationships"]


def random_tag():
    return random.choice(tagArray)


def random_hashtag():
    return "#" + random.choice(tagArray).lower()


def random_hashtags():
    tags = ""
    nr = random.randint(1, 4)
    for x in range(nr):
        tags += random_hashtag() + " "
    return tags
