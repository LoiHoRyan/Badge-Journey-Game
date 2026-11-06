# -*- coding: utf-8 -*-
WIDTH = 1152
HEIGHT = 768
FPS = 60
TITLE = "Badge Journey"
GRAVITY = .75
PLAYER_SPEED = 5.2
JUMP_POWER = -14.2
DOUBLE_JUMP_POWER = -17.0
MAX_FALL_SPEED = 18
MAX_HEALTH = 5
ATTACK_TIME = 14
INVINCIBLE_TIME = 90
DAMAGE_ZONE_COOLDOWN = 60
MUSIC_FILES = {
    "opening": "music/openingsong.mp3",
    "tutorial": "music/tutorial.mp3",
    "question": "music/traloicauhoi.mp3",
    "ending": "music/endingsong.mp3",
    "game_over": "music/gameover.mp3",
    "pause": "music/resumegame.mp3",
}
LEVEL_MUSIC = {
    1: "music/man1dongco.mp3",
    2: "music/man2samac.mp3",
    3: "music/man3baibien.mp3",
    4: "music/man4rungsau.mp3",
    5: "music/man5vungtuyet.mp3",
    6: "music/man6nuilua.mp3",
    7: "music/man7thanhphotrenmay.mp3",
    8: "music/man8nhamaycokhi.mp3",
    9: "music/man9khonggian.mp3",
    10: "music/man10dencocuoicung.mp3",
}
SOUND_FILES = {
    "hit": "music/hit.mp3",
    "portal": "music/portal.mp3",
    "spike": "music/spiketrap.mp3",
    "hurt": "music/tiengmatmau.mp3",
    "coin": "music/tiengxu.mp3",
    "victory": "music/victory.mp3",
    "skill_wave": "music/skill_wave.mp3",
    "skill_shield": "music/skill_shield.mp3",
    "shield_break": "music/skill_shield_break.mp3",
    "skill_dash": "music/skill_dash.mp3",
    "skill_storm": "music/skill_storm.mp3",
    "no_mana": "music/no_mana.mp3",
    "skill_cooldown": "music/skill_cooldown.mp3",
    "mana_restore": "music/mana_restore.mp3",
}

# SKILL & MANA
MAX_MANA=100
MANA_REGEN_AMOUNT=1
MANA_REGEN_FRAMES=30
MANA_PER_COIN=2
MANA_PER_ENEMY_HIT=3
MANA_PER_BOSS_HIT=2
SKILL_WAVE_COST=20
SKILL_WAVE_COOLDOWN=90
SKILL_WAVE_RANGE=320
SKILL_WAVE_DAMAGE=2
SKILL_SHIELD_COST=30
SKILL_SHIELD_COOLDOWN=480
SKILL_SHIELD_TIME=180
SKILL_DASH_COST=25
SKILL_DASH_COOLDOWN=240
SKILL_DASH_DISTANCE=150
SKILL_DASH_DAMAGE=1
SKILL_DASH_INVINCIBLE=24
SKILL_STORM_COST=60
SKILL_STORM_COOLDOWN=900
SKILL_STORM_DAMAGE=3
SKILL_STORM_BOSS_DAMAGE=4
QUESTION_CORRECT_DELAY_MS=1500
