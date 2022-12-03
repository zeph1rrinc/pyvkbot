from vk_api.keyboard import VkKeyboard


class Keyboard(VkKeyboard):
    def __init__(self, one_time: bool = False, inline: bool = False):
        super().__init__(one_time=one_time, inline=inline)
