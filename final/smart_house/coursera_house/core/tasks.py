from __future__ import absolute_import, unicode_literals

from json.decoder import JSONDecodeError

from celery import task
import requests
from django.core.mail import send_mail

from django.conf import settings
from .models import Setting


@task()
def smart_home_manager():
    try:
        data = get_data()
        settings.TEMPLATE_DATA = data
        # print(data)
        if data != 0:
            new_data = check_and_update_data(data)
            # print(new_data)
            if new_data["controllers"]:
                post_data(new_data)
        else:
            raise ValueError
    except ValueError:
        print('Decoding JSON has failed')


def get_data():
    controller_url = settings.SMART_HOME_API_URL
    final_data = {
        "controllers": []
    }
    try:
        data = requests.get(
            controller_url,
            headers={'Authorization': 'Bearer {}'.format(settings.SMART_HOME_ACCESS_TOKEN)}
        )

        if data.status_code != requests.codes.ok:
            return 0
        else:
            data = data.json()

        data = data['data']

        for item in data:
            final_data['controllers'].append(
                {
                    "name": item['name'],
                    "value": item['value']
                }
            )

    except ValueError:
        print('Decoding JSON has failed')

    return final_data


def post_data(final_data):

    controller_url = settings.SMART_HOME_API_URL
    try:
        requests.post(
            controller_url,
            headers={'Authorization': 'Bearer {}'.format(settings.SMART_HOME_ACCESS_TOKEN)},
            json=final_data
        )
    except ValueError:
        print('Decoding JSON has failed')


def check_and_update_data(data):
    final_data = {
        "controllers": []
    }
    leak_detector = False
    cold_water = True
    try:
        for item in data['controllers']:
            # 1
            if item['name'] == 'leak_detector' and item['value'] is True:
                leak_detector = True
                ch_send_mail()
                final_data["controllers"].append(
                    {
                        "name": 'cold_water',
                        "value": False
                    }
                )
                final_data["controllers"].append(
                    {
                        "name": 'hot_water',
                        "value": False
                    }
                )
        for item in data['controllers']:
            # 2
            if item['name'] == 'cold_water' and (item['value'] is False or leak_detector is True):
                cold_water = False
                for item2 in data['controllers']:
                    if item2['name'] == 'boiler' and item2['value'] is True:
                        final_data["controllers"].append(
                            {
                                "name": 'boiler',
                                "value": False
                            }
                        )
                for item2 in data['controllers']:
                    if item2['name'] == 'washing_machine' and item2['value'] != 'off':
                        final_data["controllers"].append(
                            {
                                "name": 'washing_machine',
                                "value": 'off'
                            }
                        )
            elif item['name'] == 'cold_water' and item['value'] is True and leak_detector is False:
                for item2 in data['controllers']:
                    # 3
                    if item2['name'] == 'boiler_temperature':
                        boiler_temperature = item2['value']
                        hot_water_target_temperature = \
                            Setting.objects.get(controller_name='hot_water_target_temperature').value
                        if boiler_temperature < hot_water_target_temperature * 0.9:
                            for item3 in data['controllers']:
                                if item3['name'] == 'smoke_detector' and item3['value'] is not True:
                                    for item4 in data['controllers']:
                                        if item4['name'] == 'boiler' and item4['value'] is not True:
                                            final_data["controllers"].append(
                                                {
                                                    "name": 'boiler',
                                                    "value": True
                                                }
                                            )
                        if boiler_temperature >= hot_water_target_temperature * 1.1:
                            for item4 in data['controllers']:
                                if item4['name'] == 'boiler' and item4['value'] is not False:
                                    final_data["controllers"].append(
                                        {
                                            "name": 'boiler',
                                            "value": False
                                        }
                                    )
        for item in data['controllers']:
            # 4,5
            if item['name'] == 'outdoor_light' and item['value'] > 50:
                for item2 in data['controllers']:
                    if item2['name'] == 'bedroom_light' and item2['value'] is False:
                        for item3 in data['controllers']:
                            if item3['name'] == 'curtains' and item3['value'] != 'slightly_open':
                                for item4 in data['controllers']:
                                    if item4['name'] == 'curtains' and item4['value'] != 'open':
                                        final_data["controllers"].append(
                                            {
                                                "name": 'curtains',
                                                "value": 'open'
                                            }
                                        )

            elif (item['name'] == 'outdoor_light' and item['value'] < 50) or\
                    (item['name'] == 'bedroom_light' and item['value'] is True):
                for item2 in data['controllers']:
                    if item2['name'] == 'curtains' and item2['value'] != 'slightly_open':
                        for item3 in data['controllers']:
                            if item3['name'] == 'curtains' and item3['value'] != 'close':
                                for item4 in final_data['controllers']:
                                    if item4['name'] == 'curtains':
                                        break
                                else:
                                    final_data["controllers"].append(
                                        {
                                            "name": 'curtains',
                                            "value": 'close'
                                        }
                                    )

        for item in data['controllers']:
            # 6
            if item['name'] == 'smoke_detector' and item['value'] is True:
                for item2 in data['controllers']:
                    if item2['name'] == 'air_conditioner' and item2['value'] is not False:
                        final_data["controllers"].append(
                            {
                                "name": 'air_conditioner',
                                "value": False
                            }
                        )
                for item2 in data['controllers']:
                    if item2['name'] == 'bedroom_light' and item2['value'] is not False:
                        final_data["controllers"].append(
                            {
                                "name": 'bedroom_light',
                                "value": False
                            }
                        )
                for item2 in data['controllers']:
                    if item2['name'] == 'bathroom_light' and item2['value'] is not False:
                        final_data["controllers"].append(
                            {
                                "name": 'bathroom_light',
                                "value": False
                            }
                        )
                for item3 in final_data['controllers']:
                    if item3['name'] == 'boiler':
                        if item3['value'] is True:
                            item3['value'] = False
                        break
                else:
                    for item4 in data['controllers']:
                        if item4['name'] == 'boiler' and item4['value'] is not False:
                            final_data["controllers"].append(
                                {
                                    "name": 'boiler',
                                    "value": False
                                }
                            )
                for item3 in final_data['controllers']:
                    if item3['name'] == 'washing_machine':
                        break
                else:
                    for item4 in data['controllers']:
                        if item4['name'] == 'washing_machine' and item4['value'] != 'off':
                            final_data["controllers"].append(
                                {
                                    "name": 'washing_machine',
                                    "value": 'off'
                                }
                            )
            elif item['name'] == 'smoke_detector' and item['value'] is False:
                for item1 in data['controllers']:
                    # 7
                    if item1['name'] == 'bedroom_temperature':
                        bedroom_temperature = item1['value']
                        bedroom_target_temperature = \
                            Setting.objects.get(controller_name='bedroom_target_temperature').value
                        if bedroom_temperature > bedroom_target_temperature * 1.1:
                            for item4 in data['controllers']:
                                if item4['name'] == 'air_conditioner' and item4['value'] is not True:
                                    final_data["controllers"].append(
                                        {
                                            "name": 'air_conditioner',
                                            "value": True
                                        }
                                    )
                        if bedroom_temperature <= bedroom_target_temperature * 0.9:
                            for item4 in data['controllers']:
                                if item4['name'] == 'air_conditioner' and item4['value'] is not False:
                                    final_data["controllers"].append(
                                        {
                                            "name": 'air_conditioner',
                                            "value": False
                                        }
                                    )
    except ValueError:
        print('Decoding JSON has failed')
    return final_data


def ch_send_mail():
    send_mail(
        'умный дом',
        'вода отключена',
        'dinamo-drogichin@mail.ru',
        [settings.EMAIL_RECEPIENT],
        fail_silently=False,
    )
