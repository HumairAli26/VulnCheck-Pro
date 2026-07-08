"""
SecureAudit
Port Threat Catalog

Author: Humair Ali

A finding of "port 445 is open" means nothing to most users on its own.
This module answers the two questions that actually matter: *what could
happen if I leave it open*, and *exactly how do I close it on my OS*.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.platform.platform_detector import Platform


@dataclass
class PortThreat:
    service: str
    threat: str
    close_steps: dict[Platform, list[str]] = field(default_factory=dict)

    def steps_for(self, platform: Platform) -> list[str]:
        return self.close_steps.get(
            platform,
            [
                "Identify the process/service bound to this port and stop it, "
                "or restrict access to it at the firewall.",
            ],
        )


PORT_THREATS: dict[int, PortThreat] = {
    21: PortThreat(
        service="FTP",
        threat=(
            "FTP transmits usernames, passwords, and file contents in plain text. "
            "Anyone on the same network segment can capture credentials with a packet "
            "sniffer, and many FTP servers are also vulnerable to anonymous login misconfiguration."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open 'Turn Windows features on or off' and uncheck 'FTP Server' under IIS if present.",
                "If a third-party FTP server is installed (FileZilla Server, etc.), stop and "
                "uninstall it, or switch it to SFTP.",
            ],
            Platform.LINUX: [
                "Check what's running it: sudo systemctl status vsftpd (or proftpd/pure-ftpd).",
                "Disable it: sudo systemctl disable --now vsftpd",
                "If you need file transfer, use SFTP over SSH instead (already encrypted).",
            ],
            Platform.MACOS: [
                "macOS does not ship FTP server software by default -- if this is open, a "
                "third-party server was installed. Quit it and remove it from Login Items.",
            ],
        },
    ),
    22: PortThreat(
        service="SSH",
        threat=(
            "SSH itself is encrypted and generally safe, but leaving it reachable from the "
            "open internet invites constant automated brute-force login attempts against "
            "weak passwords."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open Services, find 'OpenSSH SSH Server', and set it to Disabled if you don't need remote access.",
                "If you do need it, disable password auth in favor of SSH keys and restrict "
                "the allowed source IPs at the firewall.",
            ],
            Platform.LINUX: [
                "If you don't need remote SSH access: sudo systemctl disable --now ssh",
                "If you do need it: disable password login in /etc/ssh/sshd_config "
                "(PasswordAuthentication no) and use key-based auth instead.",
                "Restrict access further with: sudo ufw allow from <trusted-ip> to any port 22",
            ],
            Platform.MACOS: [
                "Open System Settings -> General -> Sharing and turn off 'Remote Login' if unused.",
                "If needed, restrict it to specific users/IPs in the same Sharing panel.",
            ],
        },
    ),
    23: PortThreat(
        service="Telnet",
        threat=(
            "Telnet sends everything -- including your login password -- as plain, "
            "unencrypted text. It is considered obsolete and dangerous by every modern "
            "security standard; anyone intercepting the traffic gets full credentials instantly."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open 'Turn Windows features on or off' and uncheck 'Telnet Server'.",
                "Restart if prompted.",
            ],
            Platform.LINUX: [
                "sudo systemctl disable --now telnetd (or inetd/xinetd if that's what runs it).",
                "Use SSH instead for any remote shell access.",
            ],
            Platform.MACOS: [
                "Telnet server isn't shipped by default on modern macOS -- check Login "
                "Items / launchd for a third-party service and remove it.",
            ],
        },
    ),
    25: PortThreat(
        service="SMTP",
        threat=(
            "An exposed, misconfigured mail server can be hijacked as an open relay, letting "
            "spammers send phishing/spam mail through your machine -- which can get your IP "
            "address blacklisted."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Check Services for a mail transfer agent (e.g. hMailServer) and stop it if unused.",
            ],
            Platform.LINUX: [
                "Check what's listening: sudo ss -tlnp | grep :25",
                "If it's Postfix/Sendmail and you don't run a mail server, disable it: "
                "sudo systemctl disable --now postfix",
                "If you do need it, ensure relay is restricted to authenticated/local users only.",
            ],
            Platform.MACOS: [
                "Check for a third-party mail server (Postfix isn't enabled by default on modern "
                "macOS) and disable it via launchctl if found.",
            ],
        },
    ),
    53: PortThreat(
        service="DNS",
        threat=(
            "A DNS server exposed to the internet can be abused for DNS amplification DDoS "
            "attacks against third parties, or, if misconfigured, leak your internal network "
            "layout via zone transfers."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open Server Manager -> Roles and remove the DNS Server role if this machine "
                "isn't meant to be a DNS server.",
            ],
            Platform.LINUX: [
                "Check what's running it: sudo ss -tlnp | grep :53",
                "If it's bind9/dnsmasq and unintended: sudo systemctl disable --now bind9",
                "If intentional, restrict recursion/zone transfers to trusted IPs only.",
            ],
            Platform.MACOS: [
                "DNS server isn't enabled by default -- check for third-party DNS software "
                "(e.g. dnsmasq via Homebrew) and disable it if unused.",
            ],
        },
    ),
    111: PortThreat(
        service="rpcbind",
        threat=(
            "rpcbind maps RPC services (often NFS) and has a long history of being used for "
            "reconnaissance and DDoS amplification. It rarely needs to be reachable from "
            "outside the local machine."
        ),
        close_steps={
            Platform.LINUX: [
                "sudo systemctl disable --now rpcbind",
                "If NFS is required, restrict it to trusted subnets in /etc/exports and your firewall.",
            ],
            Platform.WINDOWS: [
                "This service is Unix/Linux-specific; if it appears open on Windows it's likely "
                "a third-party NFS client/server -- uninstall it if unused.",
            ],
            Platform.MACOS: [
                "sudo launchctl disable system/com.apple.rpcbind (only if you don't use NFS shares).",
            ],
        },
    ),
    135: PortThreat(
        service="RPC (Windows)",
        threat=(
            "MS-RPC has been the entry point for several major worms (e.g. Blaster). Left "
            "reachable from untrusted networks, it significantly expands your remote attack surface."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Do not disable the RPC service itself (Windows depends on it) -- instead block "
                "it at the network boundary.",
                "Open Windows Defender Firewall with Advanced Security.",
                "Create an inbound rule blocking TCP 135 from any network except 'Domain'/'Private' as needed.",
            ],
            Platform.LINUX: [
                "Not applicable on stock Linux; if open, it's likely Samba/Wine -- restrict or "
                "disable the relevant service.",
            ],
            Platform.MACOS: [
                "Not applicable by default on macOS -- check for third-party software (e.g. Wine, "
                "Samba) exposing it.",
            ],
        },
    ),
    139: PortThreat(
        service="NetBIOS",
        threat=(
            "NetBIOS can leak hostnames, usernames, and shared-folder information to anyone "
            "on the network, and has historically been used to relay attacks against SMB."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open Network and Sharing Center -> Change adapter settings -> right-click your "
                "adapter -> Properties -> IPv4 -> Advanced -> WINS tab.",
                "Select 'Disable NetBIOS over TCP/IP'.",
            ],
            Platform.LINUX: [
                "If Samba's nmbd is running: sudo systemctl disable --now nmbd",
            ],
            Platform.MACOS: [
                "System Settings -> General -> Sharing -> turn off 'File Sharing' if SMB isn't needed.",
            ],
        },
    ),
    143: PortThreat(
        service="IMAP",
        threat=(
            "Plain (non-TLS) IMAP transmits your email password and message contents "
            "unencrypted, exposing them to anyone able to observe network traffic."
        ),
        close_steps={
            Platform.WINDOWS: [
                "If running a local mail server, enforce IMAPS (port 993) and disable plaintext IMAP.",
            ],
            Platform.LINUX: [
                "Edit your IMAP server config (Dovecot: /etc/dovecot/conf.d/10-ssl.conf) to require "
                "SSL and disable the plaintext listener, then: sudo systemctl restart dovecot",
            ],
            Platform.MACOS: [
                "Not shipped by default -- if a third-party mail server is running, enforce "
                "IMAPS and disable the plaintext port.",
            ],
        },
    ),
    445: PortThreat(
        service="SMB",
        threat=(
            "SMB is the exact protocol exploited by EternalBlue and used to spread WannaCry "
            "and NotPetya. An attacker on your network could read/write files on your shares "
            "or, on unpatched systems, execute code remotely with no authentication at all."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open Control Panel -> Programs -> Turn Windows features on or off.",
                "Uncheck 'SMB 1.0/CIFS File Sharing Support' (the legacy, most dangerous version).",
                "If you don't share files/printers on this network, also disable File and Printer "
                "Sharing under Network and Sharing Center -> Advanced sharing settings.",
            ],
            Platform.LINUX: [
                "sudo systemctl disable --now smbd nmbd",
                "If you need file sharing, restrict Samba to trusted subnets in smb.conf's "
                "'hosts allow' directive.",
            ],
            Platform.MACOS: [
                "System Settings -> General -> Sharing -> turn off 'File Sharing'.",
            ],
        },
    ),
    1433: PortThreat(
        service="Microsoft SQL Server",
        threat=(
            "Database ports exposed to the network are a top target for automated scanners "
            "running credential-stuffing and default-password attacks; a compromised database "
            "can mean full data theft or ransomware."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open SQL Server Configuration Manager -> SQL Server Network Configuration.",
                "Disable the TCP/IP protocol unless remote access is genuinely required.",
                "If required, restrict access via Windows Firewall to specific trusted source IPs only.",
            ],
            Platform.LINUX: [
                "Bind SQL Server to localhost only, or restrict the port via: "
                "sudo ufw deny 1433",
            ],
            Platform.MACOS: [
                "SQL Server isn't native to macOS -- if open, it's a container/VM; restrict its "
                "port mapping to localhost only.",
            ],
        },
    ),
    1521: PortThreat(
        service="Oracle Database",
        threat=(
            "Same category of risk as any exposed database port: automated scanners actively "
            "probe for default Oracle credentials (e.g. SYSTEM/MANAGER) to gain full data access."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Restrict the Oracle Listener to localhost, or firewall port 1521 to trusted IPs only.",
            ],
            Platform.LINUX: [
                "Edit listener.ora to bind to 127.0.0.1 if remote access isn't required, or "
                "restrict via: sudo ufw deny 1521",
            ],
            Platform.MACOS: [
                "Oracle isn't native to macOS -- if open, it's a container/VM; restrict its port "
                "mapping to localhost only.",
            ],
        },
    ),
    2049: PortThreat(
        service="NFS",
        threat=(
            "Misconfigured NFS exports can let any host on the network mount your shared "
            "folders with no authentication, exposing potentially sensitive files."
        ),
        close_steps={
            Platform.LINUX: [
                "Review /etc/exports and restrict each share to specific trusted subnets.",
                "If unused: sudo systemctl disable --now nfs-server",
            ],
            Platform.WINDOWS: [
                "Not applicable by default -- if NFS is enabled via 'Services for NFS', remove "
                "the feature if unused.",
            ],
            Platform.MACOS: [
                "System Settings -> Sharing -> ensure 'File Sharing' NFS exports are disabled if unused.",
            ],
        },
    ),
    3306: PortThreat(
        service="MySQL",
        threat=(
            "An exposed MySQL port is routinely targeted by automated bots trying default/weak "
            "root credentials; a breach here can mean full read/write access to every database "
            "on the server."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open my.ini and set bind-address=127.0.0.1 unless remote DB access is required.",
                "Restart the MySQL service afterward.",
            ],
            Platform.LINUX: [
                "Edit /etc/mysql/mysql.conf.d/mysqld.cnf, set bind-address = 127.0.0.1, then: "
                "sudo systemctl restart mysql",
                "If remote access is required, restrict it via firewall to specific trusted IPs.",
            ],
            Platform.MACOS: [
                "Edit my.cnf (Homebrew: /opt/homebrew/etc/my.cnf) and set bind-address = 127.0.0.1, "
                "then: brew services restart mysql",
            ],
        },
    ),
    3389: PortThreat(
        service="RDP",
        threat=(
            "RDP is one of the most commonly targeted services for ransomware deployment -- "
            "attackers scan the internet constantly for open 3389 and attempt credential "
            "stuffing or exploit known RDP vulnerabilities to gain full desktop control."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Open Settings -> System -> Remote Desktop and turn it Off if you don't use it.",
                "If you do need it, enable Network Level Authentication and restrict access via "
                "'Windows Defender Firewall with Advanced Security' to specific trusted IPs, or "
                "put it behind a VPN instead of exposing it directly.",
            ],
            Platform.LINUX: [
                "If xrdp is installed and unused: sudo systemctl disable --now xrdp",
            ],
            Platform.MACOS: [
                "RDP isn't native -- if open, a third-party RDP server is running; quit/remove it "
                "if unused.",
            ],
        },
    ),
    5432: PortThreat(
        service="PostgreSQL",
        threat=(
            "Same risk class as other exposed databases: automated scanners probe for weak "
            "'postgres' credentials, and a compromise here exposes every table on the server."
        ),
        close_steps={
            Platform.LINUX: [
                "Edit postgresql.conf, set listen_addresses = 'localhost' unless remote access "
                "is required, then: sudo systemctl restart postgresql",
                "Tighten pg_hba.conf to only allow trusted hosts/IPs.",
            ],
            Platform.WINDOWS: [
                "Edit postgresql.conf the same way via pgAdmin or a text editor, then restart the "
                "PostgreSQL service from Services.",
            ],
            Platform.MACOS: [
                "Edit postgresql.conf (Homebrew: /opt/homebrew/var/postgresql@<version>/postgresql.conf) "
                "and set listen_addresses = 'localhost', then: brew services restart postgresql",
            ],
        },
    ),
    5900: PortThreat(
        service="VNC",
        threat=(
            "VNC often ships with weak or no authentication by default, and older versions send "
            "screen data unencrypted -- an attacker who connects gets full remote control of your "
            "desktop, exactly as if they were sitting at it."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Uninstall or stop your VNC server (TightVNC, RealVNC, etc.) via Services if unused.",
                "If needed, set a strong password and tunnel it over SSH/VPN rather than exposing it directly.",
            ],
            Platform.LINUX: [
                "sudo systemctl disable --now vncserver@:1 (adjust unit name to match your setup).",
            ],
            Platform.MACOS: [
                "System Settings -> General -> Sharing -> turn off 'Screen Sharing' if unused, or "
                "set a strong password and restrict access to specific users.",
            ],
        },
    ),
    6379: PortThreat(
        service="Redis",
        threat=(
            "Redis historically shipped with no authentication at all by default. Exposed Redis "
            "instances have been mass-exploited to write malicious cron jobs/SSH keys onto the "
            "host, leading to full server takeover -- not just data theft."
        ),
        close_steps={
            Platform.LINUX: [
                "Edit /etc/redis/redis.conf: set 'bind 127.0.0.1' and 'requirepass <a-strong-password>'.",
                "Restart: sudo systemctl restart redis",
            ],
            Platform.WINDOWS: [
                "Edit redis.windows.conf the same way (bind + requirepass), then restart the Redis service.",
            ],
            Platform.MACOS: [
                "Edit redis.conf (Homebrew: /opt/homebrew/etc/redis.conf) the same way, then: "
                "brew services restart redis",
            ],
        },
    ),
    8080: PortThreat(
        service="HTTP-Alt",
        threat=(
            "Commonly used for admin panels, dev servers, and proxy/monitoring tools. Left "
            "exposed, it can leak an unauthenticated management interface directly to the network."
        ),
        close_steps={
            Platform.WINDOWS: [
                "Identify the process bound to 8080 via Resource Monitor and stop it if unintended, "
                "or restrict it via Windows Firewall if it must run.",
            ],
            Platform.LINUX: [
                "Identify it: sudo lsof -i :8080",
                "Stop the associated service, or restrict it with: sudo ufw deny 8080",
            ],
            Platform.MACOS: [
                "Identify it: sudo lsof -i :8080",
                "Quit the associated app, or restrict access at the firewall.",
            ],
        },
    ),
    9200: PortThreat(
        service="Elasticsearch",
        threat=(
            "Elasticsearch has no authentication enabled by default in many setups. Exposed "
            "instances have repeatedly been mass-scanned and wiped/ransomed by automated bots "
            "that simply query the open REST API -- no exploit required, just a browser."
        ),
        close_steps={
            Platform.LINUX: [
                "Bind it to localhost in elasticsearch.yml (network.host: 127.0.0.1) unless "
                "cluster access is required, then: sudo systemctl restart elasticsearch",
                "Enable Elasticsearch security features (authentication) if remote access is genuinely needed.",
            ],
            Platform.WINDOWS: [
                "Same fix via elasticsearch.yml, then restart the Elasticsearch service.",
            ],
            Platform.MACOS: [
                "Same fix via elasticsearch.yml, then: brew services restart elasticsearch-full",
            ],
        },
    ),
    11211: PortThreat(
        service="Memcached",
        threat=(
            "Exposed Memcached servers have been widely abused for some of the largest DDoS "
            "amplification attacks ever recorded (amplification factors over 50,000x) -- it "
            "should essentially never be reachable from outside localhost."
        ),
        close_steps={
            Platform.LINUX: [
                "Edit /etc/memcached.conf, set '-l 127.0.0.1' to bind to localhost only, then: "
                "sudo systemctl restart memcached",
            ],
            Platform.WINDOWS: [
                "Restrict the Memcached service to localhost via its startup parameters, or stop "
                "it if unused.",
            ],
            Platform.MACOS: [
                "Edit the launch config to bind to 127.0.0.1 only, then: "
                "brew services restart memcached",
            ],
        },
    ),
    27017: PortThreat(
        service="MongoDB",
        threat=(
            "Older MongoDB versions shipped with no authentication by default. Thousands of "
            "exposed instances have been found scraped, deleted, or held for ransom by bots "
            "that simply connect to the open port and dump every collection."
        ),
        close_steps={
            Platform.LINUX: [
                "Edit /etc/mongod.conf: set 'bindIp: 127.0.0.1' and enable 'security.authorization: enabled'.",
                "Restart: sudo systemctl restart mongod",
            ],
            Platform.WINDOWS: [
                "Same fix via mongod.cfg, then restart the MongoDB service.",
            ],
            Platform.MACOS: [
                "Same fix via mongod.conf, then: brew services restart mongodb-community",
            ],
        },
    ),
}
