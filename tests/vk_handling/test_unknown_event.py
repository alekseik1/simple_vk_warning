import pytest
from pytest_mock import MockFixture


@pytest.mark.asyncio
@pytest.mark.parametrize('text', [
    'command fialw', 'фывйцв', 'smtgsh'
])
async def test_goes_to_fallback_on_unknown_message(
        text,
        mocker: MockFixture,
        fake_vk_api_message_builder
):
    from src.bot import bot
    bot.api = fake_vk_api_message_builder(text=text)
    mock = mocker.AsyncMock()
    bot.labeler.message_view.handlers[-1].handle = mock

    async for event in bot.polling.listen():
        assert 'updates' in event
        for update in event['updates']:
            await bot.router.route(update, bot.api)
        break
    mock.assert_called_once()
