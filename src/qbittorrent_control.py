import qbittorrentapi
from src.config import BOT_CONFIGS


def qbittorrent_login(func):
    def wrapper(*args, **kwargs):

        qbt_client = qbittorrentapi.Client(
            host=f'http://{BOT_CONFIGS.qbittorrent.ip.network_address}:'
                 f'{BOT_CONFIGS.qbittorrent.port}',
            username=BOT_CONFIGS.qbittorrent.user,
            password=BOT_CONFIGS.qbittorrent.password)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        resp = func(qbt_client, *args, **kwargs)

        qbt_client.auth_log_out()

        return resp

    return wrapper


@qbittorrent_login
def add_magnet(qbt_client, magnet_link: str, category: str = None) -> None:
    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(urls=magnet_link, category=cat)
    else:
        qbt_client.torrents_add(urls=magnet_link)


@qbittorrent_login
def add_torrent(qbt_client, file_name: str, category: str = None) -> None:
    cat = category
    if cat == "None":
        cat = None

    try:
        if category is not None:
            qbt_client.torrents_add(torrent_files=file_name, category=cat)
        else:
            qbt_client.torrents_add(torrent_files=file_name)

    except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
        pass


@qbittorrent_login
def resume_all(qbt_client) -> None:
    qbt_client.torrents.resume.all()


@qbittorrent_login
def pause_all(qbt_client) -> None:
    qbt_client.torrents.pause.all()


@qbittorrent_login
def resume(qbt_client, torrent_hash: str) -> None:
    qbt_client.torrents_resume(torrent_hashes=torrent_hash)


@qbittorrent_login
def pause(qbt_client, torrent_hash: str) -> None:
    qbt_client.torrents_pause(torrent_hashes=torrent_hash)


@qbittorrent_login
def delete_one_no_data(qbt_client, torrent_hash: str) -> None:
    qbt_client.torrents_delete(delete_files=False,
                               torrent_hashes=torrent_hash)


@qbittorrent_login
def delete_one_data(qbt_client, torrent_hash: str) -> None:
    qbt_client.torrents_delete(delete_files=True,
                               torrent_hashes=torrent_hash)


@qbittorrent_login
def delall_no_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=False, hashes=i.hash)


@qbittorrent_login
def delall_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, hashes=i.hash)


@qbittorrent_login
def get_categories(qbt_client):
    categories = qbt_client.torrent_categories.categories
    if len(categories) > 0:
        return categories

    else:
        return


@qbittorrent_login
def get_torrent_info(qbt_client, data: str = None, status_filter: str = None, ):
    if data is None:
        return qbt_client.torrents_info(status_filter=status_filter)
    return next(iter(qbt_client.torrents_info(status_filter=status_filter, torrent_hashes=data)), None)


@qbittorrent_login
def edit_category(qbt_client, name: str, save_path: str) -> None:
    qbt_client.torrents_edit_category(name=name,
                                      save_path=save_path)


@qbittorrent_login
def create_category(qbt_client, name: str, save_path: str) -> None:
    qbt_client.torrents_create_category(name=name,
                                        save_path=save_path)


@qbittorrent_login
def remove_category(qbt_client, data: str) -> None:
    qbt_client.torrents_remove_categories(categories=data)
