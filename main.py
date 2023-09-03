from telegram import Update, InputMediaPhoto, InputMediaDocument
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder
import asyncio
import logging
import configparser
import os

cwd = os.getcwd()
config = configparser.ConfigParser()
config.read(f'{cwd}/cfg/config.ini')
BOT_TOKEN = config['APP']['BOT_TOKEN']
RECEIVER_CHANNEL_ID = config['APP']['RECEIVER_CHANNEL_ID']


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger("ConsumeInformationBot")

logger.info(msg=f"BotToken: {BOT_TOKEN} chanel_id: {RECEIVER_CHANNEL_ID}")


class LoggingMessageHandler(MessageHandler):
    async def handle_update(self,
                            update: Update,
                            application,
                            check_result,
                            context):
        # Log the message first
        if update.message and update.message.from_user:
            user = update.message.from_user
            chat_id = update.message.chat_id
            logger.info(f"Received message from {user.first_name} {user.last_name} (ID: {user.id}) chat_id: {chat_id} "
                        f"Message ID: {update.message.message_id} Message: {update.message}")

        if update.channel_post:
            user = update.channel_post.from_user
            sender = update.channel_post.sender_chat
            text = update.channel_post.text
            logger.info(f"Received message from channel {user} (sender_chat: {sender}):  Message {text}")

        # Then call the parent class's handle_update method to process the update as usual
        await super().handle_update(update,
                                    application,
                                    check_result,
                                    context)


async def send_to_channel(update: Update, subject, body, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Subject {subject}")
    logger.info(msg=f"Body {body}")
    logger.info(msg=f"Now will call send_mesage to channel  {chanel_id}")
    await update.get_bot().send_message(chat_id=chanel_id, text=f"{subject}\n{body}")

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


async def send_photo_to_channel(update: Update, user,  photo, caption, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Photo caption {caption}")
    logger.info(msg=f"Now will call send_photo to channel  {chanel_id}")

    await update.get_bot().send_photo(chat_id=chanel_id, photo=photo, caption=caption)

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


async def send_video_to_channel(update: Update, user,  video, caption, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Photo caption {caption}")
    logger.info(msg=f"Now will call send_video to channel  {chanel_id}")

    await update.get_bot().send_video(chat_id=chanel_id, video=video, caption=caption)

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


async def send_video_note_to_channel(update: Update, user,  video_note, caption, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Photo caption {caption}")
    logger.info(msg=f"Now will call send_video_note to channel  {chanel_id}")

    await update.get_bot().send_video_note(chat_id=chanel_id, video_note=video_note, caption=caption)

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


async def send_voice_to_channel(update: Update, user,  voice, caption, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Photo caption {caption}")
    logger.info(msg=f"Now will call send_voice to channel  {chanel_id}")

    await update.get_bot().send_voice(chat_id=chanel_id, voice=voice, caption=caption)

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


async def send_audio_to_channel(update: Update, user,  audio, caption, chanel_id=RECEIVER_CHANNEL_ID):
    logger.info(msg=f"Photo caption {caption}")
    logger.info(msg=f"Now will call send_audio to channel  {chanel_id}")

    await update.get_bot().send_audio(chat_id=chanel_id, audio=audio, caption=caption)

    must_delete = await update.message.reply_text("Дякую. Повідомлення прийняте")
    await asyncio.sleep(5)
    logger.info(msg=f"Deleting message in bot after 5sec")
    await update.get_bot().delete_message(update.message.chat_id, update.message.message_id)
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


# Define the start command
async def start(update: Update, _: CallbackContext) -> None:
    must_delete = await update.message.reply_text("Привет. Сообщи нам любую информацию. Мы знаем, что с ней делать.")
    if must_delete:
        await update.get_bot().delete_message(update.message.chat_id, must_delete.message_id)


# Define the message handler
async def forward_message(update: Update, _: CallbackContext):# -> None:
    # if update.message is None or update.message.from_user is None or update.channel_post is None:
    #     return

    if update.message and update.message.from_user:
        message_text = update.message.text
        user = update.message.from_user
        chat_id = update.message.chat_id
        body = f"Сообщение: {message_text}"
        # Handle images
        if update.message.photo:
            photo = update.message.photo[-1]
            caption = ""
            if update.message.caption:
                caption += f"caption: {update.message.caption}"

            caption += f"\nОт {user.username}\nИмя: {user.first_name} {user.last_name}"
            logger.info(msg=f"Sending photo to channel caption: {caption}")
            return await send_photo_to_channel(update, user, photo, caption)

        # Handle video
        if update.message.video:
            video = update.message.video
            caption = ""
            if update.message.caption:
                caption += f"caption: {update.message.caption}"

            caption += f"\nОт {user.username}\nИмя: {user.first_name} {user.last_name}"
            logger.info(msg=f"Sending video to channel, caption: {caption}")
            return await send_video_to_channel(update, user, video, caption)

        if update.message.video_note:
            video_note = update.message.video_note
            caption = ""
            if update.message.caption:
                caption += f"caption: {update.message.caption}"

            caption += f"\nОт {user.username}\nИмя: {user.first_name} {user.last_name}"
            logger.info(msg=f"Sending video to channel, caption: {caption}")
            return await send_video_note_to_channel(update, user, video_note, caption)

        # Handle voice
        if update.message.voice:
            voice = update.message.voice
            caption = ""
            if update.message.caption:
                caption += f"caption: {update.message.caption}"

            caption += f"\nОт {user.username}\nИмя: {user.first_name} {user.last_name}"
            logger.info(msg=f"Sending voice to channel, caption: {caption}")
            return await send_voice_to_channel(update, user, voice, caption)

        if update.message.audio:
            audio = update.message.audio
            caption = ""
            if update.message.caption:
                caption += f"caption: {update.message.caption}"
            # photo_url = (await photo.get_file()).file_path
            # body += f"\nImage: {photo_url}"
            caption += f"\nОт {user.username}\nИмя: {user.first_name} {user.last_name}"
            logger.info(msg=f"Sending audio to channel, caption: {caption}")
            return await send_audio_to_channel(update, user, audio, caption)

        # Handle files
        if update.message.document:
            document = update.message.document
            document_url = (await document.get_file()).file_path
            body += f"\nFile: {document_url}"

        # Handle location
        if update.message.location:
            location = update.message.location
            body += f"\nLocation: Latitude: {location.latitude}, Longitude: {location.longitude}"

        subject = f"От {user.username} Имя: {user.first_name} {user.last_name}"
        logger.info(msg=f"Sending to channel message {subject}")
        await send_to_channel(update, subject, body)

    # await update.message.reply_text("Message forwarded! Thank You.")

    elif update.channel_post:
        message_text = update.channel_post.text
        chat_id = update.channel_post.chat_id  # sender_chat
        sender_chat = update.channel_post.sender_chat
        body = f"Message: {message_text}"
        logger.info(msg=f"Got message from channel chat_id: {chat_id} sender_chat: {sender_chat} {body}")
    else:
        return


async def log_message(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    message_text = update.message.text

    logger.info(msg=f"message_text {message_text}")


async def handler_all(update: Update, _: CallbackContext) -> None:
    message = update.message
    logger.info(message)


def main() -> None:

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the command and message handlers
    # application.add_handler(MessageHandler(filters.ALL, handler_all))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(LoggingMessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.add_handler(LoggingMessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.add_handler(LoggingMessageHandler(filters.PHOTO, forward_message))
    application.add_handler(LoggingMessageHandler(filters.Document.ALL, forward_message))
    application.add_handler(LoggingMessageHandler(filters.LOCATION, forward_message))

    application.add_handler(LoggingMessageHandler(filters.VIDEO, forward_message))
    application.add_handler(LoggingMessageHandler(filters.VOICE, forward_message))
    application.add_handler(LoggingMessageHandler(filters.AUDIO, forward_message))
    application.add_handler(LoggingMessageHandler(filters.VIDEO_NOTE, forward_message))

    # Start the Bot and run it until a signal is received or the process is killed
    application.run_polling()


if __name__ == '__main__':
    main()
