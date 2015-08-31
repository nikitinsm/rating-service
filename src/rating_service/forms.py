# -*- coding: utf-8 -*-
import wtforms


def range_filter(value):
    try:
        begin, end = map(int, value.split(':', 1))
        assert begin < end
        return begin, end
    except Exception as e:
        raise wtforms.ValidationError('score_range must be in format [n1]:[n2] where n1 < n2')



class CommonForm(wtforms.Form):
    user_id = wtforms.StringField\
        ( validators=
          [ wtforms.validators.Regexp
            ( r'[A-Za-z0-9:_-]+'
            , message='value must satisfy regex "[A-Za-z0-9_-]+"'
            )
          , wtforms.validators.Required()
          ]
        , filters=
          [ str
          , ]
        , )
    resource_id = wtforms.StringField\
        ( validators=
          [ wtforms.validators.Regexp
            ( r'[A-Za-z0-9_-]+'
            , message='value must satisfy regex "[A-Za-z0-9_-]+"'
            )
          , wtforms.validators.Required()
          ]
        , filters=
          [ str
          , ]
        )
    score_range = wtforms.StringField\
        ( validators=
          [ wtforms.validators.Regexp
            ( r'[-]?[0-9]+:[1-9]+'
            , message='value must satisfy regex "[-]?[0-9]+:[1-9]+"'
            )
          , wtforms.validators.Required()
          ]
        , filters=
          [ str
          , ]
        , )
    namespace = wtforms.StringField\
        ( validators=
          [ wtforms.validators.Regexp
            ( r'[a-z_]+'
            , message='value must satisfy regex "[a-z_]+"'
            )
          , wtforms.validators.Required()
          ]
        , filters=
          [ str
          , ]
        , )


class VoteForm(CommonForm):
    score = wtforms.IntegerField\
        ( validators=
          [ wtforms.validators.Required()
          , ]
        , filters=
          [ range_filter
          , ]
        )

    def validate(self):
        result = super(VoteForm, self).validate()
        score_range = range_filter(self['score_range'].data)
        score = self['score'].data

        if not score_range[0] <= score <= score_range[1]:
            raise wtforms.ValidationError('Score %s is out of range %s' % (score, self['score_range'].data))
        return result