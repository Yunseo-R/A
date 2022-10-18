import pygame
import random

# 기본 초기화 (반드시 해야하는 것들)
#################################################################################

pygame.init() # 초기화(반드시 필요!)

# 화면 크기 설정하기
screen_width = 480 # 가로
screen_height = 640 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("블럭 피하기게임") #게임이름

# FPS
clock = pygame.time.Clock()

#################################################################################

 

#################################################################################
# 1. 사용자 게임 초기화(배경화면, 게임이미지, 좌표, 속도, 폰트 등)

#배경 만들기
background = pygame.image.load("C:/Users/user/Desktop/python/pygame/pygame_basic/background.png")
#경로는 탈출문자때문에 \\로 입력하거나 역슬래시/로 바꿔줘야 제대로 로드됨


#캐릭터(스프라이트) 
character = pygame.image.load("C:/Users/user/Desktop/python/pygame/pygame_basic/character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴
character_width = character_size[0] #가로크기
character_height = character_size[1] #세로크기
character_x_pos = (screen_width / 2) - (character_width /2) #화면 가로의 정중앙 - 캐릭터 크기의 절반 왼쪽으로 빼기 = 정중앙에 출력
character_y_pos = screen_height - character_height # 화면 세로의 최하단 - 캐릭터의 크기만큼의 좌표 (위부터 출력되므로)


# 이동할 좌표 변수
to_x = 0
to_y = 0

# 이동속도
character_speed = 1

# 적 enemy 캐릭터
enemy = pygame.image.load("C:/Users/user/Desktop/python/pygame/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size #이미지의 크기를 구해옴
enemyr_width = enemy_size[0] #가로크기
enemy_height = enemy_size[1] #세로크기
enemy_x_pos = random.randint(0, screen_width - enemyr_width)
enemy_y_pos = 0
enemy_speed = 10



# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트종류, 크기) None은 기본폰트로 설정됨

# 총 시간
total_time = 30

# 시간계산
start_ticks = pygame.time.get_ticks() # 시작 tick을 받아뒀다가 나중에 빼는 방식. 파이썬 대표적인 방식


#################################################################################

# 창이 꺼지지 않게 이벤트 루프
running = True #게임이 실행중인가요?
while running :
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정함 #높을수록 부드러움


# 2. 이벤트 처리하기(키보드, 마우스 등)

    for event in pygame.event.get() :
        #파이게임을 쓰기 위해서는 무조건 적어야함. 키보드 입력이나 마우스 입력이 있는지 체크하는 코드
        if event.type == pygame.QUIT : #창이 닫히는 이벤트가 발생했나요?
            running = False # 게임 진행중이 아니네요


        if event.type == pygame.KEYDOWN : #키보드에서 키가 눌러졌나요?
            if event.key == pygame.K_LEFT : # 캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT : #캐릭터를 오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP : #캐릭터를 위로
                to_y -= character_speed
            elif event.key == pygame.K_DOWN : #캐릭터를 아래로
                to_y += character_speed

        if event.type == pygame.KEYUP : # 방향키 떼면 멈추게 하기
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                to_y = 0

    character_x_pos += to_x * dt #델타값을 곱해줌으로서 프레임이 달라져도 속도는 일정하도록 보정

# 3. 게임 캐릭터 위치 정의

    # 가로 경계값 처리하기
    if character_x_pos < 0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width :
        character_x_pos = screen_width - character_width

    enemy_y_pos += enemy_speed

    if enemy_y_pos > screen_height :
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - enemyr_width)

# 4. 충돌처리
    # 충돌처리를 위한 rect정보 업데이트 -> 적에 닿으면 쾅 하고 게임 꺼지기
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌체크 #colliderect ->충돌했는지 확인하는 함수
    if character_rect.colliderect(enemy_rect) :
        print("충돌했어요")
        running = False




    
# 5. 화면에 그리기
    screen.blit(background,(0,0)) # 배경 그리기 # 0,0위치는 좌측 최상단 기준

    screen.blit(character, (character_x_pos, character_y_pos)) #캐릭터 그리기

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) #적 캐릭터 그리기


    # 타이머 넣기
    # 경과시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #경과시간(ms)를 1000으로 나누어 초(s)단위로 표시

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255))
    # 출력할 글자, True, 글자색상 RGB값
    screen.blit(timer, (10,10))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0 :
        print("타임아웃")
        running = False

    pygame. display.update() # 게임화면에 배경 등이 그려진 채로 유지하기

# 6. 게임 종료하기

# 꺼지기 전 잠시(2초) 대기
pygame.time.delay(2000) 

# 파이게임 종료
pygame.quit()
