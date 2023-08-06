from WeChatTool.exception import *


def check_msg_params(fun):
    def warp(*args, **kwargs):
        touser = kwargs.get('touser', [])
        toparty = kwargs.get('toparty', [])
        content = kwargs.get('content', '')
        if not touser and not toparty:
            raise ParamsError('require receive msg user or party')
        if not content or len(content) > 2048:
            raise ParamsError('require msg content or length is greater than 2048')
        if not isinstance(touser, list) or not isinstance(toparty, list):
            raise ParamsError('touser or toparty, must type list')
        ret = fun(*args, **kwargs)
        return ret
    return warp
