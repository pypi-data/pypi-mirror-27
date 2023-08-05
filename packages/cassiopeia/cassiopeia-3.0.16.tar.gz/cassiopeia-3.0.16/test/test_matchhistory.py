import pytest
import datetime


import cassiopeia as cass
from cassiopeia import Season, Queue, Summoner


def test_match_history_1():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives})
    assert len(match_history) > 400


def test_match_history_2():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime.utcnow()-datetime.timedelta(days=140), end_time=datetime.datetime.utcnow())
    assert len(match_history) > 0


def test_match_history_3():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime(2017, 2, 7), end_time=datetime.datetime(2017, 2, 14))
    assert len(match_history) > 0


def test_match_history_4():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime(2016, 1, 1), end_time=datetime.datetime(2016, 1, 11))
    assert len(match_history) == 0


def test_match_history_5():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime(2016, 1, 1), end_time=datetime.datetime.utcnow())
    assert len(match_history) > 0


def test_match_history_6():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime(2016, 12, 1), end_time=datetime.datetime(2016, 12, 30))
    assert len(match_history) > 0


def test_match_history_7():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, region=region, seasons={Season.season_7}, queues={Queue.ranked_solo_fives}, begin_time=datetime.datetime(2016, 12, 1))
    assert len(match_history) > 0
