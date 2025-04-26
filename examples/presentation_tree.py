"""Sample script to output the presentation tree structure."""

import json

import tppt


def main() -> None:
    presentation = (
        tppt.Presentation.builder()
        .slide(
            tppt.SlideBuilder().text(
                "Hello, world!",
                left=(100, "pt"),
                top=(100, "pt"),
                width=(100, "pt"),
                height=(100, "pt"),
            )
        )
        .build()
    )

    # Get and display the tree structure
    print(
        json.dumps(
            presentation.tree,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
