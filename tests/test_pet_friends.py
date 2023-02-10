import os
from api import PetFriends
from settings import *

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password): #тест получение ключа
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result  #наличие key в result
    print(f'***API ключ: {status},\n{result}')


def test_get_all_pets_with_valid_key(filter='my_pets'):  #тест вывод списка питомцев по фильрту. filter = '' или my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(f'***Список питомцев: {status},\n{result}')


def test_add_new_pet_with_valid_data(name='PeT1', animal_type='type1', age='5', pet_photo='images/pet1.jpg'): #тест добавления нового питомца с корректными данными
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец: {status},\n{result}')


def test_successful_delete_self_pet():  #тест возможность удаления питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password) #получение и сохранение ключа
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets") # запрос списка всех питомцев
    # Если список своих питомцев пустой, добавить нового и снова запросить список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "NewPat", "newpat", "3", "images/pet1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    print("***Питомец с ID: ", pet_id, " Удалён")


def test_successful_update_self_pet_info(name='Pet1_Changed2', animal_type='type_changed', age=7): #тест возможность обновить информацию о питомце
    # Получаем ключ в auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print(result, "Обновлено")
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#----напишите 10 различных тестов для данного REST API интерфейса

def test_add_new_pet_with_valid_data_without_photo(name = 'PeT1NoImage', animal_type = 'type1', age = '5'): #тест добавления нового питомца с корректными данными (БЕЗ ФОТО)
    #pet_photo = os.path.join(os.path.dirname(__file__)) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age) #добавление питомца (без фото)
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец (без фото): {status},\n{result}')


def test_successful_add_pet_photo(pet_photo='images/pet2.jpg'): #тест возможность добавить фото питомцу
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)  # получение полного пути изображения и его сохранение в переменную pet_photo
    # Получаем ключ в auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_a_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        # Проверяем что статус ответа = 200 и фото соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(result, "Добвалено фото")
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_with_Invalid_email(email=Invalid_email, password=valid_password): #тест получение ключа при невенром email
    status, result = pf.get_api_key(email, password)
    #assert status == 200
    assert 'key' not in result  #наличие key в result
    print(f'***Неверный email, код: {status},\n{result}')


def test_get_api_key_with_Invalid_password(email=valid_email, password=Invalid_password): #тест получение ключа при неверном пароле
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result  #наличие key в result
    print(f'***Неверный пароль, код: {status},\n{result}')


def test_get_api_key_with_Invalid_password_Invalid_email(email=Invalid_email, password=Invalid_password): #тест получение ключа при неверном email и неверном пароле
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result  #наличие key в result
    print(f'***Неверный email и неверный пароль, код: {status},\n{result}')


def test_get_all_pets_with_valid_key_with_Invalid_Filter(filter='My_pets'):  #тест вывод списка питомцев по фильтру при неверном значении фильтра. (filter должен = '' или my_pets)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    print(f'***Значение filter: {filter} недоступно, код: {status}')


def test_add_new_pet_with_Invalid_data_photo(name='PeT1', animal_type='type1', age='5', pet_photo='images/PeT12.jpg'): #тест добавления нового питомца с некорректными данными (неправильный путь к фото)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo

    if not os.path.exists(pet_photo):  # проверка наличия фото при добвалнеии питомца
        print(f'\n Фото не найдено! Использовано фото pet2 {pet_photo}')
        pet_photo = "images/pet2.jpg" #использовать доступное фото

    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец: {status},\n{result}')


def test_add_new_pet_with_Invalid_data_age(name='PeT1', animal_type='type1', age='-1', pet_photo='images/pet1.jpg'): #тест добавления нового питомца с некорректными данными (отрицательный возраст)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    assert (float(age) < 0)
    print(f'Статус код: {status}, при добавлении питомца с отрицательным возрастом! ({age})')
    print(f'***Новый питомец: {status},\n{result}')


def test_add_new_pet_with_Invalid_data_format(name='PeT1', animal_type='type1', age="dvadcat'", pet_photo='images/pet1.jpg'): #тест добавления нового питомца с некорректными данными (текст в поле возрст)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    print(f'Статус код: {status}, при добавлении питомца с текстом в поле "возраст"! ({age})')
    print(f'***Новый питомец: {status},\n{result}')


def test_add_pet_with_valid_data_empty(name='', animal_type='', age='', pet_photo='images/pet1.jpg'):  #тест добавления нового питомца с пустыми значениями
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    print(f'***Добавлен "питомец с пустыми значениями полей: "name", "animal_type", "age". ( {result})')