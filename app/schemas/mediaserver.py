from pathlib import Path
from typing import Optional, Dict, Union, List, Any

from pydantic import BaseModel
from app.schemas.types import MediaType, MediaServerType


class ExistMediaInfo(BaseModel):
    """
    媒体服务器存在媒体信息
    """
    # 类型 电影、电视剧
    type: Optional[MediaType]
    # 季
    seasons: Optional[Dict[int, list]] = {}
    # 媒体服务器
    server: Optional[str] = None
    # 媒体ID
    itemid: Optional[Union[str, int]] = None


class NotExistMediaInfo(BaseModel):
    """
    媒体服务器不存在媒体信息
    """
    # 季
    season: Optional[int] = None
    # 剧集列表
    episodes: Optional[list] = []
    # 总集数
    total_episode: Optional[int] = 0
    # 开始集
    start_episode: Optional[int] = 0


class RefreshMediaItem(BaseModel):
    """
    媒体库刷新信息
    """
    # 标题
    title: Optional[str] = None
    # 年份
    year: Optional[str] = None
    # 类型
    type: Optional[MediaType] = None
    # 类别
    category: Optional[str] = None
    # 目录
    target_path: Optional[Path] = None


class MediaServerLibrary(BaseModel):
    """
    媒体服务器媒体库信息
    """
    # 服务器名称
    server_name: Optional[str] = None
    # 服务器类型
    server: Optional[MediaServerType] = None
    # ID
    id: Optional[Union[str, int]] = None
    # 名称
    name: Optional[str] = None
    # 路径
    path: Optional[Union[str, list]] = None
    # 类型
    type: Optional[str] = None
    # 封面图
    image: Optional[str] = None
    # 封面图列表
    image_list: Optional[List[str]] = None
    # 跳转链接
    link: Optional[str] = None



class MediaServerItemUserState(BaseModel):
    # 已播放
    played: Optional[bool] = None
    # 继续播放
    resume: Optional[bool] = None
    # 上次播放时间 10位时间戳
    last_played_date: Optional[str] = None
    # 播放次数(不等于完播次数，理解为浏览次数)
    play_count: Optional[int] = None
    # 播放进度
    percentage: Optional[float] = None

class MediaServerItem(BaseModel):
    """
    媒体服务器媒体信息
    """
    # ID
    id: Optional[Union[str, int]] = None
    # 服务器名称
    server_name: Optional[str] = None
    # 服务器类型
    server: Optional[MediaServerType] = None
    # 媒体库ID
    library: Optional[Union[str, int]] = None
    # ID
    item_id: Optional[str] = None
    # 类型
    item_type: Optional[str] = None
    # 标题
    title: Optional[str] = None
    # 原标题
    original_title: Optional[str] = None
    # 年份
    year: Optional[str] = None
    # TMDBID
    tmdbid: Optional[int] = None
    # IMDBID
    imdbid: Optional[str] = None
    # TVDBID
    tvdbid: Optional[str] = None
    # 路径
    path: Optional[str] = None
    # 季集
    seasoninfo: Optional[Dict[int, list]] = None
    # 备注
    note: Optional[str] = None
    # 同步时间
    lst_mod_date: Optional[str] = None
    user_state: Optional[MediaServerItemUserState] = None

    class Config:
        orm_mode = True


class MediaServerSeasonInfo(BaseModel):
    """
    媒体服务器媒体剧集信息
    """
    season: Optional[int] = None
    episodes: Optional[List[int]] = []


class WebhookEventInfo(BaseModel):
    """
    Webhook事件信息
    """
    event: Optional[str] = None
    channel: Optional[MediaServerType] = None
    item_type: Optional[str] = None
    item_name: Optional[str] = None
    item_id: Optional[str] = None
    item_path: Optional[str] = None
    season_id: Optional[str] = None
    episode_id: Optional[str] = None
    tmdb_id: Optional[str] = None
    overview: Optional[str] = None
    percentage: Optional[float] = None
    ip: Optional[str] = None
    device_name: Optional[str] = None
    client: Optional[str] = None
    user_name: Optional[str] = None
    image_url: Optional[str] = None
    item_favorite: Optional[bool] = None
    save_reason: Optional[str] = None
    item_isvirtual: Optional[bool] = None
    media_type: Optional[str] = None


class MediaServerPlayItem(BaseModel):
    """
    媒体服务器可播放项目信息
    """
    id: Optional[Union[str, int]] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    type: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    percent: Optional[float] = None

class MediaServerItemFilter(MediaServerItem):
    """
    筛选字段
    """
    parent_id: Optional[str] = None
    item_id: Optional[str] = None
    title: Optional[str] = None
    year: Optional[str] = None
    item_type: Optional[list[str]] = None
    tmdbid: Optional[int] = None
    imdbid: Optional[str] = None
    tvdbid: Optional[str] = None
    played: Optional[bool] = None
    resume: Optional[bool] = None
    # 更多筛选项

    """
    排序类
    """
    sort_name: Optional[str] = None
    sort_order: Optional[bool] = None

    """
    分页
    """
    # 起始页
    start_index: Optional[int] = None
    # 页面大小 不建议超过100
    limit: Optional[int] = None

    _emby_params: Dict[str, str] = None
    _jellyfin_params: Dict[str, str] = None
    _plex_params: Dict[str, str] = None


    def set_extra_params(self, extra: Dict[str, Dict[str, str]]):
        """
        设置自定义参数

        :param extra: 额外参数，需要指定媒体服务类型，例如:
            set_extra_params({
                'emby': {'Fields': 'CommunityRating'},
                'jellyfin': {'Fields': 'CommunityRating'}
            })
        """
        for server, params in extra:
            if server == "emby":
                self._emby_params = {**self._emby_params, **params}
            elif server == "jellyfin":
                self._jellyfin_params = {**self._jellyfin_params, **params}
            elif server == "plex":
                self._plex_params = {**self._plex_params, **params}

    def get_emby_params(self) -> Dict[str, str]:
        """
        获取Emby搜索参数
        """
        return self._emby_params

    def get_jellyfin_params(self) -> Dict[str, str]:
        """
        获取Jellyfin搜索参数
        """
        return self._jellyfin_params

    def get_plex_params(self) -> Dict[str, str]:
        """
        获取Plex搜索参数
        """
        return self._plex_params
