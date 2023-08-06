import inject
from sqlalchemy_bundle import EntityManager
from sqlalchemy.orm.exc import NoResultFound
from werkzeug import exceptions
from jsonschema import validate
import json
import jsonschema

class loadentity(object):
    def __init__(self, **kwargs):
        self.entities = kwargs

    def __call__(self, f):
            def wrapped_f(*args, **kwargs):
                em = inject.instance(EntityManager)
                loaded_entities = {}
                with em.s as session:
                    inject_session = False
                    for key, entity in self.entities.items():
                        if isinstance(entity, dict):
                            model_type = entity["type"]
                            id_field_value = entity["id_field"]
                        else:
                            # La opcion de injectar em
                            if key == "inject_session":
                                inject_session = key
                                id_field_value = None
                            else:
                                model_type = entity
                                id_field_value = "id"

                        try:
                            miner = session.query(model_type).filter(model_type.id == kwargs[id_field_value]).one()
                            loaded_entities[key] = miner
                            del kwargs[id_field_value]

                        except NoResultFound:
                            raise exceptions.BadRequest('{entity_type} with id {id} does not exists'.format(
                                entity_type=model_type.__name__,
                                id=kwargs[id_field_value])
                            )

                    if inject_session:
                        return f(*args, session=session, **loaded_entities, **kwargs)
                    else:
                        return f(*args, **loaded_entities, **kwargs)
            return wrapped_f


class validate_json(object):
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            data = kwargs["request"].get_json()
            try:
                validate(data, self.schema)
            except jsonschema.exceptions.ValidationError as e:
                raise exceptions.BadRequest(e.message)
            return f(data)
        return wrapped_f


class populate(object):
    def __init__(self, model_type, schema, name):
        self.schema = schema
        #self.schema["additionalProperties"] = False
        self.model_type = model_type
        self.name = name

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            data = json.loads(kwargs["request"].data)
            try:
                validate(data, self.schema)
            except jsonschema.exceptions.ValidationError as e:
                raise exceptions.BadRequest(e.message)

            model_object = self.model_type()
            for key in self.schema["properties"]:
                if key in data:
                    setattr(model_object, key, data[key])

            kwargs[self.name] = model_object
            return f(*args, **kwargs)
        return wrapped_f