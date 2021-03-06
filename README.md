# rating-service

**Протокол**

json-rpc 2.0

**Транспорт** 

http

**Описание**

В сервисе представлены 3 метода 

* vote: Отправить результат лайка на сервер
* get_rating: Получить результат
* cancel_vote: Отменить результат
  
## vote

### аргументы:

#### user_id 
  **[A-Za-z0-9:_-]+**
  
  *id пользователя* от лица которого производится голосование.
  Если пользователю выдана сессия, то можно в качестве идентификации использовать ее.
  
#### resource_id
  **[A-Za-z0-9:_-]+**
  
  *id ресурса* который оцениваем

#### score
  **(int)**
  
  *Оценка* должна быть в диапазоне указанном в score_range 

#### score_range 
  **[-]?[0-9]+:[1-9]+**
  
  *Диапазон* в формате [от]:[до]
  
  *Пример*
  
    0 - определяет что пользователь не проголосовал*
    0:1 - только лайк
    -1:1 - (-1) дизлайк, (1) лайк
    -2:1 - (-2) дизлайк, -(1) воздержался (1) лайк
    0:5 - Голосование по 5 бальной шкале, от 1 до 5 
  
  *Примечание*
  
    Совокупность namespace, score_range, resource_id определяет ключ хранения результата голосования.
    Другими словами они отвечают на вопрос голосуем: где (namespace), как (score_range), что (resource_id) 
    Если хотя бы один из аргументов отличается считается как новое голосование.

**Пример запроса:**

    { "method": "vote"
    , "params": 
      [ "user/1"            // id пользователя  
      , "entry/1"           // id ресурса
      , 1                   // Оценка
      , "-1:1"              // Диапазон
      , "service-faq"       // Пространство имен
      ]
    , "jsonrpc": "2.0"
    , "id": 0
    }

**Ответ:**

    (true|false)?
    error - При неправильных форматах параметров

#### namespace
  **[a-z_]+**
  
  *Пространство имен* 

## get_rating

### аргументы:

Все те же что и при *vote* за исключением *оценки*

**Пример запроса**

    { "method": "get_rating"
    , "params": 
      [ 1
      , "entry/1"
      , "-1:1"
      , "service-faq"
      ]
    , "jsonrpc": "2.0"
    , "id": 0
    }
    
**Пример ответа**

    { "jsonrpc": "2.0"
    , "result":
      { "score":
        { "count": 2
        , "sum": 0
        , "avg": 0
        }
      , "user": 1
      }
    , "id": 0
    }

## cancel_vote

### аргументы:

**Пример запроса**

Все те же что и при *vote* за исключением *оценки*

    { "method": "cancel_vote"
    , "params": 
      [ 1
      , "entry/1"
      , "-1:1"
      , "service-faq"
      ]
    , "jsonrpc": "2.0"
    , "id": 0
    }
    
**Пример ответа**

    всегда true или ошибка
