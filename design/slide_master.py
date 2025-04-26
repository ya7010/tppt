from typing import Annotated

from typing_extensions import dataclass_transform


class Placeholder:
    pass


class TpptSlideLayoutMeta(type):
    """TpptSlideLayoutのメタクラス"""

    ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideLayout(metaclass=TpptSlideLayoutMeta):
    """スライドレイアウトのベースクラス"""

    ...


class MySlideLayout(TpptSlideLayout):
    title: Annotated[str, Placeholder]
    text: Annotated[str, Placeholder]


myslide: type[TpptSlideLayout] = MySlideLayout
myslide(title="a", text="b")
