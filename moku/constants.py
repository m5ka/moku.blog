from django.utils.translation import gettext_lazy as _


class Verbs:
    ATE = "ate"
    DRANK = "drank"
    MADE = "made"
    COOKED = "cooked"
    BAKED = "baked"
    ORDERED = "ordered"
    CHOICES = (
        (ATE, _("%(user)s ate %(food)s")),
        (DRANK, _("%(user)s drank %(food)s")),
        (MADE, _("%(user)s made %(food)s")),
        (COOKED, _("%(user)s cooked %(food)s")),
        (BAKED, _("%(user)s baked %(food)s")),
        (ORDERED, _("%(user)s ordered %(food)s")),
    )


EMOJI_CATEGORIES = [
    (
        _("fruit & veg"),
        (
            "🍏",
            "🍎",
            "🍐",
            "🍊",
            "🍋",
            "🍌",
            "🍉",
            "🍇",
            "🍓",
            "🫐",
            "🍈",
            "🍒",
            "🍑",
            "🥭",
            "🍍",
            "🥥",
            "🥝",
            "🍅",
            "🍆",
            "🥑",
            "🫛",
            "🥦",
            "🥬",
            "🥒",
            "🌶️",
            "🫑",
            "🌽",
            "🥕",
            "🫒",
            "🧄",
            "🧅",
            "🥔",
            "🍠",
            "🫚",
        ),
    ),
    (
        _("savoury dishes"),
        (
            "🥯",
            "🍞",
            "🥖",
            "🥨",
            "🧀",
            "🥚",
            "🍳",
            "🧈",
            "🥞",
            "🧇",
            "🥓",
            "🥩",
            "🍗",
            "🍖",
            "🦴",
            "🌭",
            "🍔",
            "🍟",
            "🍕",
            "🫓",
            "🥪",
            "🥙",
            "🧆",
            "🌮",
            "🌯",
            "🫔",
            "🥗",
            "🥘",
            "🫕",
            "🥫",
            "🫙",
            "🍝",
            "🍜",
            "🍲",
            "🍛",
            "🍣",
            "🍱",
            "🥟",
            "🦪",
            "🍤",
            "🍙",
            "🍚",
            "🍘",
            "🍥",
            "🌰",
            "🥜",
            "🫘",
            "🧊",
        ),
    ),
    (
        _("sweet treats"),
        (
            "🥠",
            "🥮",
            "🍢",
            "🍡",
            "🍧",
            "🍨",
            "🍦",
            "🥧",
            "🧁",
            "🍰",
            "🎂",
            "🍮",
            "🍭",
            "🍬",
            "🍫",
            "🥐",
            "🍿",
            "🍩",
            "🍪",
            "🍯",
        ),
    ),
    (
        _("drinks"),
        (
            "🥛",
            "🫗",
            "🍼",
            "🫖",
            "☕️",
            "🍵",
            "🧃",
            "🥤",
            "🧋",
            "🍶",
            "🍺",
            "🍻",
            "🥂",
            "🍷",
            "🥃",
            "🍸",
            "🍹",
            "🧉",
            "🍾",
        ),
    ),
    (
        _("people"),
        (
            "😀",
            "😃",
            "😄",
            "😁",
            "😆",
            "🥹",
            "😅",
            "😂",
            "🤣",
            "🥲",
            "😊",
            "😇",
            "🙂",
            "🙃",
            "😉",
            "😌",
            "😌",
            "😍",
            "🥰",
            "😘",
            "😗",
            "😙",
            "😚",
            "😋",
            "😛",
            "😝",
            "😜",
            "🤪",
            "🤨",
            "🧐",
        ),
    ),
    (
        _("animals"),
        (
            "🐶",
            "🐱",
            "🐭",
            "🐹",
            "🐰",
            "🦊",
            "🐻",
            "🐼",
            "🐨",
            "🐯",
            "🦁",
            "🐮",
            "🐷",
            "🐽",
            "🐸",
            "🐵",
            "🙈",
            "🙉",
            "🙊",
            "🐒",
            "🐔",
            "🐧",
            "🐦",
            "🐤",
            "🐣",
            "🐥",
            "🪿",
            "🦆",
            "🐦‍⬛",
            "🦅",
            "🦉",
            "🦇",
            "🐺",
            "🐗",
            "🐴",
            "🦄",
            "🫎",
            "🐝",
            "🪱",
            "🐛",
            "🦋",
            "🐌",
            "🐞",
            "🐜",
            "🪰",
        ),
    ),
    (_("tools & things"), ("🥄", "🍴", "🍽️", "🥣", "🥡", "🥢", "🧂", "🔪", "🪓")),
]
