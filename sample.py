"""Sample script to demonstrate library usage."""
import os
import sys

from zipfile import ZipFile

from evtc import parse_evtc

DEIMOS_BOSS_ID = 0x4302
RAPID_DECAY_ID = 37716


def test_one_log(zip_file_path):
  """Get the name of the first player to step in oil for one log."""
  with ZipFile(zip_file_path) as zip_file:
    subresource_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    with zip_file.open(subresource_name, 'r') as data_file:
      header, agents_by_address, skills_by_id, combat_events = parse_evtc(
          data_file)

  assert header.boss_id == DEIMOS_BOSS_ID, (
      '{path} is not a Deimos log'.format(path=zip_file_path))

  if RAPID_DECAY_ID not in skills_by_id:
    return None

  for combat_event in combat_events:
    if (combat_event.skill_id == RAPID_DECAY_ID and
        combat_event.dest_agent and
        combat_event.result <= 2):
      agent = agents_by_address[combat_event.dest_agent]
      agent_name = agent.name.decode('utf-8', errors='ignore')
      if ':' not in agent_name:
        continue

      print(agent_name.strip(), zip_file_path)
      return


def main(argv):
  """Main function."""
  assert argv, 'Argument must be a path to a log directory.'

  for file_path in os.listdir(argv[0]):
    if not file_path.endswith('.zip'):
      continue

    test_one_log(os.path.join(argv[0], file_path))


if __name__ == '__main__':
  main(sys.argv[1:])