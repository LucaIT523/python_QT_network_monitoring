from PySide6.QtWidgets import QDialog
class IPCalculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        from Forms.ui_dialog_ip_calculator import Ui_DialogIPCalculator
        self.ui = Ui_DialogIPCalculator()
        self.ui.setupUi(self) 

        self.initData()

    def initData(self):
        self.ui.comboBox_IPVersion.addItems(["IPv4", "IPv6"])

        self.ui.pushButton_Calculate.clicked.connect(self.onCalculate)
        self.ui.comboBox_IPVersion.currentTextChanged.connect(self.onVersionChanged)
        
        self.ui.comboBox_IPVersion.setCurrentIndex(0)
        self.onVersionChanged("IPv4")

    def onVersionChanged(self, version):
        if version == "IPv4":
            self.ui.lineEdit_ip_address.setPlaceholderText("e.g. 192.168.1.1")
            self.ui.lineEdit_SubnetMask.setPlaceholderText("e.g. 255.255.255.0 or /24")
        else:
            self.ui.lineEdit_ip_address.setPlaceholderText("e.g. 2001:db8::1")
            self.ui.lineEdit_SubnetMask.setPlaceholderText("e.g. /64")

    def onCalculate(self):
        import ipaddress
        try:
            ip_str = self.ui.lineEdit_ip_address.text().strip()
            subnet_str = self.ui.lineEdit_SubnetMask.text().strip()
            
            if not ip_str or not subnet_str:
                raise ValueError("IP address and subnet mask/prefix are required")

            # IPv4
            if self.ui.comboBox_IPVersion.currentText() == "IPv4":
                if not subnet_str.startswith("/"):
                    try:
                        # dotted decimal mask (like 255.255.255.0)
                        if all(octet.isdigit() for octet in subnet_str.split('.')) and len(subnet_str.split('.')) == 4:
                            # Convert dotted decimal to prefix length by counting binary 1's
                            binary_str = ''.join([bin(int(octet))[2:].zfill(8) for octet in subnet_str.split('.')])
                            prefix_len = binary_str.count('1')
                            subnet_str = f"/{prefix_len}"
                        else:
                            # prefix directly
                            mask = ipaddress.IPv4Network(f"0.0.0.0/{subnet_str}").netmask
                            prefix_len = bin(int(mask)).count('1')
                            subnet_str = f"/{prefix_len}"
                    except Exception as e:
                        raise ValueError(f"Invalid subnet mask format: {str(e)}")
                network = ipaddress.IPv4Network(f"{ip_str}{subnet_str}", strict=False)
                self.displayIPv4Results(network)
            # IPv6
            else:
                if not subnet_str.startswith("/"):
                    raise ValueError("IPv6 prefix must be in CIDR notation (e.g. /64)")
                
                network = ipaddress.IPv6Network(f"{ip_str}{subnet_str}", strict=False)
                self.displayIPv6Results(network)

        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", str(e))

    def displayIPv4Results(self, network):
        ip = network.network_address
        results = [
            "Calculated results:",
            f"   Network Address: {network.network_address}",
            f"   First Usable IP: {network.network_address + 1}",
            f"   Last Usable IP: {network.broadcast_address - 1}",
            f"   Broadcast Address: {network.broadcast_address}",
            f"   Total Hosts: {network.num_addresses - 2}", 
            f"   Netmask: {network.netmask}",
            f"   Wildcard Mask: {network.hostmask}",
            f"   CIDR Notation: /{network.prefixlen}",
            f"   Binary Netmask: {'.'.join(bin(int(x))[2:].zfill(8) for x in str(network.netmask).split('.'))}",
            "",
            "Address Validation:",
            f"   {'Private' if ip.is_private else 'Public'} Address",
            f"   {'Multicast' if ip.is_multicast else 'Unicast'} Address",
            f"   {'Reserved' if ip.is_reserved else 'Not Reserved'}"
        ]
        self.ui.textEdit_Result.setPlainText('\n'.join(results))

    def displayIPv6Results(self, network):
        ip = network.network_address
        results = [
            "Calculated results:",
            f"   Network Address: {network.network_address}",
            f"   First Address: {network.network_address + 1}",
            f"   Last Address: {network.broadcast_address - 1}",
            f"   Broadcast Address: {network.broadcast_address}",
            f"   Total Addresses: {network.num_addresses - 2}",
            f"   Prefix Length: /{network.prefixlen}",
            f"   Compressed Address: {network.compressed}",
            f"   Expanded Address: {network.exploded}",
            "",
            "Address Validation:",
            f"   {'Private' if ip.is_private else 'Public'} Address",
            f"   {'Multicast' if ip.is_multicast else 'Unicast'} Address",
            f"   {'Link-Local' if ip.is_link_local else 'Not Link-Local'}",
            f"   {'Site-Local' if ip.is_site_local else 'Not Site-Local'}",
            f"   {'Reserved' if ip.is_reserved else 'Not Reserved'}"
        ]
        self.ui.textEdit_Result.setPlainText('\n'.join(results))