from typing import Annotated, Any

from typing_extensions import dataclass_transform


class Placeholder:
    # TODO: 実装せよ
    ...


class TpptSlideLayoutMeta(type):
    """TpptSlideLayoutのメタクラス"""

    # TODO: 実装せよ
    ...


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideLayout(metaclass=TpptSlideLayoutMeta):
    """スライドレイアウトのベースクラス"""

    # TODO: 実装せよ
    ...


class MySlideLayout(TpptSlideLayout):
    title: Annotated[str, Placeholder]
    text: Annotated[str, Placeholder]

def get_placeholders(slide: TpptSlideLayout) -> dict[str, Any]:
    """クラスのメタ情報を解析し、プレースホルダーのフィールドのキーバリューを取得する"""

    # TODO: 実装せよ
    raise NotImplementedError


# TODO: 以下のアサーションが通るようにせよ
myslide: type[TpptSlideLayout] = MySlideLayout
myslide(title="a", text="b")


