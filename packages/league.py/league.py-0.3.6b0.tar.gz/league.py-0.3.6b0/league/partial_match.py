from league.riotDTO import RiotDto
from league.enums import for_id
import datetime


class PartialMatch(RiotDto):
    """
    Represents a partial match data.

    Attributes
    ----------
    lane: str
        Represents the lane that was played as.
    match_id : int
        The ID of the match, can be used to lookup the full details of the match.
    champion: :class:`Champion`
        The champion played.
    platform : str
        The regional platform the match was conducted on.
    season : int
        The ID of the season the match belongs to.
    queue : :class:`Queue`
        The queue type of the match.
    role : str
        The role of the docs.
    date : datetime.datetime
        UTC datetime of the match

    """

    def __init__(self, **kwargs):
        super(PartialMatch, self).__init__(**kwargs)
        self.lane = kwargs.get('lane')
        self.match_id = kwargs.get('gameId')
        self.champion = self._get_from_cache("champions", kwargs.get('champion'))
        self.platform = kwargs.get('platformId')
        self.season = kwargs.get('season')
        self.queue = for_id(kwargs.get('queue'))
        self.role = kwargs.get('role')
        if kwargs.get('timestamp'):
            self.date = datetime.datetime.utcfromtimestamp((kwargs.get('timestamp') / 1000)).replace(
                tzinfo=datetime.timezone.utc)
        else:
            self.date = kwargs.get('timestamp')
