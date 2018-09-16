from collections import namedtuple
from struct import unpack

Header = namedtuple('Header', 'magic version evtc_version boss_id')
Agent = namedtuple('Agent', 'address profession elite_mask toughness '
                            'concentration healing_power hitbox_width '
                            'condition_damage hitbox_height name')
Skill = namedtuple('Skill', 'id name')
CombatEvent = namedtuple('CombatEvent', 'time source_agent dest_agent value '
                                        'buff_damage overstack_value skill_id '
                                        'source_instance_id dest_instance_id '
                                        'source_master_instance_id pad_1 '
                                        'iff buff result is_activation '
                                        'is_buff_remove is_ninety is_fifty '
                                        'is_moving is_statechange is_flanking '
                                        'is_shields')


def _read_uint32(stream):
  """Unpack a uint32 from a stream."""
  return unpack('<I', stream.read(4))[0]


def _read_header(stream):
  """Unpack a header from a stream."""
  data = stream.read(16)
  return Header._make(unpack('<I8schx', data))


def _read_agent(stream):
  """Unpack an agent from a stream."""
  data = stream.read(96)
  return Agent._make(unpack('<QIIhhhhhh68s', data))


def _read_skill(stream):
  """Unpack a skill from a stream."""
  data = stream.read(68)
  return Skill._make(unpack('<I64s', data))


def _read_combat_event(stream):
  """Read a combat event from a stream."""
  data = stream.read(64)
  if not data:
    return None

  return CombatEvent._make(unpack('<QQQIIHHHHH9sbbb????????xx', data))


def parse_evtc(stream):
  """Parse an evtc file and return the combat events in a meaningful format."""
  header = _read_header(stream)

  agent_count = _read_uint32(stream)
  agents_by_address = {}
  for _ in range(agent_count):
    agent = _read_agent(stream)
    agents_by_address[agent.address] = agent
  
  skill_count = _read_uint32(stream)
  skills_by_id = {}
  for _ in range(skill_count):
    skill = _read_skill(stream)
    skills_by_id[skill.id] = skill

  combat_events = []
  while True:
    combat_event = _read_combat_event(stream)
    if not combat_event:
      break

    combat_events.append(combat_event)

  return header, agents_by_address, skills_by_id, combat_events
