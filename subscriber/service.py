import json
import traceback
import logging
import switchbot
from repository import GetSwitchError,UpdateStateError,SwitchNotExistError, IRepository

def is_valid_format(payload: dict)->bool:
    if("switch_name" not in payload):
        logging.error("Switch name is not specified.")
        return False
    if("state" not in payload):
        logging.error("State is not specified")
        return False
    if not isinstance(payload["state"], bool):
        logging.error("State is invalid value.")
        return False
    return True

def exec_switchbot(payload: str, repository: IRepository)->None:
    try:
        received_data = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        logging.error(e.msg())
        logging.error(traceback.format_exc())
        return


    if is_valid_format(received_data):
        target_switch_name = received_data['switch_name']
        required_state = received_data['state']

        try:
            current_state = repository.get_switch_record_by_switch_name(target_switch_name)
        except SwitchNotExistError:
            logging.error("Switch {} is not registered.".format(target_switch_name))
            return
        except GetSwitchError:
            logging.error("Read state failed.")
            return


        if current_state["state"] != required_state:
            driver = switchbot.Driver(device=current_state["mac"], bt_interface="hci0", timeout_secs=8)
            try_count = 1
            result = b'\x00'
            while try_count < 5:
                try_count = try_count + 1
                result = driver.run_command("press")
                if result[0]==b'\x13':
                    logging.info("Press succeed")
                    try:
                        repository.update_state_by_switch_name(target_switch_name, required_state)
                    except UpdateStateError as e:
                        logging.info("Update state failed.")
                    break
                else:
                    logging.error("Press failed {} times.".format(try_count))
        else:
            logging.warning("Already switch is {}".format("ON" if required_state else "OFF"))
