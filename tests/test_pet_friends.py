from api import PetFriends  # импортируем нашу библиотеку
from settings import valid_email, valid_password, empty_email, empty_password  # и регистрационные данные


pf = PetFriends()  # инициализируем библиотеку в переменную


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):  # пишем тесты
    status, result = pf.get_api_key(email, password)  # вызываем метод из библиотеки, результаты сохраняем в переменные
    assert status == 200  # сверяем полученный результат с ожиданием
    assert "key" in result  # провеяряем, что ключ получен, т.к. всё ок, пишем следующие методы в api.py


def test_get_all_pets_with_valid_key(filter=""):  # фильтр пустой по умолчанию
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # _ это status, тк не нужен, оставляем пустым
    status, result = pf.get_list_of_pets(auth_key, filter)  # здесь уже получаем статус и результат
    assert status == 200
    assert len(result["pets"]) > 0  # так как возвращается список в json, то такое условие


def test_add_new_pet_with_valid_data(name="Белка195", animal_type="зверушка", age="4", pet_photo="images/manul.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name


def test_successful_delete_self_pet():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Потеряшка", "зубр", "19", "images/manul.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Лунтик', animal_type='сервал', age='7'):
    # Проверка возможности обновления информации о питомце

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_valid_data(name="ДжаДжаБинг", animal_type="ктулху", age="68"):
    # Проверка возможности создания питомца без фото

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_successful_add_pet_photo():
    # Проверка возможности добавления фото питомцу

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    foto = my_pets['pets'][0]['pet_photo']  # фото питомца на сайте до добавления нового

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], "images/trubkozub.jpg")
        assert status == 200
        assert foto != result["pet_photo"]  # проверка, что фото действительно поменялось, и оно отличается от старого
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_for_valid_user_empty_password(email=valid_email, password=empty_password):
    # Проверка возможности получить auth_key с существующей почтой и пустым паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result  # убедиться, что ключ действительно не получен


def test_add_new_pet_without_photo_empty_data(animal_type="безымянное", age="26"):
    # Проверка возможности создания питомца без обязательного параметра name

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo_norequired_params(auth_key, animal_type, age)
    assert status == 400


def test_add_new_pet_without_photo_invalid_datatype(name="HelloKitty", animal_type=159, age="68"):
    # Проверка возможности создания питомца с числовым параметром вместо строкового

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo_invalid_datatype(auth_key, name, animal_type, age)
    assert status == 400  # тест падает, код 200, питомец успешно создается


def test_successful_delete_non_self_pet():
    # Проверка возможности удаления валидного НЕ СВОЕГО спитомца
    # Авторизуемся под собой, а пытаемся удалить питомца другого пользователя

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = "4287584b-1a55-4e6c-b2e2-a1757fad3ccf"  # валидный id чужого питомца
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 403  # тест падает, код 200, чужой питомец успешно удаляется


def test_add_new_pet_without_photo_long_name(name="цЬлПрЧэзСъптПтШьИЮЛЩБЦодхЁшОЯБсМвужОчоЫыыЭхБяиЪиРжзсОьуВзБФмиоЙ"
                                                  "хАМЮЯЪЁМТпьУхшЛФМеВвцхиуИЪцЙПВлщнЛжЕХлхЖфЬщЗшюЫОРуеЭяпЪэЧчйНИЭН"
                                                  "ювНэОюьЮшЖПВбоНгкХДТаШаМяЮяцКЮлТЩцЙПщыокГлщДзШИшПСмжЪзмДРБИЛоБл"
                                                  "ХтГйЮЛрВьЧэВКЮФпЕГЁКгбЭвнЩшрбМЮыжтГлМЖрэГфуыкЭлрзАЩОййОфнБмГёвД"
                                                  "пуЁЙиТЙутбдчаыТцьхЛщьъЗёйжюЭаУЭыХыпэзХтШСсЪалялпчХНойрСщлэлЪЕоН"
                                                  "ншЙЭфрЙНяъызУтШЕФЛШЯщвБИАшфбЩэчЙемёБэМяойпЯОьтАнаТФШягуКжфиёОцО"
                                                  "ХЫХШЪрФКЦТчГДФцлйОнЁТХЛпЗяхТтющьиПКиВЭЙЮеьонгЬыхщыыБДбюЗъъБПйМз"
                                                  "ЗяФмрИхЕьэФЫГфнгбдтЯЭПХяЮЬбСчЖысСЮОЫЬпгИМхАКШЬьТхЪЭЭБгЪЗЁСКЮчИЫ"
                                                  "ёОхьачйАДЙоИпщчЁёЪщЖяВЕЛМЖЬДШмЧзХАцбэъзНЩёкЧтещвБНАИЧЁЙЙхМЁьТущ"
                                                  "ёЫсЬаАЧУдшхРяДинкШОлИйСЭГсеАеБЛоХпеэЁфЗЧМфужочмыЩФСЧКЕЩЫУёОыЗНъ"
                                                  "ЙнШбмМееюИхаЖнЬцЙХеЯчеПЧвОэхфеНпёюшёьЭяУДаФДатПцёЫдСЙищепутюХХю"
                                                  "ъцчпЁицУанщОяхёУЗОчЯЗооТумбЭЁюОЛжГаШЭПшХешзАцаалМКЙАдИвНСлПЦЩЭя"
                                                  "ьзъьЯМдоллрУВрЛРИРГСЬИДВСъсЛЫясетТНбДЫзуАатЮЦпнЫЗнюшФщплХжПфкяО"
                                                  "сЬУСЯГФЭЮвХдцжЫМЕЪёСбПЩиАЪфшДШХЩжДЭсОЦБёКъЪУлЦПЩаУГяуёлКЪюХЦИЪЛ"
                                                  "кЗсЕчыКЛпЖлоЬрУЕЖфйЧЗРбщхКЧГНчРюЧыйПдйМщЛождВШХЩПЖаФыЩЬКенжУНЮи"
                                                  "ЫщЫЫхЗрОГЧИМЪыштПЦУаХщБЭлУФЬмощдЖоТалзЧкКфэъРББСЪФЛыоцУекд",
                                             animal_type="уродец", age="99"):
    # Проверка возможности создания питомца с длинным именем, 1003 буквы

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_add_new_pet_with_valid_data_empty_key(name="Чучело", animal_type="Мяучело", age="44",
                                               pet_photo="images/manul.jpg"):
    # Проверка возможности создания питомца без авторизации с пустым auth_key

    auth_key = {"key": ""}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403


def test_add_new_pet_with_invalid_name(name="<`/*?'^;)-&@~[>\:", animal_type="Выхухоль", age="29",
                                       pet_photo="images/fine.png"):
    # Проверка возможности создания питомца с именем, состоящим только из спецсимволов

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400  # тест падает, код 200, питомец успешно создается
    assert result["name"] == name


def test_get_api_key_for_valid_password_empty_email(email=empty_email, password=valid_password):
    # Проверка возможности получить auth_key с существующим паролем и пустой почтой

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result  # убедиться, что ключ действительно не получен


def test_add_new_pet_with_invalid_photo_extension(name="Молния", animal_type="трубкозуб", age="51",
                                                  pet_photo="images/trubkozub.tiff"):
    # Проверка возможности создать питомца с фото, расширение которого не упоминается в api-документации
    # Сказано, следует использовать JPG, JPEG или PNG, попробуем скормить ему TIFF

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400  # tiff тоже можно, тест падает, питомец создан
    assert result["name"] == name