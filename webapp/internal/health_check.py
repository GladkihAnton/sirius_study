from fastapi.responses import ORJSONResponse

from webapp.internal.router import internal_router


@internal_router.get('/health_check')
async def health_check():
    return ORJSONResponse({'status': 'ok'})
