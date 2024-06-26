from aiogram.utils import executor
from utils.notify_admins import on_startup_notify
from loader import dp

import handler, admin, keyboard, utils


async def startup(dispatcher):
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
