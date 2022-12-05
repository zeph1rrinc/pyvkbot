class ActionTypes:
    """
    Types of action events
    """
    CHAT_PHOTO_UPDATE = 'chat_photo_update'

    CHAT_PHOTO_REMOVE = 'chat_photo_remove'

    CHAT_CREATE = 'chat_create'

    CHAT_TITLE_UPDATE = 'chat_title_update'

    CHAT_INVITE_USER = 'chat_invite_user'

    CHAT_KICK_USER = 'chat_kick_user'

    CHAT_PIN_MESSAGE = 'chat_pin_message'

    CHAT_UNPIN_MESSAGE = 'chat_unpin_message'

    CHAT_INVITE_USER_BY_LINK = 'chat_invite_user_by_link'


class EventTypes:
    """
    Types of events
    """
    MESSAGE = 'message'

    ACTION = 'action'

    ATTACHMENT = 'attachment'


class AttachmentTypes:
    """
    Types of attachments
    """
    PHOTO = 'photo'

    VIDEO = 'video'

    AUDIO = 'audio'

    DOC = 'doc'

    AUDIO_MESSAGE = 'audio_message'
