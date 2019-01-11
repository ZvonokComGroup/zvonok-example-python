import requests

# Полная и актуальная документация по API: https://calltools.ru/guide_api


CALLTOOLS_PUBLIC_KEY = 'test_public_key'
CALLTOOLS_BASE_URL = 'https://calltools.ru'
CALLTOOLS_TIMEOUT = 30


class CallToolsException(Exception):
    pass


def create_call(campaign_id, phonenumber, text=None, speaker='Tatyana'):
    '''
    Создание звонка на прозвон с генерацией ролика
    :type campaign_id: int
    :type phonenumber: str
    :type text: str|None
    :type speaker: str
    :rtype: dict
    '''
    resp = requests.get(CALLTOOLS_BASE_URL + '/lk/cabapi_external/api/v1/phones/call/', {
        'public_key': CALLTOOLS_PUBLIC_KEY,
        'phone': phonenumber,
        'campaign_id': campaign_id,
        'text': text,
        'speaker': speaker,
    }, timeout=CALLTOOLS_TIMEOUT)
    ret = resp.json()
    if ret['status'] == 'error':
        raise CallToolsException(ret['data'])
    return ret


def check_status(campaign_id, phonenumber=None, call_id=None,
            from_created_date=None, to_created_date=None,
            from_updated_date=None, to_updated_date=None):
    '''
    Получение статуса звонка по номеру телефона или по call_id (ID звонка)
    :type campaign_id: int
    :type phonenumber: str|None
    :type call_id: int|None
    :type from_created_date: str|None
    :type to_created_date: str|None
    :type from_updated_date: str|None
    :type to_updated_date: str|None
    :rtype: dict
    '''
    if phonenumber:
        url = '/lk/cabapi_external/api/v1/phones/calls_by_phone/'
    elif call_id:
        url = '/lk/cabapi_external/api/v1/phones/call_by_id/'
    else:
        raise ValueError('check_status required call_id or phonenumber')

    resp = requests.get(CALLTOOLS_BASE_URL + url, {
        'public_key': CALLTOOLS_PUBLIC_KEY,
        'phone': phonenumber,
        'call_id': call_id,
        'campaign_id': campaign_id,
        'from_created_date': from_created_date,
        'to_created_date': to_created_date,
        'from_updated_date': from_updated_date,
        'to_updated_date': to_updated_date,
    }, timeout=CALLTOOLS_TIMEOUT)

    ret = resp.json()
    if ret['status'] == 'error':
        raise CallToolsException(ret['data'])
    return ret


def remove_call(campaign_id, phonenumber=None, call_id=None):
    '''
    Удаление номера из прозвона
    :type campaign_id: int
    :type phonenumber: str|None
    :type call_id: int|None
    :rtype: dict
    '''
    if not phonenumber and not call_id:
        raise ValueError('remove_call required call_id or phonenumber')

    resp = requests.get(CALLTOOLS_BASE_URL + '/lk/cabapi_external/api/v1/phones/remove_call/', {
        'public_key': CALLTOOLS_PUBLIC_KEY,
        'phone': phonenumber,
        'call_id': call_id,
        'campaign_id': campaign_id,
    }, timeout=CALLTOOLS_TIMEOUT)
    ret = resp.json()
    if ret['status'] == 'error':
        raise CallToolsException(ret['data'])
    return ret


# Статусы звонка

ATTEMPTS_EXCESS_STATUS = 'attempts_exc'
USER_CUSTOM_STATUS = 'user'
NOVALID_BUTTON_STATUS = 'novalid_button'
COMPLETE_FINISHED_STATUS = 'compl_finished'
COMPLETE_NOFINISHED_STATUS = 'compl_nofinished'
DELETED_CALL_STATUS = 'deleted'
IN_PROCESS_STATUS = 'in_process'

HUMAN_STATUSES = [
    (IN_PROCESS_STATUS, 'В процессе'),
    (USER_CUSTOM_STATUS, 'Пользовательский IVR'),
    (ATTEMPTS_EXCESS_STATUS, 'Попытки закончились'),
    (COMPLETE_NOFINISHED_STATUS, 'Некорректный ответ'),
    (COMPLETE_FINISHED_STATUS, 'Закончен удачно'),
    (NOVALID_BUTTON_STATUS, 'Невалидная кнопка'),
    (DELETED_CALL_STATUS, 'Удалён из прозвона'),
]


# Статусы дозвона

DIAL_STATUS_WAIT = 0
DIAL_STATUS_FAILED = 1
DIAL_STATUS_HANGUP = 2
DIAL_STATUS_RING_TIMEOUT = 3
DIAL_STATUS_BUSY = 4
DIAL_STATUS_ANSWER = 5
DIAL_STATUS_ROBOT1 = 6
DIAL_STATUS_ROBOT2 = 7
DIAL_STATUS_NOVALID_BTN = 8
DIAL_STATUS_UNKNOWN = 9
DIAL_STATUS_WED = 10
DIAL_STATUS_USERSTOPLIST = 11
DIAL_STATUS_GLOBALSTOPLIST = 12
DIAL_STATUS_WED_WAIT = 13
DIAL_STATUS_ITSELF_EXC = 14
DIAL_STATUS_REMOVE = 15


DIAL_STATUSES = [
    (DIAL_STATUS_WAIT, 'Ожидание вызова (звонка еще нет)'),
    (DIAL_STATUS_FAILED, 'Ошибка при вызове абонента'),
    (DIAL_STATUS_HANGUP, 'Абонент сбросил звонок'),
    (DIAL_STATUS_RING_TIMEOUT, 'Не дозвонились'),
    (DIAL_STATUS_BUSY, 'Абонент занят'),
    (DIAL_STATUS_ANSWER, 'Абонент ответил'),
    (DIAL_STATUS_ROBOT1, 'Ответил автоответчик'),
    (DIAL_STATUS_ROBOT2, 'Ответил автоответчик'),
    (DIAL_STATUS_NOVALID_BTN, 'Невалидная кнопка'),
    (DIAL_STATUS_WED, 'Завершен без действия клиента'),
    (DIAL_STATUS_UNKNOWN, 'Неизвестный статус'),
    (DIAL_STATUS_USERSTOPLIST, 'Пользовательский стоп-лист'),
    (DIAL_STATUS_GLOBALSTOPLIST, 'Глобальный стоп-лист'),
    (DIAL_STATUS_WED_WAIT, 'Абонент ответил, но продолжительности разговора не достаточно для фиксации результата в статистике'),
    (DIAL_STATUS_ITSELF_EXC, 'Номер абонента совпадает с CallerID'),
    (DIAL_STATUS_REMOVE, 'Номер удалён из прозвона'),
]


# Примеры использование postback в django:


class PostBackForm(forms.Form):

    ct_campaign_id = forms.IntegerField()
    ct_phone = PhoneNumberField()  # See https://github.com/stefanfoulis/django-phonenumber-field
    ct_call_id = forms.IntegerField()
    ct_completed = forms.DateTimeField(required=False)
    ct_status = forms.CharField(required=False)
    ct_dial_status = forms.IntegerField()
    ct_button_num = forms.IntegerField(required=False)
    ct_duration = forms.FloatField(required=False)


def calltools_postback(request):

    form = PostBackForm(request.GET or None)

    if form.is_valid():
        CallToolsPostBackResult.objects.create(**form.cleaned_data)

    return HttpResponse('OK')
