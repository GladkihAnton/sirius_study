from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi import status
from sqlalchemy import select

from webapp.models.sirius.user import User

# from httpx import AsyncClient

# from tests.api.auth.login.const import EXPECTED_FAILED_LOGIN, EXPECTED_SUCCESS_LOGIN, REQUEST_WITH_API_KEY_AND_EMAIL
# from tests.const import URLS

DIR_PATH = Path(__file__).parent
TASK_FIXTURE_PATH = DIR_PATH / 'fixtures'


@pytest.mark.parametrize(
    (
        'fixtures',
        # 'query_params',
        # 'expected_status',
        # 'expected_response',
    ),
    [
        (
            [TASK_FIXTURE_PATH / 'sirius.user.json'],
        ),
        (
            [],
        ),
    ],

)
# @pytest.mark.usefixtures('_common_api_fixture')
# @pytest.mark.freeze_time('2020-09-04 17:31:14.46')
@pytest.mark.asyncio()
async def test_login(
    init_database: int,
    load_fixture,
    # client: AsyncClient,
    # query_params: Dict[str, str],
    # expected_status: int,
    # expected_response: Any,
    db_session
) -> None:
    users = (await db_session.execute(select(User))).all()
    pass
    # response = await client.post(URLS['auth']['login'], json=query_params)
    # assert response.status_code == expected_status
    # assert response.json() == expected_response
