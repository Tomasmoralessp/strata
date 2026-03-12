from application.bootstrap import ApplicationBootstrap


def main():
    bootstrap = ApplicationBootstrap()

    context = bootstrap.build_context()

    pipeline = bootstrap.build_pipeline(context)

    pipeline.run()


if __name__ == "__main__":
    main()
