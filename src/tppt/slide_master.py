from typing import TYPE_CHECKING, Annotated, TypeAlias, get_args, get_origin

from typing_extensions import TypeVar, dataclass_transform

from tppt.exception import (
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
)

from .slide_layout import (
    AnyType,
    DefaultBlankSlide,
    DefaultComparisonSlide,
    DefaultContentWithCaptionSlide,
    DefaultMasterSlide,
    DefaultPictureWithCaptionSlide,
    DefaultSectionHeaderSlide,
    DefaultTitleAndContentSlide,
    DefaultTitleAndVerticalTextSlide,
    DefaultTitleOnlySlide,
    DefaultTitleSlide,
    DefaultTwoContentSlide,
    DefaultVerticalTitleAndTextSlide,
    SlideLayout,
)


class _SlideMasterMeta(type):
    def __getattr__(self, key: str) -> "type[SlideLayout]":
        # 1. クラス自身の属性を確認
        if key in self.__dict__:
            value = self.__dict__[key]
            if isinstance(value, type) and issubclass(value, SlideLayout):
                return value

        # 2. アノテーションを確認
        if hasattr(self, "__annotations__") and key in self.__annotations__:
            annotation = self.__annotations__[key]

            # Annotated型からの抽出
            origin = get_origin(annotation)
            if origin is Annotated:
                args = get_args(annotation)
                if (
                    args
                    and isinstance(args[0], type)
                    and issubclass(args[0], SlideLayout)
                ):
                    return args[0]
                else:
                    raise SlideMasterAttributeMustBeSlideLayoutError(key)
            # クラスの場合は直接チェック
            elif isinstance(annotation, type) and issubclass(annotation, SlideLayout):
                return annotation
            else:
                raise SlideMasterAttributeMustBeSlideLayoutError(key)

        raise SlideMasterAttributeNotFoundError(key)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class SlideMaster(metaclass=_SlideMasterMeta): ...


if TYPE_CHECKING:
    Layout: TypeAlias = Annotated[AnyType, ...]
else:

    class Layout:
        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]


if TYPE_CHECKING:
    MasterLayout: TypeAlias = Annotated[AnyType, ...]
else:

    class MasterLayout(Layout):
        pass


class DefaultSlideMaster(SlideMaster):
    Master: MasterLayout[DefaultMasterSlide]
    Title: Layout[DefaultTitleSlide]
    TitleAndContent: Layout[DefaultTitleAndContentSlide]
    SectionHeader: Layout[DefaultSectionHeaderSlide]
    TwoContent: Layout[DefaultTwoContentSlide]
    Comparison: Layout[DefaultComparisonSlide]
    TitleOnly: Layout[DefaultTitleOnlySlide]
    Blank: Layout[DefaultBlankSlide]
    ContentWithCaption: Layout[DefaultContentWithCaptionSlide]
    PictureWithCaption: Layout[DefaultPictureWithCaptionSlide]
    TitleAndVerticalText: Layout[DefaultTitleAndVerticalTextSlide]
    VerticalTitleAndText: Layout[DefaultVerticalTitleAndTextSlide]


GenericTpptSlideMaster = TypeVar(
    "GenericTpptSlideMaster",
    bound=SlideMaster,
)
