import uvicorn


def init_debug_fastapi_application(app_str: str,
                                   host: str,
                                   port: int,
                                   reload: bool = False,
                                   reload_delay: float = 0.25):
    uvicorn.run(app_str, host=host, port=port, log_level="debug",
                reload=reload, reload_delay=reload_delay)


init_debug_fastapi_application(
    app_str="app.api.public.main:app",
    host="0.0.0.0",
    port=8001,
)
