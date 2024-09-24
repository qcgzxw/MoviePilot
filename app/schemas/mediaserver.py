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

class MediaServerItemFilter(BaseModel):
    """
    筛选字段
    """
    # 父媒体库ID
    parent_id: Optional[str] = None
    # 媒体标题
    title: Optional[str] = None
    # 出版年份
    year: Optional[str] = None
    # 是否已播放
    is_played: Optional[bool] = None
    # 是否可以继续播放
    resume: Optional[bool] = None

    """
    分页 默认 每页100
    """
    # 起始页
    start_index: Optional[int] = 0
    # 页面大小 不建议超过100
    limit: Optional[int] = 100

    emby_params: Dict[str, str] = {}
    jellyfin_params: Dict[str, str] = {}
    plex_params: Dict[str, str] = {}


    def __init__(self, parent_id: Optional[str] = None, title: Optional[str] = None, year: Optional[str] = None,
                 is_played: Optional[bool] = None, resume: Optional[bool] = None, start_index: Optional[int] = 0,
                 limit: Optional[int] = 100, **data: Any):
        """
        构造函数用于初始化筛选器对象，并允许通过关键字参数设置筛选字段。

        :param parent_id: 可选，父媒体库ID
        :param title: 可选，媒体标题
        :param year: 可选，出版年份
        :param is_played: 可选，是否已播放
        :param resume: 可选，是否可以继续播放
        :param data: 其他父类传递的参数（通过 **data 传递）
        """
        # 调用父类的构造函数
        super().__init__(**data)

        # 初始化筛选字段
        self.parent_id = parent_id
        self.title = title
        self.year = year
        self.is_played = is_played
        self.resume = resume
        self.start_index = start_index
        self.limit = limit


    def set_page(self, start_index: int = 0, limit: int = 100):
        """
        设置分页，每次请求都需要手动设置分页起始和大小
        :param start_index: 起始页
        :param limit: 页面大小
        """
        self.start_index = start_index
        self.limit = limit
        return self


    def set_extra_params(self, extra: Dict[MediaServerType, Dict[str, str]]):
        """
        设置自定义参数
        :param extra: 额外参数，需要指定媒体服务类型，例如:
            set_extra_params({
                MediaServerType.EMBY: {'Fields': 'CommunityRating'},
                MediaServerType.JELLYFIN: {'Fields': 'CommunityRating'}
            })
        """
        for server, params in extra:
            if server == MediaServerType.Emby:
                self.emby_params = {**self.emby_params, **params}
            elif server == MediaServerType.Jellyfin:
                self.jellyfin_params = {**self.jellyfin_params, **params}
            elif server == MediaServerType.Plex:
                self.plex_params = {**self.plex_params, **params}
        return self

    def _build_params(self):
        """
        构建不同客户端的筛选参数
        """
        # Emby/Jellyfin参数构建
        self.emby_params = {
            "ParentId": self.parent_id,
            "Fields": "ProviderIds,OriginalTitle,ProductionYear,Path,UserDataPlayCount,UserDataLastPlayedDate,ParentId",
            "IsPlayed": self.is_played,
            "Recursive": self.resume,
            "Limit": self.limit,
            "StartIndex": self.start_index,
        }

        # Jellyfin参数构建（兼容Emby参数）
        self.jellyfin_params = {
            **self.emby_params,
        }

        # Plex参数构建
        self.plex_params = {
            "librarySectionID": int(self.parent_id),
            "title": None if self.title is None else self.title,
            "year": None if self.year is None else int(self.year),
            "unwatched": None if self.is_played is None else not self.is_played,
            "inProgress": None if self.resume is None else self.resume,
        }
        return self

    def _get_params(self, server: MediaServerType) -> Dict[str, str]:
        """
        获取指定媒体服务器参数
        """
        self._build_params()
        params = self.emby_params if server == MediaServerType.EMBY else \
            (self.jellyfin_params if server == MediaServerType.JELLYFIN else self.plex_params)
        return {k: v for k, v in params.items() if v is not None}

    def get_emby_params(self) -> (Dict[str, str]):
        """
        获取Emby搜索参数
        """
        return self._get_params(MediaServerType.EMBY)

    def get_jellyfin_params(self) -> (Dict[str, str]):
        """
        获取Jellyfin搜索参数
        """
        return self._get_params(MediaServerType.JELLYFIN)

    def get_plex_params(self) -> (Dict[str, str]):
        """
        获取Plex搜索参数
        """
        return self._get_params(MediaServerType.PLEX)
