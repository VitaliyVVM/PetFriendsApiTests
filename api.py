import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"  # при каждом вызове используем url

    def get_api_key(self, email, password):  # реализуем метод получения аутентификационного ключа

        headers = {  # смотрим документацию api, как передаются имэйл и пасс
            "email": email,
            "password": password
        }

        res = requests.get(self.base_url+"api/key", headers=headers)  # результат запроса сохраняем в переменную
        status = res.status_code  # статус типа 200
        result = ""
        try:
            result = res.json()  # сохраняем api-key в json, но если он не прочитается, пишем исключение
        except:
            result = res.text  # и пытаемся сохранить в текст
        return status, result  # возвращаем полученные данные

    def get_list_of_pets(self, auth_key, filter):  # названия параметров смотрим в апи-документации
        # реализуем метод получения списка своих питомцев
        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        # реализуем метод создания нового питомца
        data = MultipartEncoder(  # нужен, так как передаем json и картинку
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}
        res = requests.post(self.base_url+"api/pets", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        # реализуем метод удаления одного из своих питомцев

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str):
        # реализуем метод обновления инфы одного из своих питомцев

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str):
        # реализуем метод создания питомца без фото

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {"auth_key": auth_key["key"]}
        res = requests.post(self.base_url+"api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        # реализуем метод добавления/изменения фото одного из своих питомцев

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet_without_photo_norequired_params(self, auth_key: json, animal_type: str, age: str):
        # Попробуем создать питомца без обязательного параметра name

        data = {
            'animal_type': animal_type,
            'age': age
        }
        headers = {"auth_key": auth_key["key"]}
        res = requests.post(self.base_url+"api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet_without_photo_invalid_datatype(self, auth_key: json, name: str, animal_type: int, age: str):
        # метод создания питомца с неправильным параметром - числовым вместо строки

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {"auth_key": auth_key["key"]}
        res = requests.post(self.base_url+"api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet_all_params_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        # реализуем метод создания нового питомца
        data = MultipartEncoder(  # нужен, так как передаем json и картинку
            fields={
                'name': (name, open(name, 'rb'), 'image/jpeg'),
                'animal_type': (animal_type, open(animal_type, 'rb'), 'image/jpeg'),
                'age': (age, open(age, 'rb'), 'image/jpeg'),
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}
        res = requests.post(self.base_url+"api/pets", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
