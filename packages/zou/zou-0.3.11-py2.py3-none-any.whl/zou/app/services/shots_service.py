from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError, StatementError

from zou.app.utils import events, fields

from zou.app.models.entity import Entity
from zou.app.models.entity_type import EntityType
from zou.app.models.project import Project
from zou.app.models.task import Task
from zou.app.models.task_status import TaskStatus
from zou.app.models.task_type import TaskType

from zou.app.services import projects_service
from zou.app.services.exception import (
    EpisodeNotFoundException,
    SequenceNotFoundException,
    SceneNotFoundException,
    ShotNotFoundException
)


def get_sequence_from_shot(shot):
    try:
        sequence = Entity.get(shot["parent_id"])
    except:
        raise SequenceNotFoundException('Wrong parent_id for given shot.')
    return sequence.serialize(obj_type="Sequence")


def get_episode_from_sequence(sequence):
    try:
        episode = Entity.get(sequence["parent_id"])
    except:
        raise EpisodeNotFoundException('Wrong parent_id for given sequence.')
    return episode.serialize(obj_type="Episode")


def get_entity_type(name):
    entity_type = EntityType.get_by(name=name)
    if entity_type is None:
        entity_type = EntityType.create(name=name)
    return entity_type.serialize()


def get_episode_type():
    return get_entity_type("Episode")


def get_sequence_type():
    return get_entity_type("Sequence")


def get_shot_type():
    return get_entity_type("Shot")


def get_scene_type():
    return get_entity_type("Scene")


def get_episodes(criterions={}):
    episode_type = get_episode_type()
    criterions["entity_type_id"] = episode_type["id"]
    result = Entity.query.filter_by(**criterions).all()
    return Entity.serialize_list(result, obj_type="Episode")


def get_sequences(criterions={}):
    sequence_type = get_sequence_type()
    criterions["entity_type_id"] = sequence_type["id"]
    result = Entity.query.filter_by(**criterions).all()
    return Entity.serialize_list(result, obj_type="Sequence")


def get_shots(criterions={}):
    shot_type = get_shot_type()
    criterions["entity_type_id"] = shot_type["id"]
    Sequence = aliased(Entity, name='sequence')
    query = Entity.query.filter_by(**criterions)
    query = query.join(Project)
    query = query.join(Sequence, Sequence.id == Entity.parent_id)
    query = query.add_columns(Project.name)
    query = query.add_columns(Sequence.name)
    data = query.all()

    shots = []
    for (shot_model, project_name, sequence_name) in data:
        shot = shot_model.serialize(obj_type="Shot")
        shot["project_name"] = project_name
        shot["sequence_name"] = sequence_name
        shots.append(shot)

    return shots


def get_scenes(criterions={}):
    scene_type = get_scene_type()
    criterions["entity_type_id"] = scene_type["id"]
    Sequence = aliased(Entity, name='sequence')
    query = Entity.query.filter_by(**criterions)
    query = query.join(Project)
    query = query.join(Sequence, Sequence.id == Entity.parent_id)
    query = query.add_columns(Project.name)
    query = query.add_columns(Sequence.name)
    data = query.all()

    scenes = []
    for (scene_model, project_name, sequence_name) in data:
        scene = scene_model.serialize(obj_type="Scene")
        scene["project_name"] = project_name
        scene["sequence_name"] = sequence_name
        scenes.append(scene)

    return scenes


def get_task_status_map():
    return {
        status.id: status for status in TaskStatus.query.all()
    }


def get_task_type_map():
    return {
        task_type.id: task_type for task_type in TaskType.query.all()
    }


def get_episode_map(criterions={}):
    episodes = get_episodes(criterions)
    episode_map = {}
    for episode in episodes:
        episode_map[episode["id"]] = episode
    return episode_map


def get_shot_map(criterions={}):
    shot_map = {}
    episode_map = get_episode_map(criterions)

    shot_type = get_shot_type()
    Sequence = aliased(Entity, name='sequence')
    shot_query = Entity.query \
        .join(EntityType) \
        .join(Sequence, Sequence.id == Entity.parent_id) \
        .add_columns(Sequence.name, Sequence.parent_id) \
        .filter(Entity.entity_type_id == shot_type["id"])
    if "project_id" in criterions:
        shot_query = \
            shot_query.filter(Entity.project_id == criterions["project_id"])
    shots = shot_query.all()

    for (shot, sequence_name, sequence_parent_id) in shots:
        shot_id = str(shot.id)
        episode_name = ""
        episode = episode_map.get(str(sequence_parent_id), None)

        if episode is not None:
            episode_name = episode["name"]

        if shot.preview_file_id is not None:
            preview_file_id = str(shot.preview_file_id)
        else:
            preview_file_id = ""

        shot_map[shot_id] = {
            "id": str(shot.id),
            "name": shot.name,
            "description": shot.description,
            "frame_in": shot.data.get("frame_in", None),
            "frame_out": shot.data.get("frame_out", None),
            "preview_file_id": preview_file_id,
            "sequence_id": str(shot.parent_id),
            "sequence_name": sequence_name,
            "episode_id": str(sequence_parent_id),
            "episode_name": episode_name,
            "canceled": shot.canceled,
            "data": fields.serialize_value(shot.data)
        }

    return shot_map


def get_shots_and_tasks(criterions={}):
    shot_type = get_shot_type()
    task_status_map = get_task_status_map()
    task_type_map = get_task_type_map()
    shot_map = get_shot_map(criterions)
    task_map = {}

    query = Task.query \
        .join(Entity) \
        .filter(Entity.entity_type_id == shot_type["id"])

    if "project_id" in criterions:
        query = query.filter(Entity.project_id == criterions["project_id"])

    tasks = query.all()

    for task in tasks:
        shot_id = str(task.entity_id)

        if shot_id not in task_map:
            task_map[shot_id] = []

        task_dict = {"id": str(task.id)}
        task_status = task_status_map[task.task_status_id]
        task_type = task_type_map[task.task_type_id]
        task_dict.update({
            "task_status_id": str(task_status.id),
            "task_status_name": task_status.name,
            "task_status_short_name": task_status.short_name,
            "task_status_color": task_status.color,
            "task_type_id": str(task_type.id),
            "task_type_name": task_type.name,
            "task_type_color": task_type.color,
            "task_type_priority": task_type.priority,
            "assignees": fields.serialize_value(task.assignees)
        })
        task_map[shot_id].append(task_dict)

    shots = []
    for shot in shot_map.values():
        shot["tasks"] = task_map.get(shot["id"], [])
        shots.append(shot)

    return shots


def get_shot_raw(shot_id):
    shot_type = get_shot_type()
    try:
        shot = Entity.get_by(
            entity_type_id=shot_type["id"],
            id=shot_id
        )
    except StatementError:
        raise SequenceNotFoundException

    if shot is None:
        raise ShotNotFoundException

    return shot


def get_shot(shot_id):
    return get_shot_raw(shot_id).serialize(obj_type="Shot")


def get_full_shot(shot_id):
    shot = get_shot(shot_id)
    project = Project.get(shot["project_id"])
    sequence = Entity.get(shot["parent_id"])
    shot["project_name"] = project.name
    shot["sequence_id"] = str(sequence.id)
    shot["sequence_name"] = sequence.name

    if sequence.parent_id is not None:
        episode = Entity.get(sequence.parent_id)
        shot["episode_id"] = str(episode.id)
        shot["episode_name"] = episode.name

    return shot


def get_scene_raw(scene_id):
    scene_type = get_scene_type()
    try:
        scene = Entity.get_by(
            entity_type_id=scene_type["id"],
            id=scene_id
        )
    except StatementError:
        raise SequenceNotFoundException

    if scene is None:
        raise SceneNotFoundException

    return scene


def get_scene(scene_id):
    return get_scene_raw(scene_id).serialize(obj_type="Scene")


def get_full_scene(scene_id):
    scene = get_scene(scene_id)
    project = Project.get(scene["project_id"])
    sequence = Entity.get(scene["parent_id"])
    scene["project_name"] = project.name
    scene["sequence_id"] = str(sequence.id)
    scene["sequence_name"] = sequence.name

    if sequence.parent_id is not None:
        episode = Entity.get(sequence.parent_id)
        scene["episode_id"] = str(episode.id)
        scene["episode_name"] = episode.name

    return scene


def get_sequence_raw(sequence_id):
    sequence_type = get_sequence_type()
    try:
        sequence = Entity.get_by(
            entity_type_id=sequence_type["id"],
            id=sequence_id
        )
    except StatementError:
        raise SequenceNotFoundException

    if sequence is None:
        raise SequenceNotFoundException

    return sequence


def get_sequence(sequence_id):
    return get_sequence_raw(sequence_id).serialize(obj_type="Sequence")


def get_full_sequence(sequence_id):
    sequence = get_sequence(sequence_id)
    project = Project.get(sequence["project_id"])
    sequence["project_name"] = project.name

    if sequence["parent_id"] is not None:
        episode = Entity.get(sequence["parent_id"])
        sequence["episode_id"] = str(episode.id)
        sequence["episode_name"] = episode.name

    return sequence


def get_episode_raw(episode_id):
    episode_type = get_episode_type()
    try:
        episode = Entity.get_by(
            entity_type_id=episode_type["id"],
            id=episode_id
        )
    except StatementError:
        raise EpisodeNotFoundException

    if episode is None:
        raise EpisodeNotFoundException
    return episode


def get_episode(episode_id):
    return get_episode_raw(episode_id).serialize(obj_type="Episode")


def get_full_episode(episode_id):
    episode = get_episode(episode_id)
    project = Project.get(episode["project_id"])
    episode["project_name"] = project.name
    return episode


def get_shot_by_shotgun_id(shotgun_id):
    shot_type = get_shot_type()
    shot = Entity.get_by(
        entity_type_id=shot_type["id"],
        shotgun_id=shotgun_id
    )
    if shot is None:
        raise ShotNotFoundException

    return shot.serialize(obj_type="Shot")


def get_sequence_by_shotgun_id(shotgun_id):
    sequence_type = get_sequence_type()
    sequence = Entity.get_by(
        entity_type_id=sequence_type["id"],
        shotgun_id=shotgun_id
    )
    if sequence is None:
        raise SequenceNotFoundException

    return sequence


def is_shot(entity):
    shot_type = get_shot_type()
    return str(entity["entity_type_id"]) == shot_type["id"]


def is_scene(entity):
    scene_type = get_scene_type()
    return str(entity["entity_type_id"]) == scene_type["id"]


def is_sequence(entity):
    sequence_type = get_sequence_type()
    return str(entity["entity_type_id"]) == sequence_type["id"]


def is_episode(entity):
    episode_type = get_episode_type()
    return str(entity["entity_type_id"]) == episode_type["id"]


def get_or_create_episode(project_id, name):
    episode_type = get_episode_type()
    episode = Entity.get_by(
        entity_type_id=episode_type["id"],
        project_id=project_id,
        name=name
    )
    if episode is None:
        episode = Entity(
            entity_type_id=episode_type["id"],
            project_id=project_id,
            name=name
        )
        episode.save()
    return episode


def get_or_create_sequence(project_id, episode_id, name):
    sequence_type = get_sequence_type()
    sequence = Entity.get_by(
        entity_type_id=sequence_type["id"],
        parent_id=episode_id,
        project_id=project_id,
        name=name
    )
    if sequence is None:
        sequence = Entity(
            entity_type_id=sequence_type["id"],
            parent_id=episode_id,
            project_id=project_id,
            name=name
        )
        sequence.save()
    return sequence


def get_entities_for_project(project_id, entity_type_id, obj_type="Entity"):
    projects_service.get_project_raw(project_id)
    result = Entity.get_all_by(
        entity_type_id=entity_type_id,
        project_id=project_id
    )
    return Entity.serialize_list(result, obj_type=obj_type)


def get_episodes_for_project(project_id):
    return get_entities_for_project(
        project_id,
        get_episode_type()["id"],
        "Episode"
    )


def get_sequences_for_project(project_id):
    return get_entities_for_project(
        project_id,
        get_sequence_type()["id"],
        "Sequence"
    )


def get_shots_for_project(project_id):
    return get_entities_for_project(
        project_id,
        get_shot_type()["id"],
        "Shot"
    )


def get_scenes_for_project(project_id):
    return get_entities_for_project(
        project_id,
        get_scene_type()["id"],
        "Scene"
    )


def get_scenes_for_sequence(sequence_id):
    get_sequence(sequence_id)
    result = Entity.get_all_by(
        parent_id=sequence_id,
        entity_type_id=get_scene_type()["id"],
    )
    return Entity.serialize_list(result, "Scene")


def remove_shot(shot_id):
    shot = get_shot_raw(shot_id)
    try:
        shot.delete()
    except IntegrityError:
        shot.update({"canceled": True})
    deleted_shot = shot.serialize(obj_type="Shot")
    events.emit("shot:deletion", {"deleted_shot": deleted_shot})
    return deleted_shot


def remove_scene(scene_id):
    scene = get_scene_raw(scene_id)
    try:
        scene.delete()
    except IntegrityError:
        scene.update({"canceled": True})
    deleted_scene = scene.serialize(obj_type="Scene")
    events.emit("scene:deletion", {"deleted_scene": deleted_scene})
    return deleted_scene


def create_episode(project_id, name):
    episode_type = get_episode_type()
    episode = Entity.get_by(
        entity_type_id=episode_type["id"],
        project_id=project_id,
        name=name
    )
    if episode is None:
        episode = Entity.create(
            entity_type_id=episode_type["id"],
            project_id=project_id,
            name=name
        )
    return episode.serialize(obj_type="Episode")


def create_sequence(project_id, episode_id, name):
    sequence_type = get_sequence_type()

    if episode_id is not None:
        get_episode(episode_id)  # raises EpisodeNotFound if it fails.

    sequence = Entity.get_by(
        entity_type_id=sequence_type["id"],
        parent_id=episode_id,
        project_id=project_id,
        name=name
    )
    if sequence is None:
        sequence = Entity.create(
            entity_type_id=sequence_type["id"],
            project_id=project_id,
            parent_id=episode_id,
            name=name
        )
    return sequence.serialize(obj_type="Sequence")


def create_shot(project_id, sequence_id, name, data={}):
    shot_type = get_shot_type()

    if sequence_id is not None:
        get_sequence(sequence_id)  # raises SequenceNotFound if it fails.

    shot = Entity.get_by(
        entity_type_id=shot_type["id"],
        parent_id=sequence_id,
        project_id=project_id,
        name=name
    )
    if shot is None:
        shot = Entity.create(
            entity_type_id=shot_type["id"],
            project_id=project_id,
            parent_id=sequence_id,
            name=name,
            data=data
        )
    return shot.serialize(obj_type="Shot")


def create_scene(project_id, sequence_id, name):
    scene_type = get_scene_type()

    if sequence_id is not None:
        # raises SequenceNotFound if it fails.
        sequence = get_sequence(sequence_id)
        if sequence["project_id"] != project_id:
            raise SequenceNotFoundException

    scene = Entity.get_by(
        entity_type_id=scene_type["id"],
        parent_id=sequence_id,
        project_id=project_id,
        name=name
    )
    if scene is None:
        scene = Entity.create(
            entity_type_id=scene_type["id"],
            project_id=project_id,
            parent_id=sequence_id,
            name=name,
            data={}
        )
    return scene.serialize(obj_type="Scene")


def get_entities_out(shot_id):
    shot = get_shot_raw(shot_id)
    return Entity.serialize_list(shot.entities_out, obj_type="Asset")
