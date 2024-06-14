import requests
import json
token = '' #put token vk here
version = 5.199
collect_count = 10

def getGroup(id):
    response = requests.get('https://api.vk.com/method/users.getSubscriptions',
				params = {
				'access_token': token,
				'user_id': id,
				'extended': 1,
				'fields': 'id, name, screen_name, type, contancts, description, status, wall, links, place', 
				'v': version
				})
    return response.json()['response']['items']

def getUserInfo(id):
    response = requests.get('https://api.vk.com/method/users.get',
				params = {
				'access_token': token,
				'user_ids': id,
				'fields': 'about, contacts, career, city, universities, interests',
				'v': version
				})
    return response.json()['response'][0]

def getUserFriends(id):
	response = requests.get('https://api.vk.com/method/friends.get',
					params = {
					'access_token': token,
					'user_id': id,
					'order': 'name',
					'count': 50,
					'fields': 'nickname',
					'v': version
					})
	return response.json()['response']['items']
