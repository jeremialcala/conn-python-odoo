from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_id: str
    national_id_url: str

    db_name: str
    db_host: str
    db_username: str
    db_password: str

    sender_email: str
    sender_password: str

    gmail_server_url: str
    gmail_server_port: int

    expiration_time: int
    activation_code_length: int
    password_length: int

    qms_server: str
    qms_user: str
    qms_password: str
    amqp_exchange: str
    amqp_routing_key: str

    key_size: int
    private_key_filename: str
    public_key_filename: str

    environment: str
    version: str

    verify_token: str

    facebook_graph_url: str
    facebook_messages_url: str
    facebook_whatsapp_message: str
    facebook_graph_version: str

    log_format: str

    max_memory: str
    queue_name: str

    llm_model_name: str

    api_url: str

    odoo_host: str
    odoo_port: str
    odoo_db: str
    odoo_user: str
    odoo_pass: str

    entity_partner: str
    entity_product: str
    entity_order: str
    entity_user: str

    model_config = SettingsConfigDict(env_file="config.env")
