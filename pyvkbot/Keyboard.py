from vk_api.keyboard import VkKeyboard


class Keyboard(VkKeyboard):
    """
    Keyboard for vk bot. Extends vk_api.keyboard.VkKeyboard

    :param one_time: [OPTIONAL. DEFAULT: False] If true, keyboard closes when user pushes the buttons
    :type one_time: bool

    :param inline: [OPTIONAL. DEFAULT: False] If ture, keyboard will be inline
    :type inline: bool
    """

    def __init__(self, one_time: bool = False, inline: bool = False):
        super().__init__(one_time=one_time, inline=inline)
