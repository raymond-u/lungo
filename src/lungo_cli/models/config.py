from dataclasses import dataclass


@dataclass
class AutheliaConfig:
    notifier_smtp_host: str
    notifier_smtp_port: int
    notifier_smtp_username: str
    notifier_smtp_sender: str
    notifier_smtp_subject: str
    session_domain: str
