import random

imageArray = [
	"https://images.unsplash.com/photo-1508185159346-bb1c5e93ebb4?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=55cf14db6ed80a0410e229368963e9d8&auto=format&fit=crop&w=1900&q=80",
	"https://images.unsplash.com/photo-1495480393121-409eb65c7fbe?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=05ea43dbe96aba57d48b792c93752068&auto=format&fit=crop&w=1351&q=80",
	"https://images.unsplash.com/photo-1501611724492-c09bebdba1ac?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=ebdb0480ffed49bd075fd85c54dd3317&auto=format&fit=crop&w=1491&q=80",
	"https://images.unsplash.com/photo-1417106338293-88a3c25ea0be?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=d1565ecb73a2b38784db60c3b68ab3b8&auto=format&fit=crop&w=1352&q=80",
	"https://images.unsplash.com/photo-1500520198921-6d4704f98092?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=ac4bc726064d0be43ba92476ccae1a75&auto=format&fit=crop&w=1225&q=80",
	"https://images.unsplash.com/photo-1504966981333-1ac8809be1ca?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=9a1325446cbf9b56f6ee549623a50696&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1437075130536-230e17c888b5?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=ff573beba18e5bf45eb0cccaa2c862b3&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1515002246390-7bf7e8f87b54?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=1eac0f70640261e09152340f13b79144&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1506057278219-795838d4c2dd?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=f68d8d7b0223cd906ea8cac13421881d&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1488402410361-05152fa654d3?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=5266aadc96d5b5b23996e7120d3190a8&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1475598322381-f1b499717dda?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=cb49f991ce8dd947b45ccd1bd905ec8c&auto=format&fit=crop&w=1355&q=80",
	"https://images.unsplash.com/photo-1501949997128-2fdb9f6428f1?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=951ee200e732c9b8c4ea0a7372ca9d27&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1494783367193-149034c05e8f?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=a98c0f9a6c602e964e6533de413d59ba&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1476547362848-ed2a9f99cd29?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=5b4647c9e25267c25866936c916e4aa8&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1506017669510-0bcbe8003d70?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=9403f5d4ac23a5726bfc3c8308b31c01&auto=format&fit=crop&w=1350&q=80",
	"https://images.unsplash.com/photo-1489447068241-b3490214e879?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=a85cb0d68de38ae2aa00d8a9663a320a&auto=format&fit=crop&w=1350&q=80",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-1.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-2.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-3.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-4.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-5.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/featured-contributors/card-6.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-1.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-2.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-3.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-4.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-5.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-6.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-7.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-8.jpg",
	"https://slp-statics.astockcdn.net/static_assets/staging/21fall/premium/thematic-concept-collections/card-9.jpg",

];

tagArray = ["Advice","Android","Apple", "Architecture","Art", "Blogging","Books",
			"Business","Cars","Comics","Comedy","Cooking","Cosmetics","Crafts","Culture","Design","Education","Fashion","Food","Health",
			"Humor", "Life", "Internet", "Music", "Marketing", "Movies","News", "Photography","Politics", "Technology", "Travel", "Writing"
			,"Nutrition","Parenting","Personal","Photo", "Law","Science","Shopping","Social","Gossip","Geek","Landscape","Management","Pets","Relationships"]

def random_pic():
	return random.choice(imageArray)

def random_tag():
	return random.choice(tagArray)

def random_hashtag():
	return "#" + random.choice(tagArray).lower()

def random_hashtags():
	tags = ""
	nr = random.randint(1, 4)
	for x in range(nr):
		tags = tags + random_hashtag() + " "
	return tags
