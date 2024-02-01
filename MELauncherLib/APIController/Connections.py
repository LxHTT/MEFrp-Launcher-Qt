from PyQt5.QtCore import pyqtSignal, QThread
from MEFrpLib import (
    me_get_user_info,
    me_user_sign,
    me_refresh_user_token,
    me_get_realname_status,
    me_post_realname,
    me_get_tunnel_list,
    me_get_tunnel_config_node,
    me_get_tunnel_config_id,
    me_create_tunnel,
    me_delete_tunnel,
    me_get_tunnel_info,
    me_node_list,
    me_login,
    me_get_sponsor,
    me_get_statistics,
    me_register,
    me_send_register_email,
    me_forgot_password,
    me_get_setting,
)
from MEFrpLib.models import JSONReturnModel, TextReturnModel
from ..AppController.Settings import cfg

class BaseJSONThread(QThread):
    returnSlot = pyqtSignal(JSONReturnModel)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        raise NotImplementedError


class BaseTextThread(QThread):
    returnSlot = pyqtSignal(TextReturnModel)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        raise NotImplementedError


class GetUserInfoThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_user_info(self.authorization, self.bypass_proxy))


class UserSignThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_user_sign(self.authorization, self.bypass_proxy))


class RefreshUserTokenThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_refresh_user_token(self.authorization, self.bypass_proxy))


class GetRealnameStatusThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_realname_status(self.authorization, self.bypass_proxy))


class PostRealnameThread(BaseJSONThread):
    def __init__(self, authorization: str, idcard: str, name: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.idcard = idcard
        self.name = name
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_post_realname(self.authorization, self.idcard, self.name, self.bypass_proxy)
        )


class GetTunnelListThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_tunnel_list(self.authorization, self.bypass_proxy))


class GetTunnelConfigNodeThread(BaseTextThread):
    def __init__(self, authorization: str, node: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.node = node
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_config_node(self.authorization, self.node, self.bypass_proxy)
        )


class GetTunnelConfigIdThread(BaseTextThread):
    def __init__(self, authorization: str, id: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.id = id
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_config_id(self.authorization, self.id, self.bypass_proxy)
        )


class CreateTunnelThread(BaseJSONThread):
    def __init__(
        self,
        authorization: str,
        node: int,
        proxy_type: str,
        local_ip: str,
        local_port: int,
        remote_port: int,
        proxy_name: str,
        parent=None,
    ):
        super().__init__(parent)
        self.authorization = authorization
        self.node = node
        self.proxy_type = proxy_type
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_port = remote_port
        self.proxy_name = proxy_name
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_create_tunnel(
                self.authorization,
                self.node,
                self.proxy_type,
                self.local_ip,
                self.local_port,
                self.remote_port,
                self.proxy_name,
                self.bypass_proxy,
            )
        )


class DeleteTunnelThread(BaseJSONThread):
    def __init__(self, authorization: str, tunnel_id: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.tunnel_id = tunnel_id
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_delete_tunnel(self.authorization, self.tunnel_id, self.bypass_proxy)
        )


class GetTunnelInfoThread(BaseJSONThread):
    def __init__(self, authorization: str, tunnel_id: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.tunnel_id = tunnel_id
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_info(self.authorization, self.tunnel_id, self.bypass_proxy)
        )


class NodeListThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_node_list(self.authorization, self.bypass_proxy))


class LoginThread(BaseJSONThread):
    def __init__(self, username: str, password: str, parent=None):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_login(self.username, self.password, self.bypass_proxy))


class GetSponsorThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_sponsor(self.bypass_proxy))


class GetStatisticsThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_statistics(self.bypass_proxy))


class RegisterThread(BaseJSONThread):
    def __init__(
        self, email: str, username: str, password: str, code: str, parent=None
    ):
        super().__init__(parent)
        self.email = email
        self.username = username
        self.password = password
        self.code = code
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_register(self.email, self.username, self.password, self.code, self.bypass_proxy)
        )


class SendRegisterEmailThread(BaseJSONThread):
    def __init__(self, email: str, parent=None):
        super().__init__(parent)
        self.email = email
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_send_register_email(self.email, self.bypass_proxy))


class ForgotPasswordThread(BaseJSONThread):
    def __init__(self, email: str, username: str, parent=None):
        super().__init__(parent)
        self.email = email
        self.username = username
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_forgot_password(self.email, self.username, self.bypass_proxy))


class GetSettingThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_setting(self.bypass_proxy))
