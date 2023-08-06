# -*- coding: utf-8 -*-

"""
For interactions with the NiFi Canvas
STATUS: Work in Progress to determine pythonic datamodel
"""

from __future__ import absolute_import
from swagger_client import ProcessGroupFlowEntity, FlowApi
from swagger_client import ProcessgroupsApi, ProcessGroupEntity
from swagger_client import ProcessGroupDTO, PositionDTO
from swagger_client.rest import ApiException

__all__ = [
    "get_root_pg_id", "recurse_flow", "get_flow", "get_process_group_status",
    "get_process_group", "list_all_process_groups", "delete_process_group",
    "schedule_process_group", "create_process_group", "list_all_processors",
    "list_all_processor_types", "get_processor_type"
]


def get_root_pg_id():
    """Simple Example function for wrapper demonstration"""
    con = FlowApi()
    pg_root = con.get_process_group_status('root')
    return pg_root.process_group_status.id


def recurse_flow(pg_id='root'):
    """
    Returns information about a Process Group and all its Child Flows
    :param pg_id: id of a Process Group to use as the root for recursion
    , defaults to root if none supplied
    :returns ProcessGroupFlowEntity: Nested Process Group information
    """
    def _walk_flow(node):
        """This recursively extends the ProcessGroupEntity to contain the
        ProcessGroupFlowEntity of each of it's child process groups.
        So you can have the entire canvas in a single object
        """
        if isinstance(node, ProcessGroupFlowEntity):
            for pg in node.process_group_flow.flow.process_groups:
                pg.__setattr__(
                    'nipyapi_extended',
                    recurse_flow(pg.id)
                )
            return node
    return _walk_flow(get_flow(pg_id))


def get_flow(pg_id='root'):
    """
    Returns information about a Process Group and flow
    This surfaces the native implementation, for the recursed implementation
    see 'recurse_flow'
    :param pg_id: id of the Process Group to retrieve, defaults to the root
    process group if not set
    :return ProcessGroupFlowEntity: the Process Group object
    """
    try:
        return FlowApi().get_flow(pg_id)
    except ApiException as err:
        raise ValueError(err.body)


def get_process_group_status(pg_id='root', detail='names'):
    """
    Returns information about a Process Group
    :param pg_id: NiFi ID of the Process Groupt to retrieve
    :param detail: Level of detail to respond with
    :return:
    """
    valid_details = ['names', 'all']
    if detail not in valid_details:
        raise ValueError(
            'detail requested ({0}) not in valid list ({1})'
            .format(detail, valid_details)
        )
    raw = ProcessgroupsApi().get_process_group(id=pg_id)
    if detail == 'names':
        out = {
            raw.component.name: raw.component.id
        }
        return out
    elif detail == 'all':
        return raw


def get_process_group(identifier, identifier_type='name'):
    """
    Returns a process group, if it exists. Returns a list for duplicates
    :param identifier: String of the name or id of the process group
    :param identifier_type: 'name' or 'id'
    :return: ProcessGroupEntity if unique, None if not found, List if duplicate
    """
    valid_id_types = ['name', 'id']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "invalid identifier_type. ({0}) not in ({1})".format(
                identifier_type, valid_id_types
            )
        )
    all_pgs = list_all_process_groups()
    if identifier_type == 'name':
        out = [
            li for li in all_pgs
            if li.status.name == identifier
        ]
    elif identifier_type == 'id':
        out = [
            li for li in all_pgs
            if li.id == identifier
        ]
    else:
        out = []
    if not out:
        return None
    elif len(out) > 1:
        return out
    return out[0]


def list_all_process_groups():
    """
    Returns a flattened list of all Process Groups.
    :return list: list of ProcessGroupEntity objects
    """
    def flatten(parent_pg):
        """
        Recursively flattens the native datatypes into a generic list.
        Note that the root is a special case as it has no parent
        :param parent_pg: ProcessGroupEntity to flatten
        :return yield: generator for all ProcessGroupEntities, eventually
        """
        for child_pg in parent_pg.process_group_flow.flow.process_groups:
            for sub in flatten(child_pg.nipyapi_extended):
                yield sub
            yield child_pg
    root_flow = recurse_flow('root')
    out = list(flatten(root_flow))
    # This duplicates the nipyapi_extended structure to the root case
    root_entity = ProcessgroupsApi().get_process_group('root')
    root_entity.__setattr__('nipyapi_extended', root_flow)
    out.append(root_entity)
    return out


def list_all_processors():
    """
    Returns a flat list of all Processors anywhere on the canvas
    :return: list of ProcessorEntity's
    """
    def flattener():
        """
        Memory efficient flattener, sort of.
        :return: yield's a ProcessEntity
        """
        for pg in list_all_process_groups():
            for proc in pg.nipyapi_extended.process_group_flow.flow.processors:
                yield proc
    return list(flattener())


def delete_process_group(process_group_id, revision):
    """
    deletes a specific process group
    :param process_group_id: id of the process group to be removed
    :param revision: revision object from the parent PG to the removal target
    :return ProcessGroupEntity: the updated entity object for the deleted PG
    """
    return ProcessgroupsApi().remove_process_group(
        id=process_group_id,
        version=revision.version,
        client_id=revision.client_id
    )


def schedule_process_group(process_group_id, target_state):
    """
    Start or stop a Process Group and all children
    :param process_group_id: ID of the Process Group to Target
    :param target_state: Either 'RUNNING' or 'STOPPED'
    :return: dict of resulting process group state
    """
    # ideally this should be pulled from the client definition
    valid_states = ['STOPPED', 'RUNNING']
    if target_state not in valid_states:
        raise ValueError(
            "supplied state {0} not in valid states ({1})".format(
                target_state, valid_states
            )
        )
    out = FlowApi().schedule_components(
        id=process_group_id,
        body={
            'id': process_group_id,
            'state': target_state
        }
    )
    return out


def create_process_group(parent_pg, new_pg_name, location):
    """
    Creates a new PG with a given name under the provided parent PG
    :param parent_pg: ProcessGroupEntity object of the parent PG
    :param new_pg_name: String to name the new PG
    :param location: Tuple of (x,y) coordinates to place the new PG
    :return: ProcessGroupEntity of the new PG
    """
    try:
        return ProcessgroupsApi().create_process_group(
            id=parent_pg.id,
            body=ProcessGroupEntity(
                revision=parent_pg.revision,
                component=ProcessGroupDTO(
                    name=new_pg_name,
                    position=PositionDTO(
                        x=float(location[0]),
                        y=float(location[1])
                    )
                )
            )
        )
    except ApiException as e:
        raise e


def list_all_processor_types():
    """
    Produces the list of all available processor types in the NiFi instance
    :return ProcessorTypesEntity: Native Datatype containing list
    """
    try:
        return FlowApi().get_processor_types()
    except ApiException as e:
        raise e


def get_processor_type(identifier, identifier_type='name'):
    """

    :param identifier: String to search for
    :param identifier_type: Processor descriptor to search: bundle, name or tag
    :return: DocumentedTypeDTO if unique, None if not found, List if duplicate
    """
    valid_id_types = ['bundle', 'name', 'tag']
    if identifier_type not in valid_id_types:
        raise ValueError(
            "identifier_type not in valid list ({0})".format(
                identifier_type
            )
        )
    out = []
    all_p = list_all_processor_types().processor_types
    if identifier_type == 'name':
        out = [
            i for i in all_p if
            identifier in i.type
        ]
    if identifier_type == 'bundle':
        out = [
            i for i in all_p if
            identifier in i.bundle.artifact
        ]
    if identifier_type == 'tag':
        out = [
            i for i in all_p if
            identifier in str(i.tags)
        ]
    if not out:
        return None
    elif len(out) > 1:
        return out
    return out[0]
