from telebot.bot import Bot


class MessageUpdater:

    def __init__(self, bot, timeout=3600, verbose=False):
        self.bot = bot
        self.TIMEOUT = timeout
        self.VERBOSE = verbose

        self.handlers = []

    def register(self, handler):
        """Register a message handler.
        A handler must implement a method named handle_message that takes a
        reference to a bot instance and a message as arguments.
        """
        self.handlers.append(handler)

    def start_polling(self):
        try:
            self.bot.connect()

            max_update_id = -1

            while True:

                if max_update_id < 0:
                    updates = self.bot.get_updates(timeout=self.TIMEOUT)

                else:
                    updates = self.bot.get_updates(
                        offset=max_update_id + 1,
                        timeout=self.TIMEOUT)

                if updates is not None:

                    if updates:
                        max_update_id = -1

                    for update in updates:

                        if update is None or 'message' not in update:
                            continue

                        if self.VERBOSE:
                            print("Received message update: " +
                                  str(update['update_id']))

                        for handler in self.handlers:
                            handler.handle_message(self.bot, update['message'])

                        update_id = update['update_id']
                        if update_id > max_update_id:
                            max_update_id = update_id

        except KeyboardInterrupt:
            if self.VERBOSE:
                print()
                print("Detected interrupt from keyboard. Closing...")
            self.bot.disconnect()
