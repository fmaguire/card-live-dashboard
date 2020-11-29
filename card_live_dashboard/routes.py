from pathlib import Path

import flask

from card_live_dashboard.service.CardLiveDataManager import CardLiveDataManager


def create_flask_routes(flask_app: flask.app.Flask, base_pathname: str, card_live_data_dir: Path) -> None:
    """
    Creates flask routes outside of Dash application. Mainly used to provided a route to
    download all data.
    :param flask_app: The Flask application.
    :param base_pathname: The base path the application is running under.
    :param card_live_data_dir: The data directory containing CARD:Live data.
    :return: Returns nothing.
    """
    if base_pathname is None:
        base_pathname = '/'
    elif not base_pathname.startswith('/'):
        base_pathname = '/' + base_pathname

    if base_pathname.endswith('/'):
        base_pathname = base_pathname.rstrip('/')

    @flask_app.route(f'{base_pathname}/data/current')
    def download_data():
        flask_app.logger.info(f'Request to download all data from [{card_live_data_dir}]')
        archive = CardLiveDataManager.get_instance().data_archive()
        return flask.send_file(archive, attachment_filename='card-live-data.zip', as_attachment=True)
