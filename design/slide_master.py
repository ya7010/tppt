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
        # すべてのフィールドに値を設定
        for field_name, field_value in kwargs.items():
            if field_name in self.__class__.__annotations__:
                setattr(self, field_name, field_value)
            else:
                raise TypeError(
                    f"'{self.__class__.__name__}' got an unexpected keyword argument '{field_name}'"
                )


class MySlideLayout(TpptSlideLayout):
    title: Annotated[str, Placeholder]
    dummy: str
    text: Annotated[str, Placeholder]


def get_placeholders(
    slide_or_class: type[TpptSlideLayout] | TpptSlideLayout,
) -> dict[str, Any]:
    """クラスのメタ情報を解析し、プレースホルダーのフィールドのキーバリューを取得する

    引数にインスタンスが渡された場合は、実際のプレースホルダー値を返す
    クラスが渡された場合は、プレースホルダーの型情報を返す
    """
    if isinstance(slide_or_class, type):
        # クラスが渡された場合は型情報を返す
        return slide_or_class.__placeholders__
    else:
        # インスタンスの場合は実際の値を返す
        values = {}
        for field_name in slide_or_class.__class__.__placeholders__:
            if hasattr(slide_or_class, field_name):
                values[field_name] = getattr(slide_or_class, field_name)
        return values


# TODO: 以下のアサーションが通るようにせよ
Myslide: type[TpptSlideLayout] = MySlideLayout
myslide = MySlideLayout(title="a", text="b", dummy="dummy")

assert myslide.title == "a"
assert myslide.dummy == "dummy"
assert myslide.text == "b"
assert get_placeholders(myslide) == {"title": "a", "text": "b"}

