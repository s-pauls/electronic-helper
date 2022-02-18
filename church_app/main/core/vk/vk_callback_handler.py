class VkCallbackHandler:
    def __init__(self):
        pass

    def handle(self, data):
        object_type = data.get('type')
        group_id = data.get('group_id')

        if object_type == 'confirmation' and group_id == 210765956:
            return 'c8b900bc'

        # ruworship group
        if object_type == 'confirmation' and group_id == 210773307:
            secret_key = 'i3nFFNo9OkEZ1oU7uzbH'
            return '2ae608ab'

        return None