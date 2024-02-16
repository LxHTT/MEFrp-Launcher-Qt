#                    Copyright 2024, LxHTT.
#
#     Part of "MEFrp-Launcher-Qt", a frpc launcher for ME Frp.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/LxHTT/MEFrp-Launcher-Qt/raw/master/LICENSE
#
################################################################################

from PyQt5.QtCore import pyqtSignal, QThread
from MEFrpLib import (
    me_get_user_info,
    me_user_get_sign_info,
    me_user_sign,
    me_refresh_user_token,
    me_get_realname_status,
    me_post_realname,
    me_get_tunnel_list,
    me_get_tunnel_config_node,
    me_get_tunnel_config_id,
    me_create_tunnel,
    me_edit_tunnel,
    me_close_tunnel,
    me_delete_tunnel,
    me_node_list,
    me_login,
    me_get_sponsor,
    me_get_statistics,
    me_register,
    me_send_register_email,
    me_forgot_password,
    me_get_setting,
    me_get_free_port,
)
from MEFrpLib.models import JSONReturnModel, TextReturnModel
from ..AppController.Settings import cfg
from .. import USER_AGENT


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
        self.returnSlot.emit(
            me_get_user_info(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class UserGetSignInfoThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_user_get_sign_info(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class UserSignThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_user_sign(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class RefreshUserTokenThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_refresh_user_token(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class GetRealnameStatusThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_realname_status(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class PostRealnameThread(BaseJSONThread):
    def __init__(self, authorization: str, idcard: str, name: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.idcard = idcard
        self.name = name
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_post_realname(
                authorization=self.authorization,
                idcard=self.idcard,
                name=self.name,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class GetTunnelListThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_list(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class GetTunnelConfigNodeThread(BaseTextThread):
    def __init__(self, authorization: str, node: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.node = node
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_config_node(
                authorization=self.authorization,
                node=self.node,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class GetTunnelConfigIdThread(BaseTextThread):
    def __init__(self, authorization: str, id: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.id = id
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_tunnel_config_id(
                authorization=self.authorization,
                id=self.id,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
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
        domain: str,
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
        self.domain = domain
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        if "http" not in self.proxy_type:
            self.returnSlot.emit(
                me_create_tunnel(
                    authorization=self.authorization,
                    node=self.node,
                    proxy_type=self.proxy_type,
                    local_ip=self.local_ip,
                    local_port=self.local_port,
                    remote_port=self.remote_port,
                    proxy_name=self.proxy_name,
                    bypass_proxy=self.bypass_proxy,
                    ua=USER_AGENT,
                )
            )
        else:
            self.returnSlot.emit(
                me_create_tunnel(
                    authorization=self.authorization,
                    node=self.node,
                    proxy_type=self.proxy_type,
                    local_ip=self.local_ip,
                    local_port=self.local_port,
                    remote_port=self.remote_port,
                    proxy_name=self.proxy_name,
                    domain=self.domain,
                    bypass_proxy=self.bypass_proxy,
                    ua=USER_AGENT,
                )
            )


class EditTunnelThread(BaseJSONThread):
    def __init__(
        self,
        authorization: str,
        tunnel_id: int,
        tunnel_name: str,
        local_port: str,
        local_ip: str,
        parent=None,
    ):
        super().__init__(parent)
        self.authorization = authorization
        self.tunnel_id = tunnel_id
        self.tunnel_name = tunnel_name
        self.local_port = local_port
        self.local_ip = local_ip
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_edit_tunnel(
                authorization=self.authorization,
                tunnel_id=self.tunnel_id,
                tunnel_name=self.tunnel_name,
                local_port=self.local_port,
                local_ip=self.local_ip,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class KillTunnelAPIThread(BaseJSONThread):
    def __init__(self, authorization: str, tunnel_id: int, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.tunnel_id = tunnel_id
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_close_tunnel(
                authorization=self.authorization,
                tunnel_id=self.tunnel_id,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
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
            me_delete_tunnel(
                authorization=self.authorization,
                tunnel_id=self.tunnel_id,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


# class GetTunnelInfoThread(BaseJSONThread):
#     def __init__(self, authorization: str, tunnel_id: int, parent=None):
#         super().__init__(parent)
#         self.authorization = authorization
#         self.tunnel_id = tunnel_id
#         self.bypass_proxy = cfg.get(cfg.bypassProxy)

#     def run(self):
#         self.returnSlot.emit(
#             me_get_tunnel_info(
#                 authorization=self.authorization,
#                 tunnel_id=self.tunnel_id,
#                 bypass_proxy=self.bypass_proxy,
#                 ua=USER_AGENT,
#             )
#         )


class NodeListThread(BaseJSONThread):
    def __init__(self, authorization: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_node_list(
                authorization=self.authorization, bypass_proxy=self.bypass_proxy, ua=USER_AGENT
            )
        )


class LoginThread(BaseJSONThread):
    def __init__(self, username: str, password: str, parent=None):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_login(
                username=self.username,
                password=self.password,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class GetSponsorThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_sponsor(bypass_proxy=self.bypass_proxy, ua=USER_AGENT))


class GetStatisticsThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_statistics(bypass_proxy=self.bypass_proxy, ua=USER_AGENT))


class RegisterThread(BaseJSONThread):
    def __init__(self, email: str, username: str, password: str, code: str, parent=None):
        super().__init__(parent)
        self.email = email
        self.username = username
        self.password = password
        self.code = code
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_register(
                email=self.email,
                username=self.username,
                password=self.password,
                code=self.code,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class SendRegisterEmailThread(BaseJSONThread):
    def __init__(self, email: str, parent=None):
        super().__init__(parent)
        self.email = email
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_send_register_email(email=self.email, bypass_proxy=self.bypass_proxy, ua=USER_AGENT)
        )


class ForgotPasswordThread(BaseJSONThread):
    def __init__(self, email: str, username: str, parent=None):
        super().__init__(parent)
        self.email = email
        self.username = username
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_forgot_password(
                email=self.email,
                username=self.username,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )


class GetSettingThread(BaseJSONThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(me_get_setting(bypass_proxy=self.bypass_proxy, ua=USER_AGENT))


class GetFreePortThread(BaseJSONThread):
    def __init__(self, authorization: str, id: int, protocol: str, parent=None):
        super().__init__(parent)
        self.authorization = authorization
        self.id = id
        self.protocol = protocol
        self.bypass_proxy = cfg.get(cfg.bypassProxy)

    def run(self):
        self.returnSlot.emit(
            me_get_free_port(
                authorization=self.authorization,
                id=self.id,
                protocol=self.protocol,
                bypass_proxy=self.bypass_proxy,
                ua=USER_AGENT,
            )
        )
