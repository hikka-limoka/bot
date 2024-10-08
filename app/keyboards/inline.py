from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_author_keyboard(owner_ids):
    buttons = [
        #[InlineKeyboardButton(text="Автор", url=f"tg://user?id={owner_id}")],
        [[InlineKeyboardButton(text="Автор", url=f"tg://user?id={owner_id}") for owner_id in owner_ids]]
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def mailing_keyboard(buttons):
    keyboard = []
    for button in buttons:
        keyboard.append([InlineKeyboardButton(text=button[0], url=button[1])])

    keyboard = InlineKeyboardBuilder(markup=keyboard)
    return keyboard.as_markup()


def start_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Add/Remove Repo", url="https://t.me/vsecoder")
    )

    builder.add(
        InlineKeyboardButton(text="Report broken module", url="https://t.me/vsecoder")
    )

    builder.add(InlineKeyboardButton(text="Changelog", url="https://t.me/limokanews"))

    builder.adjust(1)

    return builder.as_markup()


def module_keyboard(module_id):
    buttons = [
        [InlineKeyboardButton(text="🔽 Download", callback_data=f"install:{module_id}")]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
