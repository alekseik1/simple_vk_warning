import pytest
from pathlib import Path
from pytest_mock import MockFixture


basedir = Path(__file__).parent


@pytest.mark.asyncio
@pytest.mark.parametrize('text', [
    'command fialw', 'фывйцв', 'smtgsh'
])
async def test_goes_to_fallback_on_unknown_message(
        text,
        mocker: MockFixture,
        monkeypatch,
        fake_vk_api_message_builder
):
    monkeypatch.chdir(basedir.parent.parent / 'src')
    monkeypatch.syspath_prepend(basedir.parent.parent / 'src')
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
