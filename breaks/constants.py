BREAK_CREATED_STATUS = 'created'
BREAK_CONFIRMED_STATUS = 'confirmed'
BREAK_ON_BREAK_STATUS = 'on_break'
BREAK_FINISHED_STATUS = 'finished'
BREAK_CANCELLED_STATUS = 'cancelled'

REPLACEMENT_MEMBER_OFFLINE = 'offline'
REPLACEMENT_MEMBER_ONLINE = 'online'
REPLACEMENT_MEMBER_BUSY = 'busy'
REPLACEMENT_MEMBER_BREAK = 'break'

BREAK_ALL_STATUSES = [
    BREAK_CREATED_STATUS,
    BREAK_CONFIRMED_STATUS,
    BREAK_ON_BREAK_STATUS,
    BREAK_FINISHED_STATUS,
    BREAK_CANCELLED_STATUS,
]
BREAK_CREATED_DEFAULT = {
                    'name': 'Создано',
                    'is_active' : True,
                    'sort' : 100,
                }