# -*- coding: utf-8 -*-
from werkzeug.datastructures import MultiDict
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from .storage import default_storage
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
    form = forms.DoVoteForm(data)
    form.validate()

    # Отмена голосования
    # Если пользовать проголосовал как 0 то удаляем запись о голосе
    if score == 0:
        return do_cancel_vote(user_id, resource_id, score_range, namespace)

    key = make_key(namespace, score_range, resource_id)
    # Если пользователь не голосовал
    # TODO: atomic
    user_key = make_key(key, user_id, 'score')
    if not default_storage.get(user_key):
        # Инкрементируем кол-во голосов
        default_storage.increment\
            ( make_key(key, 'count')
            , 1
            )
        # Увеличиваем общую сумму голосов
        default_storage.increment\
            ( make_key(key, 'sum')
            , score
            )
        # Сохраняем данные голосования пользователя
        default_storage.set(user_key, score)
        return True
    else:
        return False
dispatcher.add_method(do_vote, name='do.vote')


def do_cancel_vote\
    ( user_id
    , resource_id
    , score_range
    , namespace
    ):
    # Получем кол-во голосов пользователя
    # TODO: atomic
    key = make_key(namespace, score_range, resource_id)
    user_key = make_key(key, user_id, 'score')
    score = default_storage.get(user_key)
    if score is not None:
        # Декреметируем кол-во голосов
        default_storage.decrement\
            ( make_key(key, 'count')
            , 1
            )
        # Уменьшаем общую сумму голосов
        default_storage.decrement\
            ( make_key(key, 'sum')
            , score
            )
        # Удаляем информацию о голосе пользователя
        default_storage.delete(user_key)
    return True
dispatcher.add_method(do_cancel_vote, name='do.cancel.vote')


def get_rating\
    ( user_id
    , resource_id
    , score_range
    , namespace
    ):
    key = make_key(namespace, score_range, resource_id)
    score_count = default_storage.get(make_key(key, 'count'))
    score_sum = default_storage.get(make_key(key, 'sum'))
    return \
        { 'score':
          { 'count': score_count or 0
          , 'sum': score_sum or 0
          , 'avg': float(score_sum) / score_count if score_count else 0
          }
        , 'user': default_storage.get(make_key(key, user_id, 'score'))
        }
dispatcher.add_method(get_rating, name='get.rating')


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle\
        ( request.data
        , dispatcher
        )
    return Response(response.json, mimetype='application/json')
