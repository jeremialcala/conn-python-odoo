import odoorpc
import logging
import json
from logging import config
from classes import Settings
from utils import configure_logging, timeit


_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


@timeit
async def get_odoo_instance():
    return odoorpc.ODOO(_set.odoo_host, port=_set.odoo_port)


@timeit
async def get_odoo_entity(entity: str, odoo: odoorpc.ODOO = get_odoo_instance()):
    return odoo.env[entity]


@timeit
async def get_product_data_by_name(name: str) -> list:
    """
        Retrieve products by name from the odoo server returning a list of Products matching the indicated name,
        including an image in base64 format 'image_512'

    :param name: product name (ex. 'Coca-Cola')
    :return: list(products)
    """

    odoo = await get_odoo_instance()

    odoo.login(db=_set.odoo_db, login=_set.odoo_user, password=_set.odoo_pass)
    Product = await get_odoo_entity(entity=_set.entity_product, odoo=odoo)

    product_ids = Product.search([])
    products_names = Product.name_get(product_ids)

    product_ = [product for product in products_names if name.lower() in product[1].lower()]
    products = odoo.execute(_set.entity_product, 'read', [product_[0][0]], [])

    return [
        {
            "id": product["id"],
            "name": product["display_name"],
            "inventory": product["qty_available"],
            "list_price": product["list_price"],
            "created_date": product["write_date"],
            "image": product["image_512"]
        }
        for product in products
    ]

