# -*- coding: utf-8 -*-
from werkzeug.datastructures import MultiDict
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from .storage import Storage
from . import forms


def make_key(*segments):
    return '/'.join(map(str, segments))


def do_vote\
    ( user_id
    , resource_id
    , score
    , score_range
    , namespace
    ):

    data = MultiDict(locals().copy())
    form = forms.CommonForm(data)
    if not form.validate():
        return {'error': form.errors}

    # Отмена голосования
    # Если пользовать проголосовал как 0 то удаляем запись о голосе
    if score == 0:
        return do_vote_cancel\
            ( user_id
            , resource_id
            , score_range
            , namespace
            )

    key = make_key(namespace, score_range, resource_id)

    # Если пользователь не голосовал
    user_key = make_key(key, user_id, 'score')
    user_data = int(Storage().get(user_key) or 0)
    with Storage() as storage:
        if user_data != score:
            do_vote_cancel\
                ( user_id
                , resource_id
                , score_range
                , namespace
                )
            user_data = None

        if not user_data:
            # Инкрементируем кол-во голосов
            storage.increment\
                ( make_key(key, 'count')
                , 1
                )
            # Увеличиваем общую сумму голосов
            storage.increment\
                ( make_key(key, 'sum')
                , score
                )
            # Сохраняем данные голосования пользователя
            storage.set(user_key, score)
            return True
        else:
            return False
dispatcher.add_method(do_vote, name='vote')


def do_vote_cancel\
    ( user_id
    , resource_id
    , score_range
    , namespace
    ):

    data = MultiDict(locals().copy())
    form = forms.CommonForm(data)
    if not form.validate():
        return {'error': form.errors}

    key = make_key(namespace, score_range, resource_id)
    user_key = make_key(key, user_id, 'score')
    score = Storage().get(user_key)

    # Получем кол-во голосов пользователя
    with Storage() as storage:
        if score is not None:
            # Декреметируем кол-во голосов
            storage.decrement\
                ( make_key(key, 'count')
                , 1
                )
            # Уменьшаем общую сумму голосов
            storage.decrement\
                ( make_key(key, 'sum')
                , score
                )
            # Удаляем информацию о голосе пользователя
            storage.delete(user_key)
    return True
dispatcher.add_method(do_vote_cancel, name='cancel_vote')


def get_rating\
    ( user_id
    , resource_id
    , score_range
    , namespace
    ):

    data = MultiDict(locals().copy())
    form = forms.CommonForm(data)
    if not form.validate():
        return {'error': form.errors}

    key = make_key\
        ( namespace
        , score_range
        , resource_id
        )
    score_count = int(Storage().get(make_key(key, 'count')) or 0)
    score_sum = int(Storage().get(make_key(key, 'sum')) or 0)

    print locals()


    return \
        { 'score':
          { 'count': score_count or 0
          , 'sum': score_sum or 0
          , 'avg': float(score_sum) / (score_count or 0)
          }
        , 'user': int(Storage().get(make_key(key, user_id, 'score')) or 0)
        }
dispatcher.add_method(get_rating, name='get_rating')


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle\
        ( request.data
        , dispatcher
        )
    return Response(response.json, mimetype='application/json')
