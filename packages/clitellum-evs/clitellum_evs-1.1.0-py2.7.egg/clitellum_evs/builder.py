"""
Entidades Builder
"""
import sys
import pymongo
from entities import AggregateRoot
from bson import ObjectId
from rejection.engines import NoActionRejectionEngine, StopOnErrorRejectionEngine

class AggregateRootBuilder(object):
    """
    Aggregate Root Builder for finite state machines.
    """
    def __init__(self, database, collection_name, state_machine_class):
        self._database = database
        self._collection_name = collection_name
        self._state_machine_class = state_machine_class
        self._id = None
        self._state = None
        self._query = None
        self._events = []
        self._rejection_engine = NoActionRejectionEngine()

    @classmethod
    def create(cls, database, collection_name, state_machine_class):
        """

        :param database: base de datos.
        :param collection_name: nombre de la coleccion donde reflejar los eventos.
        :param state_machine_class: nombre de la clase tipo de la maquina de estados.
        :return: src.builder.AggregateRootBuilder
        """
        return AggregateRootBuilder(database, collection_name, state_machine_class)

    def set_entity(self, obj_id):
        """
        Setea el id de la entidad.
        :param obj_id: identificador de la entidad
        """
        self._id = obj_id
        return self
    
    def set_entity_from_query(self, query):
        """
        Setea el id de la entidad.
        :param id: identificador de la entidad
        """
        self._query = query
        return self

    def set_initial_state(self, state):
        """
        Setea el estado inicial
        :param state: estado
        """
        self._state = state
        return self

    def set_stop_on_rejection(self):
        '''
        Establece el motor de rechazo StopOnErrorRejection, no aplica mas eventos si uno 
        da error
        '''
        self._rejection_engine = StopOnErrorRejectionEngine()
        return self

    def add_event(self, event):
        """
        Anade un evento con version.
        :param event: evento
        """
        self._events.append(event)
        return self

    def build(self):
        """
        Hace el build de un Aggregate Root
        :return:
        """
        self._get_id()

        for event in self._events:
            self._insert_event(event)

        entity = self._get_collection_entity().find_one({"_id" : self._id})
        events = self._get_collection_events().find({'entity_id': self._id}) \
            .sort("version", pymongo.ASCENDING)
        machine = self._state_machine_class()

        if self._state is None:
            self._state = machine.get_initial_state()

        if entity is None:
            root = AggregateRoot(self._id, {}, machine, self._state)
        else:
            root = AggregateRoot(self._id, entity, machine, entity['state'])

        root.set_rejection_engine(self._rejection_engine)

        root_events = []
        for event in events:
            event_class = getattr(sys.modules[event['_t']['module']], event['_t']['name'])
            ev = event_class(event['_id'], event['event'])
            ev.set_version = event['version']
            root_events.append(ev)
        
        root.apply_events(root_events)
        return root

    def _get_id(self):
        if not self._id is None:
            return
        if self._query is None:
            self._id = ObjectId()
        ret = self._get_collection_entity().find_one(self._query)
        if ret is None:
            self._id = ObjectId()
        else:
            self._id = ret['_id']


    def _insert_event(self, event):
        """
        Guarda en bbdd el evento con su version y entidad definidas.
        :param event: evento
        """
        event_db = {}
        if not event.get_id() is None:
            event_db['_id'] = event.get_id()
        event_db['event'] = event.to_json()
        event_db['entity_id'] = self._id
        event_db['version'] = event.get_version()
        event_db['_t'] = {"module": event.__module__,
                          "name": event.__class__.__name__}

        self._get_collection_events().insert(event_db)


    def _get_collection_entity(self):
        return self._database.get_collection(self._collection_name + '_entity')

    def _get_collection_events(self):
        return self._database.get_collection(self._collection_name + '_events')


class SnapshotBuilder(object):
    """
    Creador de imagenes de una entidad en concreto.
    """
    def __init__(self, database, collection_name, state_machine_class):
        self._database = database
        self._collection_name = collection_name
        self._state_machine_class = state_machine_class
        self._root = None
        self._remove_rejected_events = False

    @classmethod
    def create(cls, database, collection_name, state_machine_class):
        """
        Crea un snapshot builder a partir de los parametros.
        :param database: base de datos donde guardar el snapshot.
        :param collection_name: nombre de la coleccion del la base de datos.
        :param state_machine_class: nombre de la clase tipo de la maquina de estados.
        :return: SnapshotBuilder
        """
        return SnapshotBuilder(database, collection_name, state_machine_class)

    def set_root(self, aggregate_root):
        """
        Setea un aggregate root
        :param aggregate_root: AggregateRoot
        :type aggregate_root: src.entities.AggregateRoot
        :return:
        """
        self._root = aggregate_root
        return self

    def set_remove_rejected_events(self, remove):
        '''
        Estable si al crear el snapshot hay que eliminar los eventos que han sido rechazados
        por defecto no se eliminan de la lista de eventos.
        '''
        self._remove_rejected_events = remove
        return self

    def build(self):
        """
        Build
        """
        for event in self._root.get_applied_events():
            self._save_applied_event(event)

        if self._remove_rejected_events:
            for event in self._root.get_rejection_engine().get_rejected_events():
                self._save_rejected_event(event)

        entity_db = {}
        entity_db['snapshot'] = self._root.get_entity()
        entity_db['state'] = self._root.get_state()
        entity_db['version'] = self._root.get_version()
        self._get_collection_entity().update({'_id' : self._root.get_id()}, \
                                             entity_db, upsert=True)

    def _save_applied_event(self, event):
        event_db = {}
        event_db['event'] = event.to_json()
        event_db['entity_id'] = self._root.get_id()
        event_db['version'] = event.get_version()
        event_db['_id'] = event.get_id()
        event_db['_t'] = {"module": event.__module__,
                          "name": event.__class__.__name__}
        self._get_collection_applied_events().insert(event_db)
        self._get_collection_events().remove({'_id': event.get_id()})

    def _save_rejected_event(self, event):
        event_db = {}
        event_db['event'] = event.to_json()
        event_db['entity_id'] = self._root.get_id()
        event_db['version'] = event.get_version()
        event_db['_id'] = event.get_id()
        event_db['_t'] = {"module": event.__module__,
                          "name": event.__class__.__name__}
        self._get_collection_rejected_events().insert(event_db)
        self._get_collection_events().remove({'_id': event.get_id()})
        
    def _get_collection_entity(self):
        return self._database.get_collection(self._collection_name + '_entity')

    def _get_collection_applied_events(self):
        return self._database.get_collection(self._collection_name + '_applied')

    def _get_collection_rejected_events(self):
        return self._database.get_collection(self._collection_name + '_rejected')

    def _get_collection_events(self):
        return self._database.get_collection(self._collection_name + '_events')
