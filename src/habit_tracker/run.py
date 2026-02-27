import uvicorn
from habit_tracker.config import settings
from habit_tracker.main import create_app


def main(reload: bool):
    app = create_app()

    uvicorn.run(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload_dirs=["src/"],
    )

if __name__ == "__main__":
    main(reload=False)
