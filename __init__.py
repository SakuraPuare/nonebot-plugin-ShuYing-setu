from io import BytesIO

import httpx
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import MessageSegment

m = on_startswith(('色图', 'setu', '来张色图', '涩图'))


@m.handle()
async def setu() -> None:
	url = 'https://api.sakurapuare.com/pic/?type=png'
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
			with open('temp.png', 'wb') as f:
				f.write(res.content)
				f.close()
			await m.finish(MessageSegment.image(file=BytesIO(res.content)))
