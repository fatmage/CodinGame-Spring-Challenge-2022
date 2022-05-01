import sys
import math

class Entity:
    def __init__(self, _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        self._id = _id
        self._type = _type
        self.x = x
        self.y = y
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.health = health
        self.vx = vx
        self.vy =vy
        self.near_base = near_base
        self.threat_for = threat_for


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

patrol_route0 = [[0,0],[0,0]]
patrol_route1 = [[0,0],[0,0]]
patrol_route2 = [[0,0],[0,0]]

# True for left side, False for right side
baseside = False

if base_x < 1000:
    baseside = True

if baseside:
    patrol_route0[0][0] = 600
    patrol_route0[0][1] = 4100
    patrol_route0[1][0] = 4300
    patrol_route0[1][1] = 860

    patrol_route1[0][0] = 1600
    patrol_route1[0][1] = 6000
    patrol_route1[1][0] = 6700
    patrol_route1[1][1] = 1400

    patrol_route2[0][0] = 10000
    patrol_route2[0][1] = 7500
    patrol_route2[1][0] = 13000
    patrol_route2[1][1] = 4000
else:
    patrol_route0[0][0] = 13000
    patrol_route0[0][1] = 8100
    patrol_route0[1][0] = 17000
    patrol_route0[1][1] = 4500

    patrol_route1[0][0] = 10500
    patrol_route1[0][1] = 7500
    patrol_route1[1][0] = 16000
    patrol_route1[1][1] = 2300

    patrol_route2[0][0] = 800
    patrol_route2[0][1] = 5100
    patrol_route2[1][0] = 5200
    patrol_route2[1][1] = 1300

h0_patrol_target = 0
h1_patrol_target = 0
h2_patrol_target = 0


def dist_base(ax, ay):
    return math.sqrt((ax-base_x)**2 + (ay-base_y)**2)

def dist_hero(mx, my, hx, hy):
    return math.sqrt((mx-hx)**2 + (my-hy)**2)

# game loop
while True:
    # health: Each player's base health
    # mana: Ignore in the first league; Spend ten mana to cast a spell
    player_health, player_mana = [int(j) for j in input().split()]
    enemy_health, enemy_mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see
    monsters = []
    heroes = []
    enemies = []
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither

        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if _type == 0:
            monsters.append(Entity(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))
        if _type == 1:
            heroes.append(Entity(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))
        if _type == 2:
            enemies.append(Entity(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))
            
    
    attacking_base = []
    moving_to_base = []
    neutral_near_enemy = []
    attacking_enemy = []
    closest_to_base = None
    closest_to_h0 = None
    closest_to_h1 = None
    closest_to_h2 = None
    enemy_near_h0 = None
    enemy_near_h1 = None
    enemy_near_h2 = None
    mana_to_spend = player_mana
    for i in range(len(monsters)):
        if monsters[i].near_base == 1 and monsters[i].threat_for == 1:
            attacking_base.append(monsters[i])
        if monsters[i].near_base == 0 and monsters[i].threat_for == 1:
            moving_to_base.append(monsters[i])
        if monsters[i].threat_for == 1:
            if closest_to_base == None:
                closest_to_base = monsters[i]
            elif dist_base(monsters[i].x ,monsters[i].y) < dist_base(closest_to_base.x, closest_to_base.y):
                closest_to_base = monsters[i]
            if closest_to_h0 == None:
                closest_to_h0 = monsters[i]
            elif dist_hero(monsters[i].x ,monsters[i].y, heroes[0].x, heroes[0].y) < dist_hero(closest_to_h0.x, closest_to_h0.y,heroes[0].x, heroes[0].y):
                closest_to_h0 = monsters[i]
            if closest_to_h1 == None:
                closest_to_h1 = monsters[i]
            elif dist_hero(monsters[i].x ,monsters[i].y, heroes[1].x, heroes[1].y) < dist_hero(closest_to_h1.x, closest_to_h1.y,heroes[1].x, heroes[1].y):
                closest_to_h1 = monsters[i]
        if monsters[i].threat_for == 0 and dist_hero(heroes[2].x, heroes[2].y, monsters[i].x, monsters[i].y) <= 2200:
            neutral_near_enemy.append(monsters[i])
        if monsters[i].threat_for == 2 and dist_hero(heroes[2].x, heroes[2].y, monsters[i].x, monsters[i].y <= 2200):
            attacking_enemy.append(monsters[i])

    for i in range(len(enemies)):
        if enemy_near_h0 == None and dist_hero(enemies[i].x, enemies[i].y, heroes[0].x, heroes[0].y) <= 2200:
            enemy_near_h0 = enemies[i]
        elif enemy_near_h0 != None and dist_hero(enemies[i].x, enemies[i].y, heroes[0].x, heroes[0].y) < dist_hero(enemy_near_h0.x, enemy_near_h0.y, heroes[0].x, heroes[0].y):
            enemy_near_h0 = enemies[i]
        if enemy_near_h1 == None and dist_hero(enemies[i].x, enemies[i].y, heroes[1].x, heroes[1].y) <= 2200:
            enemy_near_h1 = enemies[i]
        elif enemy_near_h1 != None and dist_hero(enemies[i].x, enemies[i].y, heroes[1].x, heroes[1].y) < dist_hero(enemy_near_h1.x, enemy_near_h1.y, heroes[1].x, heroes[1].y):
            enemy_near_h1 = enemies[i]
        if enemy_near_h2 == None and dist_hero(enemies[i].x, enemies[i].y, heroes[2].x, heroes[2].y) <= 2200:
            enemy_near_h2 = enemies[i]
        elif enemy_near_h2 != None and dist_hero(enemies[i].x, enemies[i].y, heroes[2].x, heroes[2].y) < dist_hero(enemy_near_h2.x, enemy_near_h2.y, heroes[2].x, heroes[2].y):
            enemy_near_h2 = enemies[i]

    # HERO 0 defends base, shields himself
    if enemy_near_h0 != None and mana_to_spend >= 10 and heroes[0].shield_life == 0:
        print('SPELL SHIELD', heroes[0]._id, 'h0 shield')
        mana_to_spend = mana_to_spend - 10
    elif len(attacking_base) > 0:
        if mana_to_spend >= 10 and dist_hero(heroes[0].x, heroes[0].y, closest_to_base.x, closest_to_base.y) <= 1280:
            if baseside:
                print('SPELL WIND', heroes[0].x+1612, heroes[0].y+1612, 'h0 wind')
            else: 
                print('SPELL WIND', heroes[0].x-1612, heroes[0].y-1612, 'h0 wind')
            mana_to_spend = mana_to_spend - 10
        else:
            print('MOVE', closest_to_base.x, closest_to_base.y)
    else:
        if heroes[0].x == patrol_route0[h0_patrol_target][0] and heroes[0].y == patrol_route0[h0_patrol_target][1]:
            h0_patrol_target = 1 - h0_patrol_target
        print('MOVE', patrol_route0[h0_patrol_target][0], patrol_route0[h0_patrol_target][1])

    # HERO 1 patrols surroundings and defends base from spiders and enemies
    if enemy_near_h1 != None and mana_to_spend >= 10:
        if enemy_near_h1.shield_life != 0 and heroes[1].shield_life == 0:
            print('SPELL SHIELD', heroes[1]._id, 'h1 shield')
            mana_to_spend = mana_to_spend - 10
        elif enemy_near_h1.shield_life != 0:
            print('MOVE', patrol_route1[h1_patrol_target][0], patrol_route1[h1_patrol_target][1])
        else:
            if baseside:
                print('SPELL CONTROL', enemy_near_h1._id, 18000,9000, 'h1 control')
            else:
                print('SPELL CONTROL', enemy_near_h1._id, 0, 0, 'h1 control')
            mana_to_spend = mana_to_spend - 10        
    elif len(attacking_base) > 1:
        if mana_to_spend >= 10 and dist_hero(heroes[0].x, heroes[0].y, closest_to_h0.x, closest_to_h0.y) <= 1280:
            if baseside:
                print('SPELL WIND', heroes[1].x+1612, heroes[1].y+1612, 'h1 wind')
            else: 
                 print('SPELL WIND', heroes[1].x-1612, heroes[1].y-1612, 'h1 wind')
            mana_to_spend = mana_to_spend - 10
        else:
            print('MOVE', closest_to_base.x, closest_to_base.y)
    elif len(moving_to_base) > 0:
        print('MOVE', moving_to_base[0].x, moving_to_base[0].y)
    else:
        if heroes[1].x == patrol_route1[h1_patrol_target][0] and heroes[1].y == patrol_route1[h1_patrol_target][1]:
            h1_patrol_target = 1 - h1_patrol_target
        print('MOVE', patrol_route1[h1_patrol_target][0], patrol_route1[h1_patrol_target][1])

    # HERO 2 attacks the enemy base

    if len(neutral_near_enemy) > 0 and mana_to_spend >= 10 and neutral_near_enemy[0].shield_life == 0:
        if baseside:
            print('SPELL CONTROL', neutral_near_enemy[0]._id, 18000, 9000, 'h2 control spider')
        else:
            print('SPELL CONTROL', neutral_near_enemy[0]._id, 0, 0, 'h2 control spider')
        
        mana_to_spend = mana_to_spend - 10
    elif len(attacking_enemy) > 0 and mana_to_spend >= 10 and attacking_enemy[0].shield_life == 0 and dist_hero(heroes[2].x, heroes[2].y, attacking_enemy[0].x, attacking_enemy[0].y) <= 1280:
        if baseside:
            print('SPELL WIND', 18000, 9000, 'h2 wind spider')
        else:
            print('SPELL WIND', 0, 0, 'h2 wind spider')
        mana_to_spend = mana_to_spend - 10
    elif enemy_near_h2 != None and mana_to_spend >= 10 and enemy_near_h2.shield_life == 0 and dist_hero(heroes[2].x, heroes[2].y, enemy_near_h2.x, enemy_near_h2.y) <= 1280:
        if baseside:
            print('SPELL WIND', 18000, 9000, 'h2 wind enemy')
        else:
            print('SPELL WIND', 0, 0, 'h2 wind enemy')
        mana_to_spend = mana_to_spend - 10
    else:
        if baseside:
            if heroes[2].x < 10000 or heroes[2].y < 4000 or len(neutral_near_enemy) == 0:
                if heroes[2].x == patrol_route2[h2_patrol_target][0] and heroes[2].y == patrol_route2[h2_patrol_target][1]:
                    h2_patrol_target = 1 - h2_patrol_target
                print('MOVE', patrol_route2[h2_patrol_target][0], patrol_route2[h2_patrol_target][1])
            else:
                print('MOVE', neutral_near_enemy[0].x, neutral_near_enemy[0].y)
        else:
            if heroes[2].x > 10000 or heroes[2].y > 4000 or len(neutral_near_enemy) == 0:
                if heroes[2].x == patrol_route2[h2_patrol_target][0] and heroes[2].y == patrol_route2[h2_patrol_target][1]:
                    h2_patrol_target = 1 - h2_patrol_target
                print('MOVE', patrol_route2[h2_patrol_target][0], patrol_route2[h2_patrol_target][1])
            else:
                print('MOVE', neutral_near_enemy[0].x, neutral_near_enemy[0].y)
    #else:
    #    if heroes[2].x == patrol_route2[h2_patrol_target][0] and heroes[2].y == patrol_route2[h2_patrol_target][1]:
    #        h2_patrol_target = 1 - h2_patrol_target
    #    print('MOVE', patrol_route2[h2_patrol_target][0], patrol_route2[h2_patrol_target][1])

