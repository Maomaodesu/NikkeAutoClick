import time
from player import Player

front_player = Player('front')


# 防御前哨基地 一举歼灭 获取奖励
def defence_base():
    front_player.match_and_click_by_order_with_shift([
        ('free_shop', 90, 100),
        ('destroy', 0, 0),
        ('destroy_start', 0, 0),
        ('REWARD', 0, 0),
        ('destroy_cancel', 0, 0),
        ('gain_reward', 0, 0),
        ('REWARD', 0, 0),
        ('gain_reward_click', 0, 0)
    ])


# 友情点
def friend_points():
    front_player.match_and_click_by_order([
        'friend', 'friend_give',
        'friend_confirm',
        'friend_close'])


# 邮箱
def mail():
    front_player.match_and_click_by_order(['mail', 'mail_get_all', 'REWARD', 'mail_close'])


# 模拟室
def simulation_room():
    player = Player('simulation')
    front_player.match_and_click_by_order(['ark', 'simulation_room'])
    player.match_and_click_by_order(['simulation_start_1', 'simulation_difficulty_5', 'simulation_zone_c'])
    if player.match('simulation_finished') is None:
        player.match_and_click_by_order(['simulation_start_2'])
        player.match_and_click_by_order([
            'simulation_fast',
            'simulation_skip_all',
            'simulation_battle_begin',
        ])
        while True:
            time.sleep(5)
            if player.match('simulation_battle_end') is not None:
                player.match_and_click_with_delay('simulation_battle_end', 5)
                break
        # 模拟结束
        player.match_and_click_by_order([
            'simulation_end',
            'simulation_end_confirm'
        ])
    else:
        player.match_and_click_with_delay('simulation_close', 3)
    # 返回主页
    front_player.match_and_click_with_delay('HOME', 3)


# 免费商店
def free_shop():
    player = Player('free_shop')
    front_player.match_and_click_by_order(['free_shop'])
    player.match_and_click_by_order_with_shift([
        # 普通商店领取每日免费物品
        ('free_shop_normal', 90, 150),
        ('free_shop_normal_0_diamond_purchase', 0, 0),
    ])
    front_player.match_and_click_with_delay('REWARD', 2)

    # 竞技场商店购买每日物品
    # 熔炉
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', 0, 660)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0.3)
    if player.match('free_shop_insufficient_funds') is not None:
        time.sleep(1)
        player.match_and_click_by_order(['arena_shop_purchase_cancel'])
    else:
        front_player.match_and_click_with_delay('REWARD', 2)
    # 位置1
    free_shop_detect_loop(front_player, player,0, 110)
    # 位置2
    free_shop_detect_loop(front_player, player,0, 220)
    # 位置3
    free_shop_detect_loop(front_player, player,0, 330)
    # 位置4
    free_shop_detect_loop(front_player, player, 0, 440)
    front_player.match_and_click_with_delay('RETURN', 2)

    # # 位置2
    # player.match_and_click_by_order_with_shift([
    #     ('arena_shop_unselected', 0, 0),
    #     ('arena_shop_selected', 0, 220)
    # ])
    # player.match_and_click_with_delay('arena_shop_purchase', 0.3)
    # if player.match('free_shop_insufficient_funds') is not None:
    #     time.sleep(1)
    #     front_player.match_and_click_with_delay('arena_shop_purchase_cancel', 2)
    # else:
    #     front_player.match_and_click_with_delay('REWARD', 2)
    #
    # # 位置3
    # player.match_and_click_by_order_with_shift([
    #     ('arena_shop_unselected', 0, 0),
    #     ('arena_shop_selected', 0, 330)
    # ])
    # player.match_and_click_with_delay('arena_shop_purchase', 0.3)
    # if player.match('free_shop_insufficient_funds') is not None:
    #     time.sleep(1)
    #     front_player.match_and_click_with_delay('arena_shop_purchase_cancel', 2)
    # else:
    #     front_player.match_and_click_with_delay('REWARD', 2)
    #
    # # 位置4
    # player.match_and_click_by_order_with_shift([
    #     ('arena_shop_unselected', 0, 0),
    #     ('arena_shop_selected', 0, 440)
    # ])
    # player.match_and_click_with_delay('arena_shop_purchase', 0.3)
    # if player.match('free_shop_insufficient_funds') is not None:
    #     time.sleep(1)
    #     front_player.match_and_click_with_delay('arena_shop_purchase_cancel', 2)
    # else:
    #     front_player.match_and_click_with_delay('REWARD', 2)
    #     front_player.match_and_click_with_delay('RETURN', 2)


def free_shop_detect_loop(front_player, player, direction, distance):
    # 定位到商品并点击
    player.match_and_click_by_order_with_shift([
        ('arena_shop_unselected', 0, 0),
        ('arena_shop_selected', direction, distance)
    ])
    player.match_and_click_with_delay('arena_shop_purchase', 0)
    attempt = 0
    insufficient_funds_status = None
    while insufficient_funds_status is None and attempt < 10:
        insufficient_funds_status = player.match('free_shop_insufficient_funds')
        # 每次循环增加尝试次数
        attempt += 1
    if insufficient_funds_status is not None:
        time.sleep(1)
        player.match_and_click_with_delay('arena_shop_purchase_cancel', 2)
    else:
        front_player.match_and_click_with_delay('REWARD', 2)


# 付费商店
def paid_shop():
    player = Player('paid_shop')
    daily = False
    weekly = False
    monthly = False
    front_player.match_and_click_with_delay('paid_shop_1', 2)
    front_player.match_and_click_with_delay('paid_shop_2', 2)
    while not (daily & weekly & monthly):
        # if daily & weekly & monthly:
        #     break
        player.match_and_click_by_order([
            # 消费年龄限制
            'paid_shop_age_limit',
            'paid_shop_age_limit_confirm',
            # 评价通知
            'paid_shop_info_close'])
        player.match_and_click_by_order_with_shift([
            # 日周月免费钻石
            ('paid_shop_gift', 0, 0),
            ('paid_shop_gift_shake', 0, 0)
        ])
        # 每日
        player.match_and_click_by_order_with_shift(
            [('paid_shop_beginner_special_support_selected', 0, 120), ('paid_shop_free_diamond', 0, 0)])
        front_player.match_and_click_with_delay('REWARD', 2)

        paid_shop_free_diamond_daily_sold_out = player.match('paid_shop_free_diamond_daily_sold_out')
        if paid_shop_free_diamond_daily_sold_out:
            daily = True
        # 每周
        player.match_and_click_by_order_with_shift(
            [('paid_shop_beginner_special_support_unselected', 0, 240), ('paid_shop_free_diamond', 0, 0)])
        front_player.match_and_click_with_delay('REWARD', 2)

        paid_shop_free_diamond_weekly_sold_out = player.match('paid_shop_free_diamond_weekly_sold_out')
        if paid_shop_free_diamond_weekly_sold_out:
            weekly = True
        # 每月
        player.match_and_click_by_order_with_shift(
            [('paid_shop_beginner_special_support_unselected', 0, 360), ('paid_shop_free_diamond', 0, 0)])
        front_player.match_and_click_with_delay('REWARD', 2)

        paid_shop_free_diamond_monthly_sold_out = player.match('paid_shop_free_diamond_monthly_sold_out')
        if paid_shop_free_diamond_monthly_sold_out:
            monthly = True
    player.match_and_click_with_delay('paid_shop_return', 1)


# 咨询
def consult():
    player = Player('nikke_consult')
    # 对第一个nikke进行咨询
    front_player.match_and_click_by_order(['lobby', 'nikke', 'nikke_consult'])
    player.match_and_click_by_order_with_shift([('nikke_consult_all', 90, 120)])
    while True:
        # 循环结束条件 指挥官体力用尽 —— 快速咨询
        if player.match('nikke_consult_quick'):
            # 进行快速咨询
            player.match_and_click_with_delay('nikke_consult_quick', 0.1)
            # 检测指挥官体力用尽,结束咨询
            if player.match('nikke_consult_commander_end') is not None:
                break
            # 检测妮姬体力用尽,翻页并跳过本轮循环
            if player.match('nikke_consult_nikke_end') is not None:
                player.match_and_click_by_order(['nikke_consult_next'])
                continue
            # 否则进入快速咨询
            else:
                time.sleep(2.5)
                front_player.match_and_click_by_order(['CONFIRM'])
                player.match_and_click_by_order(['nikke_consult_next_step'])

        # 循环结束条件 指挥官体力用尽 ——普通咨询
        else:
            # 进行普通咨询
            player.match_and_click_with_delay('nikke_consult_normal', 0.1)
            # 检测指挥官体力用尽,结束咨询
            if player.match('nikke_consult_commander_end') is not None:
                break
            # 检测妮姬体力用尽,翻页并跳过本轮循环
            if player.match('nikke_consult_nikke_end') is not None:
                player.match_and_click_by_order(['nikke_consult_next'])
                continue
            # 否则进入普通咨询
            else:
                # 进入咨询动画
                while True:
                    # 进行普通咨询
                    player.match_and_click_with_delay('nikke_consult_normal', 0.1)
                    # 检测指挥官体力用尽,结束咨询动画
                    if player.match('nikke_consult_commander_end') is not None:
                        break
                    # 检测妮姬体力用尽,结束咨询动画
                    if player.match('nikke_consult_nikke_end') is not None:
                        break
                    front_player.match_and_click_by_order(['CONFIRM'])
                    player.match_and_click_by_order([
                        'nikke_consult_normal_auto', 'nikke_consult_normal_option_1',
                        'nikke_consult_normal_skip', 'nikke_consult_next_step'
                    ])
                # 结束咨询动画并翻页
                player.match_and_click_by_order(['nikke_consult_next'])
    # 咨询结束，返回主页
    front_player.match_and_click_by_order(['HOME'])


# 新人竞技场
def arena():
    player = Player('arena')
    front_player.match_and_click_with_delay('ark', 4)
    front_player.match_and_click_with_delay('arena', 4)
    player.match_and_click_with_delay('arena_beginner', 0)
    attempt = 0
    arena_session_end_status = None
    while arena_session_end_status is None and attempt < 10:
        arena_session_end_status = player.match('arena_session_end')
        # 每次循环增加尝试次数
        attempt += 1
    if arena_session_end_status is not None:
        time.sleep(1)
        front_player.match_and_click_with_delay('HOME', 2)
    else:
        while True:
            arena_beginner_logo = player.match('arena_beginner_logo')
            arena_beginner_battle_free = player.match('arena_beginner_battle_free')
            if arena_beginner_logo is not None:
                if arena_beginner_battle_free is None:
                    front_player.match_and_click_by_order(['HOME'])
                    break
            player.match_and_click_by_order_with_shift([
                ('arena_beginner_battle_free', 90, 220),
                ('arena_beginner_battle_enter', 0, 0),
                ('arena_next', 270, 200)
            ])


# 远征
def trip():
    front_player.match_and_click_with_delay('base', 6)
    front_player.match_and_click_with_delay('trip', 4)
    if front_player.match('trip_gain_all_reward') is not None:
        front_player.match_and_click_by_order(['trip_gain_all_reward', 'REWARD'])
    front_player.match_and_click_by_order(['trip_send_all', 'trip_send', 'trip_close'])


def interception():
    player = Player('interception')
    front_player.match_and_click_with_delay('ark', 5)
    front_player.match_and_click_with_delay('interception', 5)
    player.match_and_click_with_delay('interception_challenge', 5)
    interception_end_detect(player, 'interception_battle', 180)
    interception_end_detect(player, 'interception_fast_battle', 5)
    interception_end_detect(player, 'interception_fast_battle', 5)
    front_player.match_and_click_with_delay('HOME', 3)


def interception_end_detect(player, button_name, wait_second):
    player.match_and_click_with_delay(button_name, wait_second)
    interception_end_status = None
    while interception_end_status is None:
        interception_end_status = player.match('interception_end')
        time.sleep(1)
    player.match_and_click_with_delay('interception_end', 3)


def mission():
    front_player.match_and_click_by_order(['mission', 'mission_get_all', 'mission_get_all', 'REWARD', 'mission_close'])


# 日常
def daily_task():
    # 付费商店
    paid_shop()
    time.sleep(5)

    # 新人竞技场
    arena()
    time.sleep(5)

    # 防御前哨基地 一举歼灭 获取奖励
    defence_base()
    time.sleep(5)

    # 友情点
    friend_points()
    time.sleep(5)

    # 邮箱
    mail()
    time.sleep(5)

    # 远征
    trip()
    time.sleep(5)

    # 免费商店
    free_shop()
    time.sleep(5)

    # 咨询
    consult()
    time.sleep(5)

    # 模拟
    simulation_room()
    time.sleep(5)

    # 拦截
    interception()
    time.sleep(5)

    # 每日任务
    mission()
