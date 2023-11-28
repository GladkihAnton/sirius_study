from socket import AF_INET
from urllib.parse import urlparse

import aiohttp
from fastapi import HTTPException, Request, status
from fastapi.responses import ORJSONResponse

async def do_proxy_request(request: Request, url: str) -> ORJSONResponse:
    domain = urlparse(url).netloc

    headers = request.headers.mutablecopy() | {
        'host': domain,
    }
    query_params = request.query_params
    data = await request.body()

    timeout = aiohttp.ClientTimeout(total=10)
    connector = aiohttp.TCPConnector(family=AF_INET, limit=0, ssl=False)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        async with session.request(
            method=request.method,
            url=url,
            headers=headers,
            params=query_params,
            data=data,
        ) as response:
            if response.status not in (status.HTTP_200_OK, status.HTTP_201_CREATED):
                detail = await response.json(content_type=response.content_type)

                raise HTTPException(status_code=response.status, detail=detail)

            return ORJSONResponse(await response.json())
