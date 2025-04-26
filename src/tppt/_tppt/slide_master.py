from typing import ClassVar, TypeVar

from typing_extensions import dataclass_transform

from tppt.exception import (
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
)

from .slide_layout import TpptSlideLayout


class TpptSlideMasterMeta(type):
    def __getattr__(self, key: str) -> "type[TpptSlideLayout]":
        if key in self.__annotations__:
            annotation = self.__annotations__[key]
            if issubclass(annotation, TpptSlideLayout):
                return annotation
            else:
                raise SlideMasterAttributeMustBeSlideLayoutError(key)

        raise SlideMasterAttributeNotFoundError(key)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideMaster(metaclass=TpptSlideMasterMeta):
    _template_path: ClassVar[str | None] = None

    @classmethod
    def get_template_path(cls) -> str | None:
        return cls._template_path


GenericTpptSlideMaster = TypeVar("GenericTpptSlideMaster", bound=TpptSlideMaster)
