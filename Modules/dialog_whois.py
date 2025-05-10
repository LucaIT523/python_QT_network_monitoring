from PySide6.QtWidgets import QDialog
class WhoisDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        from Forms.ui_dialog_whois import Ui_DialogWhois
        self.ui = Ui_DialogWhois()
        self.ui.setupUi(self)              

        self.init_data()
        
        return
    def init_data(self):
        self.ui.lineEdit_ip_address.clear()
        self.ui.textEdit_Result.clear()

        self.ui.pushButton_Run.clicked.connect(self.onRun)
        return
    def validateIPAddress(self, ip_address: str) -> bool:
        if ip_address is None:
            return False
        ip_address = ip_address.strip()
        if ip_address is None:
            return False
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        import re
        if re.match(ip_pattern, ip_address):
            # Check if each octet is between 0 and 255
            octets = ip_address.split('.')
            return all(0 <= int(octet) <= 255 for octet in octets)
        # Check if the input is a valid domain name
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](\.[a-zA-Z]{2,})+$'
        if re.match(domain_pattern, ip_address):
            return True
        if ip_address == "localhost":
            return True
        return False    

    def query_whois(self, ip_address):
        print("query_whois")
        #try:
        import ipaddress
        ip = ipaddress.ip_address(ip_address)
        print("query_whois3")
        # Check if it's a private IP address
        if ip.is_private:
            print("is_private")
            # Determine the appropriate network for the private IP
            if ip.version == 4:  # IPv4
                # Determine which private network range this IP belongs to
                if ip in ipaddress.IPv4Network('10.0.0.0/8'):
                    network = ipaddress.IPv4Network('10.0.0.0/8')
                elif ip in ipaddress.IPv4Network('172.16.0.0/12'):
                    network = ipaddress.IPv4Network('172.16.0.0/12')
                elif ip in ipaddress.IPv4Network('192.168.0.0/16'):
                    network = ipaddress.IPv4Network('192.168.0.0/16')
                else:
                    # For other private IPs, use a /24 subnet
                    network = ipaddress.IPv4Network(f'{ip}/24', strict=False)
            else:  # IPv6
                # For IPv6, use a /64 subnet for private addresses
                network = ipaddress.IPv6Network(f'{ip}/64', strict=False)
                
            # Format similar to who.is for private IPs
            formatted_result = [
                f"NetRange:       {network.network_address} - {network.broadcast_address}",
                f"CIDR:           {network}",
                f"NetName:        PRIVATE-ADDRESS-{ip.version}-RFC1918",
                f"NetHandle:      NET-{network.network_address}-1",
                f"Parent:         ",
                f"NetType:        IANA RESERVED",
                f"OriginAS:       ",
                f"Organization:    Internet Assigned Numbers Authority",
                f"RegDate:        ",
                f"Updated:        ",
                f"Comment:        These addresses are reserved for private networks.",
                f"Comment:        See RFC 1918 for more information.",
                f"Ref:            https://www.iana.org/assignments/iana-ipv4-special-registry/",
            ]
            self.ui.textEdit_Result.setPlainText('\n'.join(line for line in formatted_result if line is not None))
            return
            
        # For public IPs, use the ipwhois library
        from ipwhois import IPWhois
        ip_info = IPWhois(ip_address)
        result = ip_info.lookup_rdap()
        print(result)
        if result:
            formatted_result = []
            
            # Network Information
            if 'network' in result:
                net = result['network']
                formatted_result.extend([
                    f"NetRange:       {net.get('start_address')} - {net.get('end_address')}",
                    f"CIDR:           {net.get('cidr')}",
                    f"NetName:        {net.get('name')}",
                    f"NetHandle:      {net.get('handle')}",
                    f"Parent:         {net.get('parent_handle')}",
                    f"NetType:        {net.get('type')}",
                    f"OriginAS:       AS{result.get('asn')}",
                    f"Organization:   {result.get('objects', {}).get('CLOUD14', {}).get('contact', {}).get('name')}",
                    f"RegDate:        {next((event['timestamp'].split('T')[0] for event in net.get('events', []) if event['action'] == 'registration'), '')}",
                    f"Updated:        {next((event['timestamp'].split('T')[0] for event in net.get('events', []) if event['action'] == 'last changed'), '')}"
                ])
                
                # Add comments if available
                if 'remarks' in net and isinstance(net['remarks'], list):
                    for remark in net['remarks']:
                        if 'description' in remark:
                            for desc in remark['description'].split('\n'):
                                formatted_result.append(f"Comment:        {desc}")
                # Add Ref if available
                if 'links' in net and isinstance(net['links'], list):
                    formatted_result.append(f"Ref:        {net['links'][0]}")
            
            formatted_result.append('')  # Empty line separator
            
            # Organization Information
            for entity_handle, entity in result.get('objects', {}).items():
                if 'registrant' in entity.get('roles', []):
                    contact = entity.get('contact', {})
                    formatted_result.extend([
                        f"OrgName:        {contact.get('name', '')}",
                        f"OrgId:          {entity_handle}"
                    ])
                    
                    # Address information
                    if 'address' in contact and contact['address'] is not None and len(contact['address']) > 0:
                        address_value = contact['address'][0].get('value', '') if isinstance(contact['address'][0], dict) else ''
                        address_parts = address_value.split('\n')
                        if len(address_parts) >= 4:
                            formatted_result.extend([
                                f"Address:        {address_parts[0]}",
                                f"City:           {address_parts[1]}",
                                f"StateProv:      {address_parts[2]}",
                                f"PostalCode:     {address_parts[3]}",
                                f"Country:        {address_parts[4] if len(address_parts) > 4 else 'US'}"
                            ])
                    # Add events if available
                    if 'events' in entity and isinstance(entity['events'], list):
                        formatted_result.extend([
                            f"RegDate:        {next((event['timestamp'].split('T')[0] for event in entity.get('events', []) if event['action'] == 'registration'), '')}",
                            f"Updated:        {next((event['timestamp'].split('T')[0] for event in entity.get('events', []) if event['action'] == 'last changed'), '')}"
                        ])
                    # Add comments if available
                    if 'remarks' in entity and isinstance(entity['remarks'], list):
                        for remark in entity['remarks']:
                            if 'description' in remark:
                                for desc in remark['description'].split('\n'):
                                    formatted_result.append(f"Comment:        {desc}")
                    # Add Ref if available
                    if 'links' in entity and isinstance(entity['links'], list):
                        formatted_result.append(f"Ref:        {entity['links'][0]}")
                    
                    formatted_result.append('') 
            
            # Contact Information for different roles
            for entity_handle, entity in result.get('objects', {}).items():
                contact = entity.get('contact', {})
                roles = entity.get('roles', [])
                
                for role in roles:
                    if role in ['abuse', 'technical', 'noc']:
                        role_prefix = 'Org' if role != 'noc' else 'R'
                        formatted_result.extend([
                            f"{role_prefix}{role.capitalize()}Handle: {entity_handle}",
                            f"{role_prefix}{role.capitalize()}Name:   {contact.get('name', '')}",
                            f"{role_prefix}{role.capitalize()}Phone:  {contact.get('phone', [{}])[0].get('value', '') if contact.get('phone') else ''}",
                            f"{role_prefix}{role.capitalize()}Email:  {contact.get('email', [{}])[0].get('value', '') if contact.get('email') else ''}",
                            f"{role_prefix}{role.capitalize()}Ref:    {entity.get('links', [''])[0] if entity.get('links') else ''}",
                            ""
                        ])
            
            self.ui.textEdit_Result.setPlainText('\n'.join(line for line in formatted_result if line is not None))
        else:
            self.ui.textEdit_Result.setPlainText("No whois information found.")
        # except Exception as e:
        #     from PySide6.QtWidgets import QMessageBox
        #     QMessageBox.warning(self, "Error", f"Failed to query whois information: {str(e)}")

        
    def onRun(self):
        ip_address = self.ui.lineEdit_ip_address.text()

        if self.validateIPAddress(ip_address):    
            self.ui.pushButton_Run.setEnabled(False)        
            self.ui.textEdit_Result.clear()
            self.query_whois(ip_address)
            self.ui.pushButton_Run.setEnabled(True)
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Input Error", "Invalid IP address.")
        return
    def closeEvent(self, event):
        event.accept()
