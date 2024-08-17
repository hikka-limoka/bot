from aiogram import Router
from aiogram.types import InlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.api import LimokaAPI
from app.search import Search
from app.keyboards.inline import module_keyboard

import random, html

router = Router()


@router.inline_query()
async def module_query(inline_query: InlineQuery):
    if inline_query.query:
        api = LimokaAPI()
        modules = await api.get_all_modules()

        contents = []

        for module in modules:
            contents.append(
                {
                    "id": module["id"],
                    "content": module["name"],
                }
            )

        for module in modules:
            contents.append(
                {
                    "id": module["id"],
                    "content": module["description"],
                }
            )

        for module in modules:
            for command in module["commands"]:
                contents.append({"id": module["id"], "content": command["command"]})
                contents.append({"id": module["id"], "content": command["description"]})

        search = Search(inline_query.query)
        modules_matched = search.search_module(contents)

        results = []

        if type(modules_matched) is int and modules_matched == 0:
            return InlineQueryResultArticle(
                    id="404",
                    title="<b>Not found</b>",
                    description="<i>Not found</i>",
                    input_message_content=InputTextMessageContent(
                        message_text=
                        "Not found"
                    ),
                )

        for module in modules_matched:
            info = await api.get_module_by_id(module)
            commands = []

            command_template = "<code>.{command}</code> - <i>{description}</i>"

            for command in info["commands"]:
                commands.append(
                    command_template.format(
                        command=command["command"], description=command["description"]
                    )
                )

            commands = "\n".join(commands)

            dev_username = info["developer"]
            name = info["name"]
            results.append(
                InlineQueryResultArticle(
                    id=f"{random.randint(1,10000000000000000)}",
                    title=f"{info['name']}",
                    description=f"{info['description']}",
                    input_message_content=InputTextMessageContent(
                        message_text=(
                            f"🔎 Best guess for <code>{html.escape(inline_query.query)}</code>"
                            "\n"
                            f"\n🧩 <b>Module <code>{html.escape(name)}</code> by {dev_username}</b>"
                            f"\nℹ️ <i>{info['description']}</i>"
                            f"\n🔽 <b>Downloads:</b> {len(info['downloads'])}"
                            f"\n👀 <b>Views:</b> {len(info['looks'])}"
                            f"\n\n{commands}"
                        ),
                    ),
                    reply_markup=module_keyboard(info["id"]),
                )
            )

            await inline_query.answer(
                results=results,
                cache_time=30,
                is_personal=True,
            )
