from inspect import isclass
from typing import Annotated, Any, ClassVar, get_type_hints

from typing_extensions import dataclass_transform, get_args, get_origin


class Placeholder:
    """プレースホルダーを表すクラス。

    Annotatedと共に使用して、フィールドがプレースホルダーであることを示します。
    """

    def __init__(self, description: str = ""):
        self.description = description

    def __repr__(self) -> str:
        return f"Placeholder({self.description!r})"


class TpptSlideLayoutMeta(type):
    """TpptSlideLayoutのメタクラス

    プレースホルダーとして注釈されたフィールドを追跡します。
    """

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        cls = super().__new__(mcs, name, bases, namespace)

        # プレースホルダーフィールドを収集
        annotations = get_type_hints(cls, include_extras=True)
        placeholders = {}

        for field_name, field_type in annotations.items():
            # Annotatedフィールドを検索
            if get_origin(field_type) is Annotated:
                args = get_args(field_type)
                # Placeholderメタデータを持つフィールドを検索
                for arg in args[1:]:
                    if isinstance(arg, Placeholder) or (
                        isclass(arg) and issubclass(arg, Placeholder)
                    ):
                        placeholders[field_name] = args[0]  # 実際の型
                        break

        # プレースホルダー情報をクラスに保存
        setattr(cls, "__placeholders__", placeholders)
        return cls


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideLayout(metaclass=TpptSlideLayoutMeta):
    """スライドレイアウトのベースクラス"""

    __placeholders__: ClassVar[dict[str, Any]] = {}

    def __init__(self, **kwargs) -> None:
        # プレースホルダーフィールドの値を設定
        for field_name, field_value in kwargs.items():
            if field_name in self.__class__.__placeholders__:
                setattr(self, field_name, field_value)
            else:
                raise TypeError(
                    f"'{self.__class__.__name__}' got an unexpected keyword argument '{field_name}'"
                )


class MySlideLayout(TpptSlideLayout):
    title: Annotated[str, Placeholder]
    text: Annotated[str, Placeholder]


def get_placeholders(slide: type[TpptSlideLayout]) -> dict[str, Any]:
    """クラスのメタ情報を解析し、プレースホルダーのフィールドのキーバリューを取得する"""
    return slide.__placeholders__


# TODO: 以下のアサーションが通るようにせよ
Myslide: type[TpptSlideLayout] = MySlideLayout
myslide = Myslide(title="a", text="b")

assert get_placeholders(Myslide) == {"title": "a", "text": "b"}
