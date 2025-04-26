from inspect import isclass
from typing import Annotated, Any, ClassVar, TypeVar, get_type_hints

from typing_extensions import dataclass_transform, get_args, get_origin

T = TypeVar("T")
AnyType = TypeVar("AnyType")


# 型チェック用のクラス定義
class _Placeholder:
    """プレースホルダーを表すクラス。

    Annotatedと共に使用して、フィールドがプレースホルダーであることを示します。
    または、Placeholder[型]として直接使用することもできます。
    """

    def __init__(self, description: str = ""):
        self.description = description
        self.value = None

    def __repr__(self) -> str:
        return f"Placeholder({self.description!r})"

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        return Annotated[item, cls()]


Placeholder = Annotated[AnyType, _Placeholder]


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
                # メタデータのチェック
                metadata_args = args[1:]

                # Placeholderとして直接マークされたフィールドを検索
                if any(
                    arg is _Placeholder
                    or (isclass(arg) and arg.__name__ == "_Placeholder")
                    for arg in metadata_args
                ):
                    placeholders[field_name] = args[0]  # 実際の型
                    continue

                # ネストされたAnnotatedのチェック (Placeholder[T]パターン)
                # Placeholder[T] = Annotated[T, _Placeholder]のパターンを検出
                base_type = args[0]
                if get_origin(base_type) is Annotated:
                    nested_args = get_args(base_type)
                    if any(
                        arg is _Placeholder
                        or (isclass(arg) and arg.__name__ == "_Placeholder")
                        for arg in nested_args[1:]
                    ):
                        placeholders[field_name] = nested_args[0]  # 実際の型
                        continue

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
            if field_name in self.__class__.__placeholders__:
                # プレースホルダーフィールドの場合
                setattr(self, field_name, field_value)
            elif field_name in self.__class__.__annotations__:
                setattr(self, field_name, field_value)
            else:
                raise TypeError(
                    f"'{self.__class__.__name__}' got an unexpected keyword argument '{field_name}'"
                )


class MySlideLayout(TpptSlideLayout):
    title: Annotated[str, _Placeholder]  # 直接_Placeholderを使用
    dummy: str
    text: Annotated[str, _Placeholder]


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


# Placeholder[T]形式での使用方法
class MySlideLayout2(TpptSlideLayout):
    title: Placeholder[str]  # Annotated[str, _Placeholder]に展開される
    dummy: str
    text: Placeholder[str]


myslide2 = MySlideLayout2(title="a", dummy="dummy", text="b")
myslide2.dummy = "dummy2"
assert get_placeholders(myslide2) == {"title": "a", "text": "b"}
