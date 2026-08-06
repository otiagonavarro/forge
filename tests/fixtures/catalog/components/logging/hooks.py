def after_install(context) -> None:
    marker = context.destination / ".logging_hook_ran"
    marker.write_text("ok")
