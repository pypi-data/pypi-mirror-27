from .base import BaseData, OptionalDict


class MessageCreateData(BaseData):
    def __init__(self, title=None, content=None, skip_type=None, skip_target=None,
                 content_clickable=None, send_nick_name=None, type=None,
                 target_user_id=None, send_at=None):
        """
        title	否	string	消息标题
        content	是	string	消息内容
        skip_type	否	int	跳转类型 0-不跳转 1-图文 2-音频 3-视频 5-跳转外部链接 6-专栏
        skip_target	否	string	跳转外部链接时填完整链接，跳资源时填资源id，非跳转消息不填该字段
        content_clickable	否	string	可点击的文字内容，非跳转消息不填该字段
        send_nick_name	否	string	发送人的昵称，例如：管理员
        type	是	int	消息类型 0-私人消息 1-群发消息
        target_user_id	否	string	消息触达人的user_id，群发消息不填该字段
        send_at	否	string	消息发送时间，unix 时间戳
        """
        self.data = OptionalDict()
        self.data['title'] = title
        self.data['content'] = content
        self.data['skip_type'] = skip_type
        self.data['skip_target'] = skip_target
        self.data['content_clickable'] = content_clickable
        self.data['send_nick_name'] = send_nick_name
        self.data['type'] = type
        self.data['target_user_id'] = target_user_id
        self.data['send_at'] = send_at


class MessageQueryData(BaseData):
    def __init__(self, order=None, page_index=None, page_size=None, user_id=None, state=None):
        """
        order	否	string	1（默认）降序，0升序
        page_index	否	string	页码，从0开始，默认为0
        page_size	否	string	每页请求条数，最大支持300，默认取10条
        user_id	是	string	用户id
        state	否	string	状态 0-正常 1-被撤回，默认全部
        """
        self.data = OptionalDict()
        self.data['order'] = order
        self.data['page_index'] = page_index
        self.data['page_size'] = page_size
        self.data['user_id'] = user_id
        self.data['state'] = state
