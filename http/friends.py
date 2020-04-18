import requests
import datetime
from operator import itemgetter

NOW = datetime.datetime.now().year


def calc_age(uid):
    """
    the function accepts the id of the user vk.com and returns an ordered list of ages and
    the number of people with these ages as friends with this user
    """
    token = '3e99f55f3e99f55f3e99f55f573ee8ea8333e993e99f55f6001db2bdd828ae9b36ef12e'

    user_id_params = {
        'v': '5.71',
        'access_token': token,
        'user_ids': uid,
    }
    user_id = requests.get('https://api.vk.com/method/users.get', params=user_id_params).json()

    users_friends_params = {
        'v': '5.71',
        'access_token': token,
        'user_id': user_id['response'][0]['id'],
        'fields': 'bdate',
    }
    users_friends = requests.get('https://api.vk.com/method/friends.get', params=users_friends_params).json()

    all_friends_bdate = [i['bdate'] for i in users_friends['response']['items'] if ('bdate' in i) and len(i['bdate']) > 5]
    all_friends_age = sorted([NOW - int(i[-4:]) for i in all_friends_bdate])
    list_ages = sorted(sorted(list(set([(i, all_friends_age.count(i)) for i in all_friends_age])), key=itemgetter(0)), key=itemgetter(1), reverse=True)
    return list_ages


if __name__ == '__main__':
    iud = 'mercylonelymercylonelymercymercy'
    res = calc_age(iud)
    print(res)
