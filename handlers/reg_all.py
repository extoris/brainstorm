from handlers.commands import register_handler_commands
from handlers.echo import register_echo
from handlers.manager import register_check_word, register_trans_list, register_trans_litters, register_trans_voice, register_incorrect_answer

async def reg_all_handlers(dp):
    register_handler_commands(dp)
    register_check_word(dp)
    register_trans_list(dp)
    register_trans_litters(dp)
    register_trans_voice(dp)
    register_incorrect_answer(dp)



    # register_echo(dp)