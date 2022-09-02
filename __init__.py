from io import BytesIO
from typing import Union

import httpx
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Bot, MessageSegment, Message

m = on_startswith(('色图', 'setu', '来张色图', '涩图'), priority=5, block=True)


def get_type(event: Union[GroupMessageEvent, PrivateMessageEvent]) -> int:
	"""
	Get the type of event
    :param event: Union[GroupMessageEvent, PrivateMessageEvent]
    :return: type of event, 1 is private message, 2 is group message
    """
	types = event.message_type
	if types == 'private_message':
		return 1
	elif types == 'group_message':
		return 2


@m.handle()
async def setu(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]) -> None:
	url = 'https://api.sakurapuare.com/pic/?type=png'
	msg = event.message[0].data['text']
	msg_list = msg.split(' ')
	if len(msg_list) == 1:
		nums = 1
	else:
		nums = int(msg_list[-1])
	if nums <= 5:
		for i in range(nums):
			async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
				try:
					res = await client.get(url)
					if res.is_error:
						logger.error("[setu] 获取色图失败")
				except httpx.ReadTimeout:
					return
				except httpx.ConnectTimeout:
					await m.finish(message='获取色图失败了呢~')
				else:
					await bot.send_msg(group_id=event.group_id,
					                   message=Message(MessageSegment.image(file=BytesIO(res.content))))
	else:
		await m.finish(message='一次最多只能获取5张哦~')
