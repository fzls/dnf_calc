#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : const
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

###########################################################
#                         逻辑相关常量                     #
###########################################################

# 可升级得到的工作服列表
work_uniforms = [
    "11150", "12150", "13150", "14150", "15150",  # 工作服防具：大自然
    "21190", "22190", "23190",  # 工作服首饰：权能
    "31230", "32230", "33230",  # 工作服特殊装备：能量
]
# 智慧产物列表
the_product_of_wisdoms = [
    "13390150", "22390240", "23390450", "33390750", "21400340", "31400540", "32410650",
]

# 旧版本自定义存档的列定义
g_old_col_custom_save_key = 14  # 旧版本中，存档项名所在的列
g_old_col_custom_save_value_begin = 15  # 旧版本中，各个存档的该存档项所在的列的初始列，加上存档index（0-99）后得到其所在列
g_old_row_custom_save_start = 0  # 旧版本中，下面的各个行加上这个后得到该存档项最终所在行数

# 自定义存档的列定义
g_col_custom_save_key = 1  # 存档项名所在的列
g_col_custom_save_value_begin = 2  # 各个存档的该存档项所在的列的初始列，加上存档index（0-99）后得到其所在列

# 自定义存档的行定义
g_row_custom_save_start = 300  # 各个自定义列对应的存档名所在的那一行，下面的各个行加上这个后得到该存档项最终所在行数
g_row_custom_save_save_name = 1  # 存档名
g_row_custom_save_weapon = 2  # 武器
g_row_custom_save_job = 3  # 职业选择
g_row_custom_save_fight_time = 4  # 输出时间
g_row_custom_save_title = 5  # 称号选择
g_row_custom_save_pet = 6  # 宠物选择
g_row_custom_save_cd = 7  # 冷却补正
g_row_custom_save_speed = 8  # 选择速度
g_row_custom_save_has_baibianguai = 9  # 是否拥有百变怪
g_row_custom_save_can_upgrade_work_uniforms_nums = 10  # 当前拥有的材料够升级多少件工作服
g_row_custom_save_transfer_from = 11  # 跨界来源账户列表
g_row_custom_save_max_transfer_count = 12  # 最大跨界数目
g_row_custom_save_use_pulei_legend_by_default = 13  # 是否默认将普雷传说装备加入备选池

# 输出职业base_array中的各个下标的含义
index_deal_strength_and_intelligence = 0  # 0-C-stat-力智
index_deal_physical_magical_independent_attack_power = 1  # 1-D-att-物理/魔法/独立攻击力
index_deal_extra_percent_attack_damage = 2  # 2-E-damper-攻击时额外增加X%的伤害增加量
index_deal_extra_percent_crit_damage = 3  # 3-F-criper-暴击时，额外增加X%的伤害增加量
index_deal_extra_percent_addtional_damage = 4  # 4-G-bonper-攻击时，附加X%的伤害，也就是白字
index_deal_extra_percent_elemental_damage = 5  # 5-H-elebon-攻击时，附加X%的属性伤害
index_deal_extra_percent_final_damage = 6  # 6-I-allper-最终伤害+X%
index_deal_extra_percent_physical_magical_independent_attack_power = 7  # 7-J-attper-物理/魔法/独立攻击力 +X%
index_deal_extra_percent_strength_and_intelligence = 8  # 8-K-staper-力智+X%
index_deal_extra_all_element_strength = 9  # 9-L-ele-所有属性强化+X
index_deal_extra_percent_continued_damage = 10  # 10-M-sloper-发生持续伤害5秒，伤害量为对敌人造成伤害的X%
index_deal_extra_percent_skill_attack_power = 11  # 11-N-skiper-技能攻击力 +X%
index_deal_extra_percent_special_effect = 12  # 12-O-special-特殊词条补正，如歧路和不息的装备，详见自定义中这俩装备相关配置
index_deal_extra_percent_attack_speed = 13  # 13-P-speed-攻击速度 +X%
index_deal_extra_percent_magic_physical_crit_rate = 14  # 14-Q-critical-魔法/物理暴击率 +X%
index_deal_extra_active_skill_effect = 15  # 15-R-active-主动技能增加等级所带来的的影响（目前C的伤害计算没有计入该值，仅奶系职业用到）
index_deal_extra_passive_transfer_skill = 16  # 16-S-pas1-增加转职被动的等级
index_deal_extra_passive_first_awaken_skill = 17  # 17-T-pas2-增加一绝被动的等级
index_deal_extra_passive_second_awaken_skill = 18  # 18-U-pas3-增加二觉被动的等级
index_deal_extra_passive_third_awaken_skill = 19  # 19-V-pas4-增加三觉被动的等级
index_deal_cool_correction = 20  # 20-Y-cool_skill-冷却矫正系数，每冷却1%，记0.35这个值
index_deal_extra_active_second_awaken_skill = 21  # 21-AK-active2-二觉主动技能
index_deal_extra_active_skill_lv_1_45 = 22  # 22-AO-pas0-1_45主动技能
index_deal_extra_active_skill_lv_50 = 23  # 23-AP-pas1-50主动技能
index_deal_extra_active_skill_lv_60_80 = 24  # 24-AQ-pas2-60_80主动技能
index_deal_extra_active_skill_lv_85 = 25  # 25-AR-pas3-85主动技能
index_deal_extra_active_skill_lv_95 = 26  # 26-AS-pas4-95主动技能
index_deal_extra_active_skill_lv_100 = 27  # 27-AT-pas5-100主动技能

deal_entry_index_to_name = {
    index_deal_strength_and_intelligence: "0-C-stat-力智",
    index_deal_physical_magical_independent_attack_power: "1-D-att-物理/魔法/独立攻击力",
    index_deal_extra_percent_attack_damage: "2-E-damper-攻击时额外增加X%的伤害增加量",
    index_deal_extra_percent_crit_damage: "3-F-criper-暴击时，额外增加X%的伤害增加量",
    index_deal_extra_percent_addtional_damage: "4-G-bonper-攻击时，附加X%的伤害，也就是白字",
    index_deal_extra_percent_elemental_damage: "5-H-elebon-攻击时，附加X%的属性伤害",
    index_deal_extra_percent_final_damage: "6-I-allper-最终伤害+X%",
    index_deal_extra_percent_physical_magical_independent_attack_power: "7-J-attper-物理/魔法/独立攻击力 +X%",
    index_deal_extra_percent_strength_and_intelligence: "8-K-staper-力智+X%",
    index_deal_extra_all_element_strength: "9-L-ele-所有属性强化+X",
    index_deal_extra_percent_continued_damage: "10-M-sloper-发生持续伤害5秒，伤害量为对敌人造成伤害的X%",
    index_deal_extra_percent_skill_attack_power: "11-N-skiper-技能攻击力 +X%",
    index_deal_extra_percent_special_effect: "12-O-special-特殊词条补正，如歧路和不息的装备，详见自定义中这俩装备相关配置",
    index_deal_extra_percent_attack_speed: "13-P-speed-攻击速度 +X%",
    index_deal_extra_percent_magic_physical_crit_rate: "14-Q-critical-魔法/物理暴击率 +X%",
    index_deal_extra_active_skill_effect: "15-R-active-主动技能增加等级所带来的的影响（目前C的伤害计算没有计入该值，仅奶系职业用到）",
    index_deal_extra_passive_transfer_skill: "16-S-pas1-增加转职被动的等级",
    index_deal_extra_passive_first_awaken_skill: "17-T-pas2-增加一绝被动的等级",
    index_deal_extra_passive_second_awaken_skill: "18-U-pas3-增加二觉被动的等级",
    index_deal_extra_passive_third_awaken_skill: "19-V-pas4-增加三觉被动的等级",
    index_deal_cool_correction: "20-Y-cool_skill-冷却矫正系数，每冷却1%，记0.35这个值",
    index_deal_extra_active_second_awaken_skill: "21-AK-active2-二觉主动技能",
    index_deal_extra_active_skill_lv_1_45: "22-AO-pas0-1_45主动技能",
    index_deal_extra_active_skill_lv_50: "23-AP-pas1-50主动技能",
    index_deal_extra_active_skill_lv_60_80: "24-AQ-pas2-60_80主动技能",
    index_deal_extra_active_skill_lv_85: "25-AR-pas3-85主动技能",
    index_deal_extra_active_skill_lv_95: "26-AS-pas4-95主动技能",
    index_deal_extra_active_skill_lv_100: "27-AT-pas5-100主动技能",
}

# 奶系职业base_array中的各个下标的含义
index_buf_physical_and_mental_strength = 0  # 0-C-[守护恩赐]体力、精神 +X
index_buf_intelligence = 1  # 1-D-[启示:圣歌]、[人偶操纵者]智力 +X
index_buf_bless_extra_percent_strength_and_intelligence = 2  # 2-E-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%
index_buf_bless_extra_percent_physical_attack_power = 3  # 3-F-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]物理攻击力增加量 +X%
index_buf_bless_extra_percent_magical_attack_power = 4  # 4-G-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]魔法攻击力增加量 +X%
index_buf_bless_extra_percent_independent_attack_power = 5  # 5-H-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]独立攻击力增加量 +X%
index_buf_taiyang_extra_strength_and_intelligence = 6  # 6-I-[天启之珠]、[圣光天启]、[开幕！人偶剧场]力量/智力 +X
index_buf_taiyang_extra_percent_strength_and_intelligence = 7  # 7-J-[天启之珠]、[圣光天启]、[开幕！人偶剧场]力量、智力增加量 +X%
index_buf_bless_lv30 = 8  # 8-K-30级技能或直接指定祝福技能祝福等级+X
index_buf_taiyang_lv50 = 9  # 9-L-50级技能或直接指定太阳技能太阳等级+X
index_buf_amplification = 10  # [守护徽章]体力、精神增加量 +15%[勇气圣歌]BUFF效果增幅量 +5%[死命召唤]BUFF效果增幅量 +5%是否buff效果增幅
index_buf_job_passive_lv15 = 11  # 11-N-[守护恩赐]、[启示：圣歌]、[人偶操纵者]15级职业被动Lv+X
index_buf_naiba_protect_badge_lv25 = 12  # 12-O-奶爸25级守护徽章等级+X
index_buf_first_awaken_passive_lv48 = 13  # 13-P-1觉被动等级+X
index_buf_second_awaken_passive_lv75 = 14  # 14-Q-2觉被动等级+X
index_buf_second_awaken_lv85 = 15  # 15-R-2觉等级+X
index_buf_third_awaken_passive_lv95 = 16  # 16-S-3觉被动等级+X
index_buf_belief_halo = 17  # 17-T-[信念光环]体力、精神 +X
index_buf_piety_halo_or_girs_love = 18  # 18-U-[虞诚信念]、[少女的爱]力量/智力 +X
index_buf_hymn_cool = 19  # 19-V-圣歌冷却减少X% (re: 目前好像没实装)
index_buf_wisteria_whip_cool = 20  # 20-W-藤鞭冷却减少X% (re: 目前好像没实装)

buf_entry_index_to_name = {
    index_buf_physical_and_mental_strength: "0-C-[守护恩赐]体力、精神 +X",
    index_buf_intelligence: "1-D-[启示:圣歌]、[人偶操纵者]智力 +X",
    index_buf_bless_extra_percent_strength_and_intelligence: "2-E-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%",
    index_buf_bless_extra_percent_physical_attack_power: "3-F-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]物理攻击力增加量 +X%",
    index_buf_bless_extra_percent_magical_attack_power: "4-G-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]魔法攻击力增加量 +X%",
    index_buf_bless_extra_percent_independent_attack_power: "5-H-[荣誉祝福]、[勇气祝福]、[禁忌诅咒]独立攻击力增加量 +X%",
    index_buf_taiyang_extra_strength_and_intelligence: "6-I-[天启之珠]、[圣光天启]、[开幕！人偶剧场]力量/智力 +X",
    index_buf_taiyang_extra_percent_strength_and_intelligence: "7-J-[天启之珠]、[圣光天启]、[开幕！人偶剧场]力量、智力增加量 +X%",
    index_buf_bless_lv30: "8-K-30级技能或直接指定祝福技能祝福等级+X",
    index_buf_taiyang_lv50: "9-L-50级技能或直接指定太阳技能太阳等级+X",
    index_buf_amplification: "[守护徽章]体力、精神增加量 +15%[勇气圣歌]BUFF效果增幅量 +5%[死命召唤]BUFF效果增幅量 +5%是否buff效果增幅",
    index_buf_job_passive_lv15: "11-N-[守护恩赐]、[启示：圣歌]、[人偶操纵者]15级职业被动Lv+X",
    index_buf_naiba_protect_badge_lv25: "12-O-奶爸25级守护徽章等级+X",
    index_buf_first_awaken_passive_lv48: "13-P-1觉被动等级+X",
    index_buf_second_awaken_passive_lv75: "14-Q-2觉被动等级+X",
    index_buf_second_awaken_lv85: "15-R-2觉等级+X",
    index_buf_third_awaken_passive_lv95: "16-S-3觉被动等级+X",
    index_buf_belief_halo: "17-T-[信念光环]体力、精神 +X",
    index_buf_piety_halo_or_girs_love: "18-U-[虞诚信念]、[少女的爱]力量/智力 +X",
    index_buf_hymn_cool: "19-V-圣歌冷却减少X% (re: 目前好像没实装)",
    index_buf_wisteria_whip_cool: "20-W-藤鞭冷却减少X% (re: 目前好像没实装)",
}

job_to_base_array_index_range_and_index_to_name_dict = {
    "deal": {
        "index_begin": index_deal_strength_and_intelligence,
        "index_end": index_deal_extra_active_skill_lv_100,
        "index_to_name_dict": deal_entry_index_to_name,
    },
    "buf": {
        "index_begin": index_buf_physical_and_mental_strength,
        "index_end": index_buf_wisteria_whip_cool,
        "index_to_name_dict": buf_entry_index_to_name,
    },
}

# 国服特色词条（宠物、称号、徽章、皮肤、宝珠、武器装扮等等）
entry_name_to_indexes = {
    # 物理/魔法/独立攻击力 +X
    "physical_magical_independent_attack_power": {
        "deal": [index_deal_physical_magical_independent_attack_power],
    },
    # 力量/智力 +X
    "strength_and_intelligence": {
        "deal": [index_deal_strength_and_intelligence],
        "buf": [index_buf_intelligence],
    },
    # 体力/精神 +X
    "physical_and_mental_strength": {
        "buf": [index_buf_physical_and_mental_strength],
    },
    # 攻击速度+X%
    "extra_percent_attack_speed": {
        "deal": [index_deal_extra_percent_attack_speed],
    },
    # 所有属性强化 +X
    "extra_all_element_strength": {
        "deal": [index_deal_extra_all_element_strength],
    },
    # 物理、魔法暴击率 +X%
    "extra_percent_magic_physical_crit_rate": {
        "deal": [index_deal_extra_percent_magic_physical_crit_rate],
    },
    # 攻击时，附加X%的伤害
    "extra_percent_addtional_damage": {
        "deal": [index_deal_extra_percent_addtional_damage],
    },
    # 增加X%的力量、智力
    "extra_percent_strength_and_intelligence": {
        "deal": [index_deal_extra_percent_strength_and_intelligence],
    },
    # 攻击时，有X1几率增加X2点力量、智力、体力、精神，效果持续X3秒。（冷却时间X4秒）
    # ps：只对输出职业生效，由于站街不生效，奶不用管这个词条，所以名字需要跟四维那个区分开来
    "strength_and_intelligence_when_attack": {
        "deal": [index_deal_strength_and_intelligence],
    },
    # 暴击时，额外增加X%的伤害增加量。（决斗场中，适用一般效果）
    "extra_percent_crit_damage": {
        "deal": [index_deal_extra_percent_crit_damage],
    },
    # 最终伤害增加X%
    "extra_percent_final_damage": {
        "deal": [index_deal_extra_percent_final_damage],
    },
    # 所有职业Lv1~50全部技能Lv+1（特性技能除外）
    "extra_all_job_all_skill_lv_1_50": {
        "deal": [
            index_deal_extra_passive_transfer_skill,
            index_deal_extra_passive_first_awaken_skill,
            index_deal_extra_active_skill_lv_1_45,
            index_deal_extra_active_skill_lv_50,
        ],
        "buf": [
            index_buf_bless_lv30,
            index_buf_taiyang_lv50,
            index_buf_job_passive_lv15,
            index_buf_naiba_protect_badge_lv25,
            index_buf_first_awaken_passive_lv48,
        ]
    },
    # 冷却矫正系数（仅输出职业）
    "cool_correction": {
        "deal": [index_deal_cool_correction]
    },
    # 冷却减少时间-X%（仅奶系职业）
    "reduce_percent_cool": {
        "buf": [
            index_buf_hymn_cool,
            index_buf_wisteria_whip_cool,
        ]
    },
    # 宠物技能：使主人增加X%的攻击力，是乘算，且加到最终伤害中，所以可以视为输出职业的技能攻击力词条来处理
    "creature_increase_owner_attack_power": {
        "deal": [index_deal_extra_percent_skill_attack_power],
    },
    # 所有职业Lv1~50全部主动技能Lv+X（特性技能除外）
    "extra_all_job_all_active_skill_lv_1_50": {
        "deal": [
            index_deal_extra_active_skill_lv_1_45,
            index_deal_extra_active_skill_lv_50,
        ],
        "buf": [
            index_buf_bless_lv30,
            index_buf_taiyang_lv50,
            index_buf_naiba_protect_badge_lv25,
        ]
    },
    # 所有职业Lv1~30全部主动技能Lv+X（特性技能除外）
    "extra_all_job_all_active_skill_lv_1_30": {
        "deal": [
            index_deal_extra_active_skill_lv_1_45,  # 由于原版中输出职业没有1-30这样的词条,这个好像不太好处理?暂时先打个折?
        ],
        "buf": [
            index_buf_bless_lv30,
            index_buf_naiba_protect_badge_lv25,
        ]
    },
    # 勇气祝福(奶系) +X
    "extra_bless_skill": {
        "buf": [
            index_buf_bless_lv30,
        ]
    },
    # 太阳(奶系) +X
    "extra_taiyang_skill": {
        "buf": [
            index_buf_taiyang_lv50,
        ]
    },
    # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%
    "extra_percent_bless_strength_and_intelligence": {
        "buf": [
            index_buf_bless_extra_percent_strength_and_intelligence,
        ]
    },
    # 输出职业转职被动技能Lv+X
    "extra_deal_passive_transfer_skill": {
        "deal": [
            index_deal_extra_passive_transfer_skill,
        ],
    },
    # 二觉被动技能Lv+X
    "extra_deal_passive_second_awaken_skill": {
        "deal": [
            index_deal_extra_passive_second_awaken_skill,
        ],
    },
    # 其他额外最终加成,采用与技能攻击力一样的算法
    "other_rate_like_extra_percent_skill_attack_power": {
        "deal": [index_deal_extra_percent_skill_attack_power],
    },
    # 所有职业Lv15~20全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_15_20": {
        "deal": [
            index_deal_extra_passive_transfer_skill,
        ],
        "buf": [
            index_buf_job_passive_lv15,
        ]
    },
    # 所有职业Lv20~25全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_20_25": {
        "buf": [
            index_buf_naiba_protect_badge_lv25,
        ]
    },
    # 所有职业Lv25~30全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_25_30": {
        "buf": [
            index_buf_bless_lv30,
            index_buf_naiba_protect_badge_lv25,
        ]
    },
    # 所有职业Lv30~35全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_30_35": {
        "buf": [
            index_buf_bless_lv30,
        ]
    },
    # (在buff换装中，且与当前身上穿的不一样)所有职业Lv25~30全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_25_30_in_buff_dress_up": {
        "buf": [
            index_buf_bless_lv30,
        ]
    },
    # (在buff换装中，且与当前身上穿的不一样)所有职业Lv30~35全部技能Lv+X（特性技能除外）
    "extra_all_job_all_skill_lv_30_35_in_buff_dress_up": {
        "buf": [
            index_buf_bless_lv30,
        ]
    },
}

entry_name_to_name = {
    "physical_magical_independent_attack_power": "物理/魔法/独立攻击力 +X",
    "strength_and_intelligence": "力量/智力 +X",
    "physical_and_mental_strength": "体力/精神 +X",
    "extra_percent_attack_speed": "攻击速度+X%",
    "extra_all_element_strength": "所有属性强化 +X",
    "extra_percent_magic_physical_crit_rate": "物理、魔法暴击率 +X%",
    "extra_percent_addtional_damage": "攻击时，附加X%的伤害",
    "extra_percent_strength_and_intelligence": "增加X%的力量、智力",
    "strength_and_intelligence_when_attack": "攻击时，有X1几率增加X2点力量、智力、体力、精神，效果持续X3秒。（冷却时间X4秒） ps：只对输出职业生效，由于站街不生效，奶不用管这个词条，所以名字需要跟四维那个区分开来",
    "extra_percent_crit_damage": "暴击时，额外增加X%的伤害增加量。（决斗场中，适用一般效果）",
    "extra_percent_final_damage": "最终伤害增加X%",
    "extra_all_job_all_skill_lv_1_50": "所有职业Lv1~50全部技能Lv+1（特性技能除外）",
    "cool_correction": "冷却矫正系数（仅输出职业）",
    "reduce_percent_cool": "冷却减少时间-X%（仅奶系职业）",
    "creature_increase_owner_attack_power": "宠物技能：使主人增加X%的攻击力，是乘算，且加到最终伤害中，所以可以视为输出职业的技能攻击力词条来处理",
    "extra_all_job_all_active_skill_lv_1_50": "所有职业Lv1~50全部主动技能Lv+X（特性技能除外）",
    "extra_all_job_all_active_skill_lv_1_30": "所有职业Lv1~30全部主动技能Lv+X（特性技能除外）",
    "extra_bless_skill": "勇气祝福(奶系) +X",
    "extra_taiyang_skill": "太阳(奶系) +X",
    "extra_percent_bless_strength_and_intelligence": "[荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%",
    "extra_deal_passive_transfer_skill": "输出职业转职被动技能Lv+X",
    "extra_deal_passive_second_awaken_skill": "二觉被动技能Lv+X",
    "other_rate_like_extra_percent_skill_attack_power": "其他额外最终加成,采用与技能攻击力一样的算法",
    "extra_all_job_all_skill_lv_15_20": "所有职业Lv15~20全部技能Lv+X（特性技能除外）",
    "extra_all_job_all_skill_lv_20_25": "所有职业Lv20~25全部技能Lv+X（特性技能除外）",
    "extra_all_job_all_skill_lv_25_30": "所有职业Lv25~30全部技能Lv+X（特性技能除外）",
    "extra_all_job_all_skill_lv_30_35": "所有职业Lv30~35全部技能Lv+X（特性技能除外）",
    "extra_all_job_all_skill_lv_25_30_in_buff_dress_up": "(在buff换装中，且与当前身上穿的不一样)所有职业Lv25~30全部技能Lv+X（特性技能除外）",
    "extra_all_job_all_skill_lv_30_35_in_buff_dress_up": "(在buff换装中，且与当前身上穿的不一样)所有职业Lv30~35全部技能Lv+X（特性技能除外）",
}