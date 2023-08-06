# coding=utf-8
"""
Tests for Mission objects
"""
import os
from pathlib import Path
from time import sleep
from zipfile import BadZipFile

import pytest
from hypothesis import strategies as st
from hypothesis import given, settings

from emiz.mission import BaseUnit, Coalition, Country, FlyingUnit, Group, Mission
from emiz.miz import ENCODING, Miz

if os.path.exists('./test_files'):
    BASE_PATH = os.path.abspath('./test_files')
elif os.path.exists('./test/test_files'):
    BASE_PATH = os.path.abspath('./test/test_files')
else:
    raise RuntimeError('cannot find test files')

TEST_FILE = os.path.join(BASE_PATH, 'TRG_KA50.miz')
OUT_FILE = os.path.join(BASE_PATH, 'TRG_KA50_EMFT.miz')
BAD_ZIP_FILE = os.path.join(BASE_PATH, 'bad_zip_file.miz')
MISSING_FILE = os.path.join(BASE_PATH, 'missing_files.miz')
DUPLICATE_GROUP_ID = os.path.join(BASE_PATH, 'duplicate_group_id.miz')
ALL_OBJECTS = os.path.join(BASE_PATH, 'all_objects.miz')
LARGE_FILE = os.path.join(BASE_PATH, 'TRMT_2.4.0.miz')
RADIO_FILE = os.path.join(BASE_PATH, 'radios.miz')
BAD_FILES = ['bad_zip_file.miz', 'missing_files.miz']

RADIOS_TESTS = [
    (
        1, 'F-86F Sabre',
        [
            ('ARC-27', 1, {
                1: 225.0, 2: 225.0, 3: 399.9, 4: 270.2, 5: 255.0, 6: 259.0, 7: 262.0, 8: 257.0, 9: 253.2, 10: 263.0,
                11: 267.0, 12: 254.0, 13: 264.0, 14: 266.0, 15: 265.0, 16: 252.0, 17: 268.0, 18: 269.0},),
            ('ARC-27', 1, {
                1: 225.0, 2: 225.0, 3: 399.9, 4: 270.2, 5: 255.0, 6: 259.0, 7: 262.0, 8: 257.0, 9: 253.2, 10: 263.0,
                11: 267.0, 12: 254.0, 13: 264.0, 14: 266.0, 15: 265.0, 16: 252.0, 17: 268.0, 18: 269.0},),
        ]
    ),
    (
        2, 'M-2000C',
        [
            ('UHF', 1, {
                1: 225.0, 2: 400.0, 3: 225.0, 4: 256.3, 5: 254.0, 6: 250.0, 7: 270.0, 8: 257.0, 9: 255.0, 10: 262.0,
                11: 259.0, 12: 268.0, 13: 269.0, 14: 260.0, 15: 263.0, 16: 261.0, 17: 267.0, 18: 251.0, 19: 253.0,
                20: 266.0},),
            ('V/UHF', 2, {
                1: 129.2, 2: 118.0, 3: 400.0, 4: 127.0, 5: 125.0, 6: 121.0, 7: 141.0, 8: 128.0, 9: 126.0, 10: 133.0,
                11: 130.0, 12: 139.0, 13: 140.0, 14: 131.0, 15: 134.0, 16: 132.0, 17: 138.0, 18: 122.0, 19: 124.0,
                20: 137.0},),
        ]
    ),
    (
        3, 'MiG-21Bis',
        [
            ('R-832', 1, {
                1: 120.0, 2: 80.0, 3: 399.9, 4: 121.25, 5: 125.222, 6: 126.0, 7: 130.0, 8: 133.0, 9: 122.0, 10: 124.0,
                11: 134.0, 12: 125.0, 13: 135.0, 14: 137.0, 15: 136.0, 16: 123.0, 17: 132.0, 18: 127.0, 19: 129.0,
                20: 138.0},),
        ]
    ),
    (
        4, 'P-51D',
        [
            ('SCR552', 1, {1: 124.0, 2: 100.0, 3: 156.0, 4: 139.0},),
        ]
    ),
    (
        5, 'TF-51D',
        [
            ('SCR552', 1, {1: 124.0, 2: 124.0, 3: 131.0, 4: 139.0},),
        ]
    ),
    (
        6, 'Ka-50',
        [
            ('R828', 1, {
                1: 21.5, 2: 20.0, 3: 59.9, 4: 28.0, 5: 30.0, 6: 32.0, 7: 40.0, 8: 50.0, 9: 55.5, 10: 59.9},),
            ('ARK22', 2, {
                1: 0.625, 2: 0.15, 3: 1.75, 4: 0.591, 5: 0.408, 6: 0.803, 7: 0.443, 8: 0.215, 9: 0.525, 10: 1.065,
                11: 0.718, 12: 0.35, 13: 0.583, 14: 0.283, 15: 0.995, 16: 1.21},),
        ]
    ),
    (
        7, 'Mi-8MT',
        [
            ('R863', 1, {
                1: 127.5, 2: 100.0, 3: 399.9, 4: 127.0, 5: 125.0, 6: 121.0, 7: 141.0, 8: 128.0, 9: 126.0, 10: 133.0,
                11: 130.0, 12: 129.0, 13: 123.0, 14: 131.0, 15: 134.0, 16: 132.0, 17: 138.0, 18: 122.0, 19: 124.0,
                20: 137.0},),
            ('R828', 2, {
                1: 21.5, 2: 20.0, 3: 59.9, 4: 28.0, 5: 30.0, 6: 32.0, 7: 40.0, 8: 50.0, 9: 55.5, 10: 59.9},),
        ]
    ),
    (
        8, 'UH-1H',
        [
            ('ARC51', 1, {
                1: 251.0, 2: 225.0, 3: 399.975, 4: 256.0, 5: 254.0, 6: 250.0, 7: 270.0, 8: 257.0, 9: 255.0, 10: 262.0,
                11: 259.0, 12: 268.0, 13: 269.0, 14: 260.0, 15: 263.0, 16: 261.0, 17: 267.0, 18: 251.0, 19: 253.0,
                20: 266.0},),
        ]
    ),
]

with Miz(TEST_FILE) as miz:
    DUMMY_MISSION = miz.mission


# noinspection PyPep8Naming,PyShadowingNames
# @pytest.mark.nocleandir
class TestMizBasics:
    @pytest.fixture(autouse=True)
    def clean_up(self):
        yield
        if os.path.exists(OUT_FILE):
            os.remove(OUT_FILE)

    def test_init(self):
        Miz(TEST_FILE)
        with pytest.raises(FileNotFoundError):
            Miz('./i_do_not_exist')

    def test_context(self):
        with Miz(TEST_FILE) as miz:
            assert isinstance(miz.mission, Mission)
            assert isinstance(miz.l10n, dict)
            assert miz.zip_content

    def test_unzip(self):
        miz = Miz(TEST_FILE)
        miz.unzip()

    def test_decode(self):
        miz = Miz(TEST_FILE)
        miz.unzip()
        miz._decode()

    @pytest.mark.long
    def test_large_decode(self):
        miz = Miz(LARGE_FILE)
        miz.unzip()
        miz._decode()

    def test_zip(self):
        assert not Path(OUT_FILE).exists()
        with Miz(TEST_FILE) as miz:
            miz.zip(OUT_FILE)
        assert Path(OUT_FILE).exists()
        with Miz(OUT_FILE) as miz2:
            assert miz.mission.d == miz2.mission.d
            miz.mission.weather.cloud_density = 4
            assert not miz.mission.d == miz2.mission.d

    @pytest.mark.long
    def test_large_zip(self):
        with Miz(LARGE_FILE, keep_temp_dir=True) as miz:
            out_file = miz.zip()
        assert Path(out_file).exists()
        with Miz(out_file) as miz2:
            assert miz.mission.d == miz2.mission.d
            miz.mission.weather.cloud_density = 4
            assert not miz.mission.d == miz2.mission.d
            sleep(1)
            m1 = miz.mission_file
            m2 = miz2.mission_file
            with open(m1, encoding=ENCODING) as _f:
                t1 = _f.read()
            with open(m2, encoding=ENCODING) as _f:
                t2 = _f.read()
            assert t1 == t2

    def test_is_unzipped(self):
        mis = Miz(TEST_FILE)
        assert not mis.zip_content
        mis.unzip()
        assert mis.zip_content

    def test_missing_file_in_miz(self):
        missing = Miz(MISSING_FILE)
        with pytest.raises(FileNotFoundError):
            missing.unzip()

    def test_bad_zip_file(self):
        mis = Miz(BAD_ZIP_FILE)
        with pytest.raises(BadZipFile):
            mis.unzip()

    def test_temp_dir_cleaning(self):
        mis = Miz(TEST_FILE)
        mis.unzip()
        assert os.path.exists(mis.temp_dir)
        assert os.listdir(mis.temp_dir)
        mis._remove_temp_dir()
        assert not os.path.exists(mis.temp_dir)


# noinspection PyPep8Naming,PyShadowingNames
class TestMizValues:
    @pytest.fixture()
    def mission(self):
        yield Mission(dict(DUMMY_MISSION.d), dict(DUMMY_MISSION.l10n))
        # with Miz(TEST_FILE, keep_temp_dir=True) as miz:
        #     yield miz

    @pytest.fixture(autouse=True)
    def clean_up(self):

        success = yield

        if success:
            try:
                os.remove(OUT_FILE)
            except FileNotFoundError:
                pass

    def test_bullseye(self, mission):
        assert (11557, 371700) == mission.red_coa.bullseye_position
        assert (-291014, 617414) == mission.blue_coa.bullseye_position

    def test_ln10(self, mission):
        assert mission.l10n == dict(
            [('DictKey_GroupName_5', 'etcher'), ('DictKey_GroupName_8', 'gal'), ('DictKey_GroupName_11', 'gilles'),
             ('DictKey_GroupName_14', 'New Vehicle Group'), ('DictKey_GroupName_17', 'New Vehicle Group #001'),
             ('DictKey_GroupName_20', 'New Vehicle Group #002'), ('DictKey_GroupName_23', 'New Vehicle Group #003'),
             ('DictKey_GroupName_26', 'New Vehicle Group #004'), ('DictKey_GroupName_29', 'New Vehicle Group #005'),
             ('DictKey_GroupName_32', 'New Vehicle Group #006'), ('DictKey_GroupName_35', 'New Vehicle Group #007'),
             ('DictKey_GroupName_38', 'New Vehicle Group #008'), ('DictKey_GroupName_41', 'New Vehicle Group #009'),
             ('DictKey_GroupName_44', 'New Vehicle Group #010'), ('DictKey_GroupName_47', 'New Vehicle Group #011'),
             ('DictKey_GroupName_50', 'New Vehicle Group #012'), ('DictKey_GroupName_53', 'New Vehicle Group #013'),
             ('DictKey_GroupName_56', 'New Vehicle Group #014'), ('DictKey_GroupName_59', 'New Vehicle Group #015'),
             ('DictKey_GroupName_62', 'New Vehicle Group #016'), ('DictKey_GroupName_65', 'New Vehicle Group #017'),
             ('DictKey_GroupName_68', 'New Vehicle Group #018'), ('DictKey_GroupName_71', 'New Vehicle Group #019'),
             ('DictKey_GroupName_74', 'New Vehicle Group #020'), ('DictKey_GroupName_77', 'New Vehicle Group #021'),
             ('DictKey_GroupName_80', 'New Vehicle Group #022'), ('DictKey_GroupName_83', 'New Vehicle Group #023'),
             ('DictKey_GroupName_86', 'New Vehicle Group #024'), ('DictKey_GroupName_89', 'New Vehicle Group #025'),
             ('DictKey_GroupName_92', 'New Vehicle Group #026'), ('DictKey_GroupName_95', 'New Vehicle Group #027'),
             ('DictKey_GroupName_98', 'New Vehicle Group #028'), ('DictKey_GroupName_101', 'New Vehicle Group #029'),
             ('DictKey_GroupName_104', 'New Vehicle Group #030'), ('DictKey_GroupName_107', 'New Vehicle Group #031'),
             ('DictKey_GroupName_110', 'New Vehicle Group #032'), ('DictKey_UnitName_6', 'etcher'),
             ('DictKey_UnitName_9', 'gal'), ('DictKey_UnitName_12', 'gilles'), ('DictKey_UnitName_15', 'Unit #1'),
             ('DictKey_UnitName_18', 'Unit #001'), ('DictKey_UnitName_21', 'Unit #002'),
             ('DictKey_UnitName_24', 'Unit #003'), ('DictKey_UnitName_27', 'Unit #004'),
             ('DictKey_UnitName_30', 'Unit #005'), ('DictKey_UnitName_33', 'Unit #006'),
             ('DictKey_UnitName_36', 'Unit #007'), ('DictKey_UnitName_39', 'Unit #008'),
             ('DictKey_UnitName_42', 'Unit #009'), ('DictKey_UnitName_45', 'Unit #010'),
             ('DictKey_UnitName_48', 'Unit #011'), ('DictKey_UnitName_51', 'Unit #012'),
             ('DictKey_UnitName_54', 'Unit #013'), ('DictKey_UnitName_57', 'Unit #014'),
             ('DictKey_UnitName_60', 'Unit #015'), ('DictKey_UnitName_63', 'Unit #016'),
             ('DictKey_UnitName_66', 'Unit #017'), ('DictKey_UnitName_69', 'Unit #018'),
             ('DictKey_UnitName_72', 'Unit #019'), ('DictKey_UnitName_75', 'Unit #020'),
             ('DictKey_UnitName_78', 'Unit #021'), ('DictKey_UnitName_81', 'Unit #022'),
             ('DictKey_UnitName_84', 'Unit #023'), ('DictKey_UnitName_87', 'Unit #024'),
             ('DictKey_UnitName_90', 'Unit #025'), ('DictKey_UnitName_93', 'Unit #026'),
             ('DictKey_UnitName_96', 'Unit #027'), ('DictKey_UnitName_99', 'Unit #028'),
             ('DictKey_UnitName_102', 'Unit #029'), ('DictKey_UnitName_105', 'Unit #030'),
             ('DictKey_UnitName_108', 'Unit #031'), ('DictKey_UnitName_111', 'Unit #032'), ('DictKey_WptName_7', ''),
             ('DictKey_WptName_10', ''), ('DictKey_WptName_13', ''), ('DictKey_WptName_16', ''),
             ('DictKey_WptName_19', ''), ('DictKey_WptName_22', ''), ('DictKey_WptName_25', ''),
             ('DictKey_WptName_28', ''), ('DictKey_WptName_31', ''), ('DictKey_WptName_34', ''),
             ('DictKey_WptName_37', ''), ('DictKey_WptName_40', ''), ('DictKey_WptName_43', ''),
             ('DictKey_WptName_46', ''), ('DictKey_WptName_49', ''), ('DictKey_WptName_52', ''),
             ('DictKey_WptName_55', ''), ('DictKey_WptName_58', ''), ('DictKey_WptName_61', ''),
             ('DictKey_WptName_64', ''), ('DictKey_WptName_67', ''), ('DictKey_WptName_70', ''),
             ('DictKey_WptName_73', ''), ('DictKey_WptName_76', ''), ('DictKey_WptName_79', ''),
             ('DictKey_WptName_82', ''), ('DictKey_WptName_85', ''), ('DictKey_WptName_88', ''),
             ('DictKey_WptName_91', ''), ('DictKey_WptName_94', ''), ('DictKey_WptName_97', ''),
             ('DictKey_WptName_100', ''), ('DictKey_WptName_103', ''), ('DictKey_WptName_106', ''),
             ('DictKey_WptName_109', ''), ('DictKey_WptName_112', ''), ('DictKey_descriptionBlueTask_3', ''),
             ('DictKey_descriptionRedTask_2', ''), ('DictKey_descriptionText_1', ''),
             ('DictKey_sortie_4', 'sortie_test')])

    def test_qnh(self, mission):
        assert mission.weather.qnh == 760
        mission.weather.qnh = 754
        assert mission.weather.qnh == 754
        for wrong_qnh in ['caribou', 719, 791, -1, None, True]:
            with pytest.raises(ValueError):
                mission.weather.qnh = wrong_qnh

    def test_seasons(self, mission):
        # Season code has been deprecated by ED
        mission.weather.season_code = mission.weather.seasons_enum['winter']
        mission.weather.temperature = -50
        assert mission.weather.temperature == -50
        mission.weather.season_code = mission.weather.seasons_enum['summer']
        assert mission.weather.temperature == 5
        # with pytest.raises(ValueError):
        mission.weather.temperature = -50
        mission.weather.temperature = 50
        assert mission.weather.temperature == 50
        mission.weather.season_code = mission.weather.seasons_enum['winter']
        assert mission.weather.temperature == 15
        # with pytest.raises(ValueError):
        mission.weather.temperature = 50
        mission.weather.temperature = -50
        mission.weather.season_code = mission.weather.seasons_enum['fall']
        assert mission.weather.temperature == -10
        mission.weather.season_code = mission.weather.seasons_enum['summer']
        assert mission.weather.temperature == 5
        mission.weather.temperature = 50
        mission.weather.season_code = mission.weather.seasons_enum['spring']
        assert mission.weather.temperature == 30
        for test in [(1, 'summer'), (2, 'winter'), (3, 'spring'), (4, 'fall')]:
            assert test[0] == mission.weather.get_season_code_from_name(test[1])
            mission.weather.season_code = test[0]
            assert mission.weather.season_name == test[1]
        for wrong_name in (1, -1, None, True, 'caribou'):
            with pytest.raises(ValueError, msg=wrong_name):
                mission.weather.get_season_code_from_name(wrong_name)

    def test_wind(self, mission):
        assert mission.weather.wind_at2000_dir == 0
        assert mission.weather.wind_at2000_speed == 0
        assert mission.weather.wind_at8000_dir == 0
        assert mission.weather.wind_at8000_speed == 0
        assert mission.weather.wind_at_ground_level_dir == 0
        assert mission.weather.wind_at_ground_level_speed == 0
        for wrong_speed in [-1, 51, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_speed):
                mission.weather.wind_at_ground_level_speed = wrong_speed
            with pytest.raises(ValueError, msg=wrong_speed):
                mission.weather.wind_at8000_speed = wrong_speed
            with pytest.raises(ValueError, msg=wrong_speed):
                mission.weather.wind_at2000_speed = wrong_speed
        for wrong_dir in [-1, 360, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_dir):
                mission.weather.wind_at_ground_level_dir = wrong_dir
            with pytest.raises(ValueError, msg=wrong_dir):
                mission.weather.wind_at2000_dir = wrong_dir
            with pytest.raises(ValueError, msg=wrong_dir):
                mission.weather.wind_at8000_dir = wrong_dir
        for i in range(0, 359, 1):
            mission.weather.wind_at8000_dir = i
            mission.weather.wind_at2000_dir = i
            mission.weather.wind_at_ground_level_dir = i
        for i in range(0, 50, 1):
            mission.weather.wind_at8000_speed = i
            mission.weather.wind_at2000_speed = i
            mission.weather.wind_at_ground_level_speed = i

    def test_turbulence(self, mission):
        assert mission.weather.turbulence_at_ground_level == 0
        for i in range(0, 60, 1):
            mission.weather.turbulence_at_ground_level = i
        for wrong_turbulence in [-1, 61, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_turbulence):
                mission.weather.turbulence_at_ground_level = wrong_turbulence

    def test_atmosphere_type(self, mission):
        assert mission.weather.atmosphere_type == 0
        mission.weather.atmosphere_type = 1
        assert mission.weather.atmosphere_type == 1
        for wrong_atmo_type in [-1, 2, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_atmo_type):
                mission.weather.atmosphere_type = wrong_atmo_type

    def test_fog(self, mission):
        assert not mission.weather.fog_enabled
        mission.weather.fog_enabled = True
        assert mission.weather.fog_enabled
        assert mission.weather.fog_visibility == 25
        assert mission.weather.fog_thickness == 0
        mission.weather.fog_visibility = 500
        assert mission.weather.fog_visibility == 500
        mission.weather.fog_thickness = 500
        assert mission.weather.fog_thickness == 500
        for i in range(0, 6000, 100):
            mission.weather.fog_visibility = i
        for i in range(0, 1000, 10):
            mission.weather.fog_thickness = i
        for wrong_visibility in [-1, 6001, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_visibility):
                mission.weather.fog_visibility = wrong_visibility
        for wrong_thickness in [-1, 1001, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_thickness):
                mission.weather.fog_thickness = wrong_thickness

    def test_clouds(self, mission):
        assert mission.weather.cloud_thickness == 200
        assert mission.weather.cloud_base == 300
        for i in range(0, 10):
            mission.weather.cloud_density = i
        for wrong_density in [-1, 11, True, None, 'caribou']:
            with pytest.raises(ValueError, msg=wrong_density):
                mission.weather.cloud_density = wrong_density
        for i in range(300, 5000, 100):
            mission.weather.cloud_base = i
        for wrong_base in [-1, -500, 5001, 50000, None, False, 'caribou']:
            with pytest.raises(ValueError):
                mission.weather.cloud_base = wrong_base
        for i in range(200, 2000, 50):
            mission.weather.cloud_thickness = i
        for wrong_thickness in [199, 2001, -500, 2, 12000, None, False, 'caribou']:
            with pytest.raises(ValueError):
                mission.weather.cloud_thickness = wrong_thickness

    def test_precipitations(self, mission):
        mission.weather.cloud_density = 4
        mission.weather.season_code = 3
        mission.weather.temperature = 1
        mission.weather.precipitations = 0
        for i in range(1, 4):
            with pytest.raises(ValueError, msg=i):
                mission.weather.precipitations = i
        mission.weather.cloud_density = 5
        mission.weather.precipitations = 1
        for i in range(2, 4):
            with pytest.raises(ValueError, msg=i):
                mission.weather.precipitations = i
        mission.weather.cloud_density = 9
        for i in range(0, 2):
            mission.weather.precipitations = i
        mission.weather.temperature = 0
        for i in range(0, 4):
            mission.weather.precipitations = i
        mission.weather.temperature = -1
        for i in range(3, 4):
            mission.weather.precipitations = i
        for i in range(1, 2):
            with pytest.raises(ValueError, msg=i):
                mission.weather.precipitations = i
        mission.weather.precipitations = 4
        # Season code has been deprecated by ED
        # miz.mission.weather.season_code = 1
        # assert miz.mission.weather.temperature == 5
        # assert miz.mission.weather.precipitations == 2
        # miz.mission.weather.season_code = 2
        # miz.mission.weather.temperature = -20
        # assert miz.mission.weather.precipitations == 4
        # miz.mission.weather.precipitations = 3
        # miz.mission.weather.season_code = 1
        # assert miz.mission.weather.precipitations == 1

    def test_ground_control(self, mission):
        assert not mission.ground_control.pilots_control_vehicles
        mission.ground_control.pilots_control_vehicles = True
        assert mission.ground_control.pilots_control_vehicles
        for attrib in [
            'artillery_commander_blue',
            'artillery_commander_red',
            'forward_observer_blue',
            'forward_observer_red',
            'instructor_blue',
            'instructor_red',
            'observer_red',
            'observer_blue',
        ]:
            assert getattr(mission.ground_control, attrib) == 0
            for wrong_param in [-1, 101, True, None, 'caribou']:
                with pytest.raises(ValueError, msg=wrong_param):
                    setattr(mission.ground_control, attrib, wrong_param)
            for i in range(0, 60, 5):
                setattr(mission.ground_control, attrib, i)

    def test_name(self, mission):
        assert 'blue' == mission.blue_coa.coalition_name
        assert 'red' == mission.red_coa.coalition_name

    def test_country_generator(self, mission):
        for coa in (mission.blue_coa, mission.red_coa):
            assert coa.countries
        l = 0
        for country in mission.blue_coa.countries:
            assert isinstance(country, Country)
            l += 1
        assert l == 19
        l = 0
        for country in mission.red_coa.countries:
            assert isinstance(country, Country)
            l += 1
        assert l == 11

    def test_get_country_by_name(self, mission):
        assert isinstance(mission.blue_coa.get_country_by_name('USA'), Country)
        assert isinstance(mission.blue_coa.get_country_by_id(2), Country)
        assert isinstance(mission.blue_coa.get_country_by_name('USA'), Country)
        assert isinstance(mission.blue_coa.get_country_by_id(2), Country)
        for wrong_country_name in (1, -1, 0, False, None, True):
            with pytest.raises(ValueError, msg=wrong_country_name):
                mission.blue_coa.get_country_by_name(wrong_country_name)
        for wrong_country_id in (-1, False, None, True, 'caribou'):
            with pytest.raises(ValueError, msg=wrong_country_id):
                mission.blue_coa.get_country_by_id(wrong_country_id)
        for unknown_country_name in ('nope', 'nope too'):
            with pytest.raises(ValueError, msg=unknown_country_name):
                mission.blue_coa.get_country_by_name(unknown_country_name)
        for unknown_country_id in (150,):
            with pytest.raises(ValueError, msg=unknown_country_id):
                mission.blue_coa.get_country_by_id(unknown_country_id)

    def test_groups(self, mission):
        l = 0
        for group in mission.blue_coa.groups:
            l += 1
            assert isinstance(group, Group)
        assert l == 3
        l = 0
        for group in mission.red_coa.groups:
            l += 1
            assert isinstance(group, Group)
        assert l == 33

    def test_get_groups_from_category(self, mission):
        for invalid_category in ('caribou', 'Plane', 'plAne', 'ships', -1, 0, 1, True, False, None):
            with pytest.raises(ValueError):
                for _ in mission.blue_coa.get_groups_from_category(invalid_category):
                    pass
        with Miz(ALL_OBJECTS) as miz:
            for category in ('ship', 'plane', 'helicopter', 'vehicle'):
                l = 0
                for group in miz.mission.blue_coa.get_groups_from_category(category):
                    assert isinstance(group, Group)
                    assert group.group_category == category
                    l += 1
                assert l == 1

    def test_units(self, mission):
        l = 0
        for unit in mission.blue_coa.units:
            l += 1
            assert isinstance(unit, BaseUnit)
        assert l == 3
        l = 0
        for unit in mission.red_coa.units:
            l += 1
            assert isinstance(unit, BaseUnit)
        assert l == 33

    def test_get_units_from_category(self, mission):
        for invalid_category in ('caribou', 'Plane', 'plAne', 'ships', -1, 0, 1, True, False, None):
            with pytest.raises(ValueError):
                for _ in mission.blue_coa.get_units_from_category(invalid_category):
                    pass
        with Miz(ALL_OBJECTS) as miz:
            # for unit in mission.blue_coa.units:
            #     print(unit.group_category)
            for category in ('ship', 'plane', 'helicopter', 'vehicle'):
                l = 0
                for unit in miz.mission.blue_coa.get_units_from_category(category):
                    assert isinstance(unit, BaseUnit)
                    assert unit.group_category == category
                    l += 1
                assert l == 1

    def test_get_group_by_id(self, mission):
        for group_id in range(1, 3):
            assert isinstance(mission.blue_coa.get_group_by_id(group_id), Group)
        for group_id in range(4, 36):
            assert isinstance(mission.red_coa.get_group_by_id(group_id), Group)
        for wrong_group_id in (-1, False, None, True, 'caribou'):
            with pytest.raises(ValueError, msg=wrong_group_id):
                mission.red_coa.get_group_by_id(wrong_group_id)
        for non_existing_group_id in (37, 50, 100, 150, mission.next_group_id):
            assert mission.red_coa.get_group_by_id(non_existing_group_id) is None
            assert mission.blue_coa.get_group_by_id(non_existing_group_id) is None

    def test_group_by_name(self, mission):
        for group_name in ('etcher', 'gal', 'gilles'):
            assert isinstance(mission.blue_coa.get_group_by_name(group_name), Group)
        for i in range(1, 33):
            assert isinstance(mission.red_coa.get_group_by_name('New Vehicle Group #{}'.format(str(i).zfill(3))),
                              Group)
        for wrong_group_name in (-1, 0, 1, False, True, None):
            with pytest.raises(ValueError, msg=wrong_group_name):
                mission.blue_coa.get_group_by_name(wrong_group_name)
        for non_existing_group_name in ('yup', 'yop', 'New Vehicle group #019', 'Gilles', 'etcheR'):
            assert mission.red_coa.get_group_by_name(non_existing_group_name) is None
            assert mission.blue_coa.get_group_by_name(non_existing_group_name) is None

    def test_get_unit_by_id(self, mission):
        for unit_id in range(1, 3):
            assert isinstance(mission.blue_coa.get_unit_by_id(unit_id), BaseUnit)
        for unit_id in range(4, 36):
            assert isinstance(mission.red_coa.get_unit_by_id(unit_id), BaseUnit)
        for wrong_unit_id in (-1, False, None, True, 'caribou'):
            with pytest.raises(ValueError, msg=wrong_unit_id):
                mission.red_coa.get_unit_by_id(wrong_unit_id)
        for non_existing_unit_id in (37, 50, 100, 150, mission.next_unit_id):
            assert mission.red_coa.get_group_by_id(non_existing_unit_id) is None
            assert mission.blue_coa.get_group_by_id(non_existing_unit_id) is None

    def test_unit_by_name(self, mission):
        for unit_name in ('etcher', 'gal', 'gilles'):
            assert isinstance(mission.blue_coa.get_unit_by_name(unit_name), BaseUnit)
        for i in range(1, 33):
            assert isinstance(mission.red_coa.get_unit_by_name('Unit #{}'.format(str(i).zfill(3))), BaseUnit)
        for wrong_unit_name in (-1, 0, 1, False, True, None):
            with pytest.raises(ValueError, msg=wrong_unit_name):
                mission.blue_coa.get_unit_by_name(wrong_unit_name)
        for non_existing_unit_name in ('yup', 'yop', 'unit #017', 'Gilles', 'etcheR'):
            assert mission.red_coa.get_unit_by_name(non_existing_unit_name) is None
            assert mission.blue_coa.get_unit_by_name(non_existing_unit_name) is None

    def test_set_hidden(self):
        with Miz(TEST_FILE) as miz:
            group = miz.mission.get_group_by_name('etcher')
            assert isinstance(group, Group)
            assert not group.group_hidden
            group.group_hidden = True
            assert group.group_hidden
            miz.zip(OUT_FILE)
        with Miz(OUT_FILE) as miz:
            new_group = miz.mission.get_group_by_name('etcher')
            assert isinstance(new_group, Group)
            for attrib in [x for x in Group.attribs if not x == 'group_hidden']:
                assert getattr(group, attrib) == getattr(new_group, attrib)
            assert group.group_hidden

    @pytest.mark.skip('disabled for the time being')
    def test_group_start_time(self):
        with Miz(TEST_FILE) as miz:
            group = miz.mission.get_group_by_name('etcher')
            assert miz.mission.mission_start_time == group.group_start_time
            assert miz.mission.mission_start_time_as_date == group.group_start_time_as_date
            assert group.group_start_time_as_date == '01/06/2011 12:00:00'
            assert group.group_start_delay == 0
            group.group_start_delay += 60
            assert group.group_start_time_as_date == '01/06/2011 12:01:00'
            group.group_start_delay += 3600
            assert group.group_start_time_as_date == '01/06/2011 13:01:00'
            group.group_start_time_as_date = '01/06/2011 12:00:00'
            assert miz.mission.mission_start_time == group.group_start_time
            assert group.group_start_delay == 0
            for invalid_start_date in (
                    'caribou', True, False, None, -1, '35/06/2010 12:00:00', '01/15/2010 12:00:00',
                    '01/06/2010 25:00:00',
                    '01/06/2010 12:61:00', '01/06/2010 12:00:120'):
                with pytest.raises(ValueError, msg=invalid_start_date):
                    group.group_start_time_as_date = invalid_start_date
            for wrong_start_date in (
                    '01/06/2011 11:59:59', '01/05/2011 12:00:00', '31/05/2011 12:00:00', '01/06/2010 12:00:00'):
                with pytest.raises(ValueError, msg=wrong_start_date):
                    group.group_start_time_as_date = wrong_start_date
            group.group_start_time_as_date = '01/06/2011 13:00:00'
            assert group.group_start_delay == 3600
            group.group_start_time_as_date = '02/06/2011 12:00:00'
            assert group.group_start_delay == 3600 * 24
            miz.zip(OUT_FILE)

        with Miz(OUT_FILE) as miz:
            group = miz.mission.get_group_by_name('etcher')
            assert group.group_start_delay == 3600 * 24

    def test_get_unit(self, mission):
        group = mission.get_group_by_name('etcher')
        assert isinstance(group, Group)
        unit1 = group.get_unit_by_name('etcher')
        assert isinstance(unit1, BaseUnit)
        unit2 = group.get_unit_by_id(1)
        assert isinstance(unit2, BaseUnit)
        unit3 = group.get_unit_by_index(1)
        assert isinstance(unit3, BaseUnit)
        assert unit1 == unit2 == unit3

    def test_objects(self):
        with Miz(ALL_OBJECTS) as miz:
            _ = miz.mission.blue_coa.get_country_by_id(2)
            country = miz.mission.blue_coa.get_country_by_id(2)
            assert isinstance(country, Country)
            assert country.groups
            assert country.units
            for category in ('helicopter', 'ship', 'vehicle', 'plane'):
                assert country.get_groups_from_category(category)
                assert country.get_units_from_category(category)
                for group in country.get_groups_from_category(category):
                    assert isinstance(group, Group)
                for unit in country.get_units_from_category(category):
                    assert isinstance(unit, BaseUnit)
            for wrong_category in (True, -1, 0, 1, False, None, 'caribou'):
                with pytest.raises(ValueError, msg=wrong_category):
                    for _ in country.get_groups_from_category(wrong_category):
                        pass
                with pytest.raises(ValueError, msg=wrong_category):
                    for _ in country.get_units_from_category(wrong_category):
                        pass
            for id_ in (1, 2, 3, 4):
                assert isinstance(country.get_group_by_id(id_), Group)
                assert isinstance(country.get_unit_by_id(id_), BaseUnit)
            assert country.get_unit_by_id(5) is None
            assert country.get_group_by_id(5) is None
            for group_name in ('New Vehicle Group', 'New Helicopter Group', 'New Airplane Group', 'New Ship Group'):
                assert isinstance(country.get_group_by_name(group_name), Group)
            assert country.get_group_by_name('some other group') is None
            for unit_name in ('Unit #1', 'Unit #001', 'Pilot #001', 'Pilot #002'):
                assert isinstance(country.get_unit_by_name(unit_name), BaseUnit)
            assert country.get_unit_by_name('some other unit') is None

    def test_get_country(self, mission):
        assert isinstance(mission.blue_coa.get_country_by_id(2), Country)
        assert isinstance(mission.blue_coa.get_country_by_name('USA'), Country)
        with pytest.raises(ValueError):
            mission.red_coa.get_country_by_name('USA')
        with pytest.raises(ValueError):
            mission.red_coa.get_country_by_id(2)
        with Miz(TEST_FILE) as miz:
            assert isinstance(mission.blue_coa.get_country_by_name('USA'), Country)

    @pytest.mark.parametrize('unit_id, unit_type, radios_to_test', RADIOS_TESTS)
    def test_radios(self, unit_id, unit_type, radios_to_test):
        with Miz(RADIO_FILE) as miz:
            mission = miz.mission

        unit = mission.get_unit_by_id(unit_id)
        assert unit.unit_type == unit_type
        assert isinstance(unit, FlyingUnit)
        for radio in radios_to_test:
            radio_name, radio_number, channels_to_test = radio
            radio_by_name = unit.get_radio_by_name(radio_name)
            radio_by_number = unit.get_radio_by_number(radio_number)
            assert radio_by_name == radio_by_number
            for channel, freq in channels_to_test.items():
                assert radio_by_name.get_frequency(channel) == freq
                assert radio_by_number.get_frequency(channel) == freq

    def test_radios_set_freq(self):
        with Miz(RADIO_FILE) as miz:
            unit = miz.mission.get_unit_by_id(1)
            assert isinstance(unit, FlyingUnit)
            radio = unit.get_radio_by_number(1)
            radio.set_frequency(1, radio.min)
            radio.set_frequency(1, radio.max)
            for wrong_freq_type in [None, False, True, 'caribou', 0, -1]:
                with pytest.raises(ValueError):
                    radio.set_frequency(1, wrong_freq_type)
            for wrong_freq in [radio.max + 1, radio.min - 1]:
                with pytest.raises(ValueError):
                    radio.set_frequency(1, wrong_freq)
            miz.zip(OUT_FILE)
            with Miz(OUT_FILE) as miz2:
                unit2 = miz2.mission.get_unit_by_id(1)
                assert isinstance(unit2, FlyingUnit)
                radio2 = unit2.get_radio_by_number(1)
                assert type(radio) == type(radio2)

    def test_radios_equal(self):
        with Miz(RADIO_FILE) as miz:
            unit = miz.mission.get_unit_by_id(6)
            assert isinstance(unit, FlyingUnit)
            radio1 = unit.get_radio_by_number(1)
            radio2 = unit.get_radio_by_number(2)
            assert not radio1 == radio2
            radio3 = miz.mission.get_unit_by_id(7).get_radio_by_number(2)
            assert radio1.radio_name == radio3.radio_name
            assert radio1 == radio3
            radio1.set_frequency(1, 30.0)
            assert not radio1 == radio3

    def test_radios_generator(self):
        with Miz(RADIO_FILE) as miz:
            unit = miz.mission.get_unit_by_id(6)
            # noinspection PyUnusedLocal
            for radio in unit.radio_presets:
                # TODO resume
                pass

    @given(time=st.integers(0, 86399))
    @settings(max_examples=1)
    def test_mission_start_time(self, time, mission):
        assert mission.mission_start_time == 43200
        assert mission.mission_start_datetime_as_string == '01/06/2011 12:00:00'
        mission.mission_start_time = 0
        assert mission.mission_start_datetime_as_string == '01/06/2011 00:00:00'
        mission.mission_start_time = time

    @given(time=st.integers(min_value=86400))
    @settings(max_examples=1)
    def test_wrong_mission_start_time(self, time, mission):
        with pytest.raises(ValueError):
            mission.mission_start_time = time

    @given(time=st.integers(max_value=-1))
    @settings(max_examples=1)
    def test_wrong_mission_start_time_neg(self, time, mission):
        with pytest.raises(ValueError):
            mission.mission_start_time = time

    def test_repr(self, mission):
        assert 'Mission({})'.format(mission.d) == mission.__repr__()

    def test_coalitions_generator(self, mission):
        assert miz.mission.coalitions
        l = 0
        for coa in miz.mission.coalitions:
            assert isinstance(coa, Coalition)
            l += 1
        assert l == 2

    def test_sortie_name(self):
        with Miz(TEST_FILE) as miz:
            assert miz.mission.sortie_name == 'sortie_test'
            wrong_sortie_names = [1, 0, -1, True, None]
            for wrong_sortie_name in wrong_sortie_names:
                with pytest.raises(ValueError):
                    miz.mission.sortie_name = wrong_sortie_name
            miz.mission.sortie_name = 'caribou'
            assert miz.mission.sortie_name == 'caribou'
            miz.zip(OUT_FILE)
        with Miz(OUT_FILE) as miz:
            assert miz.mission.sortie_name == 'caribou'

    def test_next_unit_id(self, mission):
        assert mission.next_unit_id == 37
        with pytest.raises(IndexError):
            with Miz(DUPLICATE_GROUP_ID) as miz:
                _ = miz.mission.next_unit_id

    def test_next_group_id(self, mission):
        assert mission.next_group_id == 37
        with pytest.raises(IndexError):
            with Miz(DUPLICATE_GROUP_ID) as miz:
                _ = miz.mission.next_group_id

    def test_get_group_by_name(self, mission):
        group = mission.get_group_by_name('etcher')
        assert isinstance(group, Group)
        assert group.group_id == 1
        assert mission.get_group_by_name('le_caribou_puissant') is None

    def test_get_unit_by_name(self, mission):
        unit = mission.get_unit_by_name('etcher')
        assert isinstance(unit, BaseUnit)
        assert unit.unit_id == 1
        assert mission.get_unit_by_name('le_caribou_puissant') is None
