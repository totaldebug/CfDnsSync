class Factory:
    def sync(self):
        from cfdnssync.sync import Sync

        config = self.config()

        return Sync(config)

    def run_config(self):
        from cfdnssync.config import RunConfig

        config = RunConfig()

        return config


    def logging(self):
        import logging

        from cfdnssync.logging import initialize

        config = self.config()
        initialize(config)

        return logging

    def logger(self):
        logger = self.logging().getLogger("CfDnsSync")
        config = self.config()

        from cfdnssync.logger.filter import LoggerFilter
        logger.addFilter(LoggerFilter(config["logging"]["filter"], logger))

        return logger

    def console_logger(self):
        from rich.logging import RichHandler

        from cfdnssync.console import console
        from cfdnssync.rich_addons import RichHighlighter

        config = self.config()
        return RichHandler(console=console, show_time=config.log_console_time, log_time_format='[%Y-%m-%d %X]', show_path=False, highlighter=RichHighlighter(),)

    def config(self):
        from cfdnssync.config import Config

        return Config()

factory = Factory()
logger = factory.logger()
logging = factory.logging()
