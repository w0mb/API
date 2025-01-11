import requests

# Идентификатор клипа (формат: owner_id_clip_id)
clip_id = '217903378_456269924'
<iframe src="https://vk.com/video_ext.php?oid=-226241530&id=456258223&hash=05937219fc2347e2"
# Задаем параметры запроса
params = {
    'videos': clip_id,  # Формат 'owner_id_clip_id'
    'access_token': 'vk1.a.r5Xjps7CUU4zv7_KZsE7r4J3B0s4lyJT7BOseHgqZL8EMivDwZ80jOjWAXpRzakf8WU8OQhd481-dayX3PZT4JCB8nAxj_hRc9JGF77x_CFmCb3LI574oUOjxyatlLrvZmdobqe16CGiOEaep2bXxIU-UxpqYDZb_QI2Z1Gghk5wfXfizxbFvfWB844iVFgid0nVyNZLe-E47aMoFdwX5w',
    # Ваш access_token
    'v': '5.199'  # Версия API ВКонтакте
}

# Отправляем GET-запрос к API ВКонтакте
response = requests.get('https://api.vk.com/method/video.viewSegments?v=5.245&client_id=6287487', params=params)

# Проверяем, успешен ли запрос
if response.status_code == 200:
    data = response.json()

    # Выводим весь ответ, чтобы понять его структуру
    print("Ответ от API:", data)

    # Проверяем наличие ключа 'response' и что в нем есть данные
    if 'response' in data:
        if 'items' in data['response'] and len(data['response']['items']) > 0:  # Проверяем, есть ли клип в ответе
            clip_info = data['response']['items'][0]

            # Проверяем доступность видео
            if clip_info.get('restriction', {}).get('can_play', 1) == 1:  # Если доступно для воспроизведения
                video_url = clip_info['player']
                print(f"Ссылка на клип: {video_url}")

                # Скачиваем клип на жесткий диск
                with open('clip.mp4', 'wb') as f:
                    f.write(requests.get(video_url).content)
                print("Клип успешно скачан!")
            else:
                print("Доступ к клипу ограничен.")
        else:
            print("Клип не найден в ответе.")
    else:
        print("Нет данных в ключе 'response'.")
else:
    # Выводим ошибку при плохом статусе ответа
    print(f"Ошибка запроса: {response.status_code}, Ответ: {response.text}")
