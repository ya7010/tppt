from typing import Any, ClassVar, Self, Type, TypeVar, overload

from typing_extensions import dataclass_transform


class TpptSlideMasterMeta(type):
    """TpptSlideMasterのメタクラス"""

    def __getattr__(self, key: str) -> "type[TpptSlideLayout]":
        if key in self.__annotations__:
            annotation = self.__annotations__[key]
            if issubclass(annotation, TpptSlideLayout):
                return annotation
            else:
                raise AttributeError(f"属性 {key} は {annotation} ではありません")

        raise AttributeError(f"属性 {key} は存在しません")


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideMaster(metaclass=TpptSlideMasterMeta):
    """スライドマスターのベースクラス"""

    _template_path: ClassVar[str | None] = None

    @classmethod
    def get_template_path(cls) -> str | None:
        """
        テンプレートパスを取得する
        """
        return cls._template_path


class TpptSlideLayout:
    """スライドレイアウトのベースクラス"""

    @overload
    def __get__(self, instance: None, objtype: type[Any]) -> type[Self]: ...

    @overload
    def __get__(self, instance: object, objtype: type[Any]) -> Self: ...

    def __get__(self, instance: object | None, objtype: type[Any]) -> type[Self] | Self:
        if instance is None:
            return type(self)

        else:
            return self


# 型変数を調整
TpptSlideMasterType = TypeVar("TpptSlideMasterType", bound=Type[TpptSlideMaster])
TpptSlideLayoutType = TypeVar("TpptSlideLayoutType", bound=Type[TpptSlideLayout])


class MyMasterSlide(TpptSlideLayout):
    def __init__(self, a: int, b: str): ...


class MyTitleSlide(TpptSlideLayout): ...


class MyContentSlide(TpptSlideLayout): ...


class MySlideMaster(TpptSlideMaster):
    master: MyMasterSlide
    title: MyTitleSlide
    totle_and_content: MyContentSlide


# 以下のアサーションが通るようにせよ
master: type[TpptSlideMaster] = MySlideMaster
assert MySlideMaster.master == MyMasterSlide
assert MySlideMaster.title == MyTitleSlide
assert MySlideMaster.totle_and_content == MyContentSlide
MySlideMaster.master(a=1, b="a")
