class VkCallbackHandler:
    def __init__(self):
        pass

    # https://dev.vk.com/api/community-events/json-schema
    def handle(self, data):
        object_type = data.get('type')
        group_id = data.get('group_id')

        if object_type == 'confirmation' and group_id == 210765956:
            return {'type': 'confirmation', 'answer': 'c8b900bc'}

        # ruworship group
        if object_type == 'confirmation' and group_id == 210773307:
            secret_key = 'i3nFFNo9OkEZ1oU7uzbH'
            return {'type': 'confirmation', 'answer': '2ae608ab'}

        return None