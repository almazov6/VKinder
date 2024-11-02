import configpars
from vkton import Bot, Commands, Context

bot = Bot(configpars.cfg.configparser('VK'), group_id=228101541)


@Commands.command(keywords=['Начать'], back_to='Начать')
def hello(ctx: Context):
    ctx.user.send('Hello')


bot.run()
