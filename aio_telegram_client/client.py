from aio_clients import (
    Http,
    Options,
    multipart,
)
from aiohttp import ClientTimeout


class Client(Http):
    def __init__(self, token: str):
        self.token = token
        super().__init__(
            host=f'https://api.telegram.org/bot{self.token}/',
        )

    async def get_updates(self, offset=None, timeout=None):
        return await self.post('getUpdates', json={
            'offset': offset,
            'timeout': timeout,
        }, o=Options(timeout=ClientTimeout(timeout + 1)))

    async def send_audio(self, chat_id: int, audio: bytes):
        with multipart.Easy('form-data') as form:
            form.add_form(multipart.Form(key='chat_id', value=str(chat_id)))
            form.add_form(multipart.File(key='audio', value=audio, file_name='land.mp3'))

        return await self.post('sendAudio', form=form)

    async def send_message(self, chat_id: int, text: str):
        return await self.post('sendMessage', json={
            'chat_id': chat_id,
            'text': text,
        })

    async def get_chat_admins(self, chat_id: int):
        return await self.post('getChatAdministrators', json={
            'chat_id': chat_id,
        })
