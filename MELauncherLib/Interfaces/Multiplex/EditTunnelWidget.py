from PyQt5.QtWidgets import QVBoxLayout, QWidget
from qmaterialwidgets import LineEdit


class EditTunnelWidget(QWidget):
    def __init__(
        self, tunnel_id: int, tunnel_name: str, local_ip: str, local_port: int, parent=None
    ):
        super().__init__(parent)
        self.verticalLayout = QVBoxLayout(self)
        self.tunnelNameEdit = LineEdit(self)
        self.verticalLayout.addWidget(self.tunnelNameEdit)
        self.localAddrEdit = LineEdit(self)
        self.verticalLayout.addWidget(self.localAddrEdit)
        self.localPortEdit = LineEdit(self)
        self.verticalLayout.addWidget(self.localPortEdit)

        self.tunnelNameEdit.setLabel("隧道名称")
        self.localAddrEdit.setLabel("本地IP")
        self.localPortEdit.setLabel("本地端口")
        self.setProperty("id", tunnel_id)
        self.tunnelNameEdit.setText(tunnel_name)
        self.localAddrEdit.setText(local_ip)
        self.localPortEdit.setText(str(local_port))
