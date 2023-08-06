# coding=utf-8
"""
Main entry point
"""

import asyncio
import queue

import click

from esst import __version__
from esst.core import CFG, CTX, MAIN_LOGGER

MAIN_LOGGER.debug(f'Starting ESST version {__version__}')


async def watch_for_exceptions():
    """
    Dummy loop to wake up asyncio event loop from time to time
    """
    while True:
        if CTX.exit:
            break
        await asyncio.sleep(0.1)


def _main(  # pylint: disable=too-many-locals,too-many-arguments
        discord: bool,
        server: bool,
        dcs: bool,
        listener: bool,
        start_dcs: bool,
        install_hooks: bool,
        install_dedi_config: bool,
        auto_mission: bool,
):
    """
    Main entry point

    Args:
        install_dedi_config: setup DCS to run in dedicated mode
        install_hooks: install GameGUI hooks
        dcs: start dcs loop
        discord: start Discord bot loop
        server: start server loop
        listener: start the listener loop
        start_dcs: start the server thread, but not the actual DCS app
        auto_mission: downloads the latest mission from Github
    """

    if CFG.sentry_dsn:
        from esst.utils.sentry import Sentry
        CTX.sentry = Sentry(CFG.sentry_dsn)
        CTX.sentry.register_context('App context', CTX)
        CTX.sentry.register_context('Config', CFG)

    CTX.loop = asyncio.get_event_loop()

    def _handler(_, context):
        MAIN_LOGGER.error(f'error in event loop: {context["message"]}')

    # CTX.loop.set_exception_handler(_handler)

    from esst.utils.conn import monitor_connection, wan_available
    CTX.wan = CTX.loop.run_until_complete(wan_available())
    CTX.loop.create_task(monitor_connection())

    CTX.start_discord_loop = discord and CFG.start_discord_loop
    CTX.start_server_loop = server and CFG.start_server_loop
    CTX.start_dcs_loop = dcs and CFG.start_dcs_loop
    CTX.start_listener_loop = listener and CFG.start_listener_loop

    CTX.dcs_can_start = start_dcs
    CTX.dcs_setup_dedi_config = install_dedi_config
    CTX.dcs_install_hooks = install_hooks
    CTX.dcs_auto_mission = auto_mission

    CTX.loop = asyncio.get_event_loop()
    # CTX.loop.set_debug(True)
    CTX.discord_msg_queue = queue.Queue()

    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(
        f'ESST v{__version__} - Use CTRL+C to exit')
    MAIN_LOGGER.debug(f'starting ESST {__version__}')

    from esst.utils import clean_all_folder
    clean_all_folder()

    import esst.discord_bot.discord_bot
    discord_loop = esst.discord_bot.discord_bot.App()

    import esst.dcs.dcs
    dcs_loop = esst.dcs.dcs.App()

    import esst.server.server
    server_loop = esst.server.server.App()

    from esst.listener import DCSListener
    try:
        listener_loop = DCSListener()
    except OSError as exc:
        if exc.errno == 10048:
            MAIN_LOGGER.error(
                'cannot bind socket, maybe another instance of ESST is already running?')
            exit(-1)
    else:

        futures = asyncio.gather(
            CTX.loop.create_task(discord_loop.run()),
            CTX.loop.create_task(dcs_loop.run()),
            CTX.loop.create_task(listener_loop.run()),
            CTX.loop.create_task(server_loop.run()),
            CTX.loop.create_task(watch_for_exceptions()),
        )

        def sigint_handler(*_):
            """
            Catches exit signal (triggered byu CTRL+C)

            Args:
                *_: frame

            """
            MAIN_LOGGER.info(
                'ESST has been interrupted by user request, shutting down')
            CTX.exit = True

        import signal
        signal.signal(signal.SIGINT, sigint_handler)
        CTX.loop.run_until_complete(futures)
        MAIN_LOGGER.debug('main loop is done, killing DCS')

        futures = asyncio.gather(
            CTX.loop.create_task(dcs_loop.kill_running_app()),
            CTX.loop.create_task(listener_loop.run_until_dcs_is_closed()),
        )

        CTX.loop.run_until_complete(futures)
        MAIN_LOGGER.debug('all done !')


@click.group(invoke_without_command=True)  # noqa: C901
@click.option('--callgraph', default=False, help='Run ESST with pycallgraph', show_default=True, is_flag=True)
@click.option('--discord/--no-discord', default=True, help='Starts the Discord bot loop', show_default=True)
@click.option('--server/--no-server', default=True, help='Starts the server monitoring loop', show_default=True)
@click.option('--dcs/--no-dcs', default=True, help='Starts the DCS app loop', show_default=True)
@click.option('--listener/--no-listener', default=True, help='Starts the socket loop', show_default=True)
@click.option('--start-dcs/--no-start-dcs', help='Spawn DCS.exe process', default=True, show_default=True)
@click.option('--install-hooks/--no-install-hooks', help='Install GameGUI hooks', default=True, show_default=True)
@click.option('--install-dedi-config/--no-install-dedi-config', help='Setup DCS to run in dedicated mode', default=True,
              show_default=True)
@click.option('--auto-mission/--no-auto-mission', help='Download latest mission', default=True, show_default=True)
def main(  # pylint: disable=too-many-locals,too-many-arguments
        discord: bool,
        server: bool,
        dcs: bool,
        listener: bool,
        start_dcs: bool,
        install_hooks: bool,
        install_dedi_config: bool,
        auto_mission: bool,
        callgraph: bool,):
    """Dummy entry point added to allow for callgraph context"""
    if callgraph:
        try:
            from pycallgraph.output import GraphvizOutput
            from pycallgraph import PyCallGraph, Config, GlobbingFilter
        except ImportError:
            raise RuntimeError('Please install pycallgraph first')

        trace_output = GraphvizOutput()
        trace_output.output_file = 'trace.png'
        trace_config = Config(max_depth=20)

        trace_config.trace_filter = GlobbingFilter(exclude=[
            'pycallgraph.*',
            'importlib.*',
        ])
        with PyCallGraph(output=trace_output, config=trace_config):
            _main(
                discord=discord,
                server=server,
                dcs=dcs,
                listener=listener,
                start_dcs=start_dcs,
                install_hooks=install_hooks,
                install_dedi_config=install_dedi_config,
                auto_mission=auto_mission,
            )
    else:
        _main(
            discord=discord,
            server=server,
            dcs=dcs,
            listener=listener,
            start_dcs=start_dcs,
            install_hooks=install_hooks,
            install_dedi_config=install_dedi_config,
            auto_mission=auto_mission,
        )


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
