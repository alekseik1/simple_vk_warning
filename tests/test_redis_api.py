import pytest
import fakeredis.aioredis
import aioredis
from pytest_mock import MockFixture
from unittest.mock import AsyncMock
from typing import Tuple, List

from src.redis_.crud import set_password_for_user, get_password_from_redis


@pytest.mark.good_input
@pytest.mark.asyncio
async def test_get_password_from_filled_redis_gives_correct_data(
        fake_credentials: List[Tuple[int, str]], redis_filled: aioredis.Redis):
    # GIVEN: filled redis database
    # WHEN: calling get_password_from_redis
    # THEN: correct data is obtained
    for user_id, expected_password in fake_credentials:
        assert expected_password == await get_password_from_redis(redis_filled, user_id)


@pytest.mark.good_input
@pytest.mark.asyncio
async def test_set_password_does_not_fail(
        fake_credentials, redis_empty
):
    # GIVEN: empty redis database
    # WHEN: calling set_password_for_user
    # THEN: nothing fails
    for user_id, password in fake_credentials:
        await set_password_for_user(redis_empty, user_id, password)


@pytest.mark.good_input
@pytest.mark.asyncio
async def test_set_and_get_password_give_same_results(
        redis_empty, fake_credentials
):
    # GIVEN: empty redis database
    # WHEN: calling set_password_for_user
    for user_id, password in fake_credentials:
        await set_password_for_user(redis_empty, user_id, password)
    # THEN: get_password_for_user will give correct results
    for user_id, expected_password in fake_credentials:
        assert expected_password == await get_password_from_redis(redis_empty, user_id)


@pytest.mark.good_input
@pytest.mark.asyncio
async def test_closes_connection_after_transaction(redis_empty, close_redis_mock: AsyncMock):
    # GIVEN: empty redis database
    # WHEN: calling any redis method
    # THEN: connection being properly closed
    await set_password_for_user(redis_empty, 1, '1')
    assert close_redis_mock.call_count == 1
    await get_password_from_redis(redis_empty, 1)
    assert close_redis_mock.call_count == 2


@pytest.fixture()
async def close_redis_mock(mocker: MockFixture):
    quit_mock = mocker.AsyncMock()
    # fakeredis does not support 'QUIT', so need to mock it
    mocker.patch.object(aioredis.Redis, 'quit', quit_mock)
    return quit_mock


@pytest.fixture()
async def redis_empty(mocker: MockFixture, close_redis_mock):
    redis = await fakeredis.aioredis.create_redis_pool()
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture()
async def fake_credentials(redis_empty: aioredis.Redis):
    creds = [(i, str(i) * 10) for i in range(10)]
    yield creds


@pytest.fixture()
async def redis_filled(redis_empty, fake_credentials):
    for u, p in fake_credentials:
        await redis_empty.set(u, p)
    return redis_empty
