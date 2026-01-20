"""SDK to Json."""
import collections
import inspect
import json
from inspect import signature

from msa_sdk import util
from msa_sdk.conf_profile import ConfProfile
from msa_sdk.customer import Customer
from msa_sdk.device import Device
from msa_sdk.geolocation import Geolocation
from msa_sdk.lookup import Lookup
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.pops import Pops
from msa_sdk.repository import Repository
from msa_sdk.variables import Variables
# Explicit imports for the new transformer structure
from transformers.base_transformer import BaseTransformer
from transformers.action_mapper import ActionMapper
from transformers.type_mapper import TypeMapper
from transformers.pattern_normalizer import PatternNormalizer
from transformers.metadata_enricher import MetadataEnricher
from transformers.category_mapper import CategoryMapper
from transformers.pipelines import apply_transformers

conf_profile = ConfProfile()
customer = Customer()
device = Device()
geolocation = Geolocation(1)
lookup = Lookup()
orchestration = Orchestration(1)
order = Order(1)
pops = Pops()
repository = Repository()
variable = Variables()

base_transformer = BaseTransformer()
action_mapper = ActionMapper()
type_mapper = TypeMapper()
pattern_normalizer = PatternNormalizer()
metadata_enricher = MetadataEnricher()
category_mapper = CategoryMapper()
pipelines = apply_transformers()

output_doc = collections.defaultdict(dict)  # type: dict


def get_members(cls_name, obj):
    """Extract members."""
    output_doc[cls_name] = {"methods": list()}
    for i in inspect.getmembers(obj, predicate=inspect.ismethod):
        if i[0].startswith('__init__'):
            output_doc[cls_name]["methods"].append(
                {
                    i[0]: {
                        "description": inspect.getdoc(i[1]),
                        "parameters": str(signature(i[1]))
                    }
                }
            )
        if not i[0].startswith('_'):
            output_doc[cls_name]["methods"].append(
                {
                    i[0]: {
                        "description": inspect.getdoc(i[1]),
                        "parameters": str(signature(i[1]))
                    }
                }
            )


def get_members_function():
    """Exctract members of a function."""
    output_doc["util"] = {"methods": list()}
    for func_name, funcobj in inspect.getmembers(util,
                                                 predicate=inspect.isfunction):
        output_doc["util"]["methods"].append(
            {
                func_name: {
                    "description": inspect.getdoc(funcobj),
                    "parameters": str(signature(funcobj))
                }
            }
        )


get_members('ConfProfile', conf_profile)
get_members('Customer', customer)
get_members('Device', device)
get_members('Geolocation', geolocation)
get_members('Lookup', lookup)
get_members('Orchestration', orchestration)
get_members('Order', order)
get_members('Pops', pops)
get_members('Repository', repository)
get_members('Variables', variable)

get_members('BaseTransformer', base_transformer)
get_members('ActionMapper', action_mapper)
get_members('TypeMapper', type_mapper)
get_members('PatternNormalizer', pattern_normalizer)
get_members('MetadataEnricher', metadata_enricher)
get_members('CategoryMapper', category_mapper)
get_members('apply_transformers', pipelines)

get_members_function()

print(json.dumps(output_doc))
