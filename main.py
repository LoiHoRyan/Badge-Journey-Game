# -*- coding: utf-8 -*-
import os, json, sys, pygame, math
try:
    import cv2
except Exception:
    cv2=None
from settings import *
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
def path(p): return os.path.join(BASE_DIR,p)
def clamp(v,a,b): return max(a,min(b,v))
def load_image(p,size=None,smooth=False):
    try: img=pygame.image.load(path(p)).convert_alpha()
    except Exception:
        img=pygame.Surface((60,60),pygame.SRCALPHA); img.fill((255,0,255,180)); pygame.draw.rect(img,(0,0,0),img.get_rect(),3)
    if size: img=pygame.transform.smoothscale(img,size) if smooth else pygame.transform.scale(img,size)
    return img
def get_font(sz):
    fp=path('assets/font/Minecraft.ttf')
    return pygame.font.Font(fp,sz) if os.path.exists(fp) else pygame.font.SysFont('consolas',sz,bold=True)

def find_video_file(names):
    """Tìm mp4 linh hoạt: ưu tiên assets/scenes, nhưng cũng nhận file đặt ở thư mục gốc.
    Chấp nhận cả tên có/không có .mp4 và không phân biệt hoa thường.
    """
    candidates=[]
    for name in names:
        base=os.path.splitext(name)[0]
        for folder in ('assets/scenes','assets/Scenes','.'):
            candidates.append(os.path.join(folder, base+'.mp4'))
            candidates.append(os.path.join(folder, base+'.MP4'))
            candidates.append(os.path.join(folder, base))
    for rel in candidates:
        if os.path.exists(path(rel)):
            return path(rel)
    # quét thư mục để tránh lỗi Windows ẩn đuôi file hoặc khác hoa/thường
    wanted={os.path.splitext(n)[0].lower() for n in names}
    for folder in (path('assets/scenes'), BASE_DIR):
        if os.path.isdir(folder):
            for fn in os.listdir(folder):
                stem,ext=os.path.splitext(fn)
                if stem.lower() in wanted and ext.lower()=='.mp4':
                    return os.path.join(folder,fn)
    return None

def wrap_text(text, font_obj, max_width):
    words=str(text).split(' ')
    lines=[]; current=''
    for word in words:
        test=word if not current else current+' '+word
        if font_obj.size(test)[0] <= max_width:
            current=test
        else:
            if current: lines.append(current)
            current=word
    if current: lines.append(current)
    return lines

def draw_wrapped_text(surface, text, font_obj, color, x, y, max_width, line_gap=6, center=False):
    for line in wrap_text(text, font_obj, max_width):
        img=font_obj.render(line, True, color)
        rect=img.get_rect()
        if center:
            rect.centerx=x+max_width//2; rect.y=y
        else:
            rect.topleft=(x,y)
        surface.blit(img, rect)
        y += img.get_height()+line_gap
    return y

class VideoPlayer:
    def __init__(self, names, fallback_surface=None, size=(WIDTH, HEIGHT)):
        self.size=size; self.fallback=fallback_surface
        self.video_path=find_video_file(names)
        self.cap=None; self.fps=30; self.frame=None; self.last_tick=0
        self.error=''
        if self.video_path and cv2 is not None:
            self.open()
        elif self.video_path and cv2 is None:
            self.error='Chưa cài opencv-python để đọc MP4'
        else:
            self.error='Không tìm thấy file MP4'
    def open(self):
        try:
            self.cap=cv2.VideoCapture(self.video_path)
            if not self.cap or not self.cap.isOpened():
                self.cap=None; self.error='Không mở được MP4'; return
            fps=self.cap.get(cv2.CAP_PROP_FPS)
            self.fps=fps if fps and fps>1 else 30
        except Exception as e:
            self.cap=None; self.error=str(e)
    def reset(self):
        if self.cap:
            try: self.cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            except Exception: pass
    def draw(self, surface):
        if not self.cap:
            if self.fallback: surface.blit(self.fallback,(0,0))
            else: surface.fill((0,0,0))
            # hiện cảnh báo nhỏ thay vì chỉ màn hồng để biết lỗi nằm ở đâu
            try:
                f=pygame.font.SysFont('consolas',20,bold=True)
                msg=self.error or 'MP4 chưa sẵn sàng'
                img=f.render(msg,True,(255,255,255)); bg=pygame.Surface((img.get_width()+24,img.get_height()+16),pygame.SRCALPHA); bg.fill((0,0,0,170))
                surface.blit(bg,(20,20)); surface.blit(img,(32,28))
            except Exception: pass
            return
        now=pygame.time.get_ticks()
        if self.frame is None or now-self.last_tick >= int(1000/max(1,self.fps)):
            ok, frame=self.cap.read()
            if not ok:
                self.reset(); ok, frame=self.cap.read()
            if ok:
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame=cv2.resize(frame,self.size)
                self.frame=pygame.image.frombuffer(frame.tobytes(),self.size,'RGB').convert()
            self.last_tick=now
        if self.frame: surface.blit(self.frame,(0,0))
        elif self.fallback: surface.blit(self.fallback,(0,0))
        else: surface.fill((0,0,0))
QUESTION_BANK={1: [('Số liền sau của số 9 là số nào?', ['8', '10', '7', '11'], 1, 'Số liền sau của 9 là 10.'), ("Từ nào dưới đây có tiếng chứa âm 'ch'?", ['Con cá', 'Cái chổi', 'Viên phấn', 'Quả bóng'], 1, "Từ 'chổi' có âm đầu là 'ch'."), ('Phép tính nào dưới đây có kết quả nhỏ nhất?', ['2 + 3', '5 - 1', '6 - 4', '1 + 2'], 2, '6 - 4 = 2 là nhỏ nhất.'), ('Điền vần: Che chở cho con, đó là tình m____.', ['ẹ', 'a', 'u', 'ơ'], 0, "Ghép vần 'ẹ' được từ mẹ."), ('Bộ phận nào giúp em nghe thấy tiếng nhạc?', ['Mắt', 'Mũi', 'Tai', 'Tay'], 2, 'Tai giúp nghe âm thanh.'), ('Hình nào có 3 cạnh?', ['Hình vuông', 'Hình tròn', 'Hình tam giác', 'Hình chữ nhật'], 2, 'Hình tam giác có 3 cạnh.'), ('Khi gặp thầy cô giáo, em nên làm gì?', ['Đi thẳng', 'Khoanh tay chào lễ phép', 'Chạy trốn', 'Chỉ tay nói to'], 1, 'Chào lễ phép thể hiện kính trọng.'), ('Từ nào viết đúng chính tả?', ['Gà trống', 'Gà giống', 'Gà rống', 'Gà chông'], 0, 'Viết đúng là gà trống.'), ('AB dài 4cm, BC dài 5cm. Cả hai dài bao nhiêu?', ['8cm', '9cm', '10cm', '1cm'], 1, '4 + 5 = 9cm.'), ('Đâu là con vật nuôi quen thuộc?', ['Con hổ', 'Con sư tử', 'Con mèo', 'Con gấu'], 2, 'Con mèo là vật nuôi quen thuộc.')], 2: [('Tìm x, biết x - 15 = 20.', ['x = 5', 'x = 35', 'x = 25', 'x = 15'], 1, 'x = 20 + 15 = 35.'), ('Từ nào chỉ hoạt động của học sinh?', ['Đọc sách', 'Sách giáo khoa', 'Trường học', 'Chăm chỉ'], 0, 'Đọc sách là hoạt động.'), ('Một ngày có bao nhiêu giờ?', ['12 giờ', '24 giờ', '60 giờ', '48 giờ'], 1, 'Một ngày có 24 giờ.'), ('Cơ quan nào giúp chúng ta thở?', ['Tim', 'Dạ dày', 'Phổi', 'Não'], 2, 'Phổi giúp cơ thể thở.'), ('Từ nào trái nghĩa với khen ngợi?', ['Chê bai', 'Yêu mến', 'Tuyên dương', 'Thưởng'], 0, 'Trái nghĩa là chê bai.'), ('Kết quả của 5 × 4 + 10 là:', ['20', '30', '40', '14'], 1, '5×4=20, 20+10=30.'), ('Từ nào chỉ màu xanh da trời?', ['Red', 'Green', 'Yellow', 'Blue'], 3, 'Blue là xanh dương.'), ('Làm đổ hộp bút của bạn, em cần làm gì?', ['Bỏ chạy', 'Nhặt giúp và xin lỗi', 'Đổ lỗi', 'Cười lớn'], 1, 'Cần nhặt giúp và xin lỗi.'), ('Số lớn nhất có hai chữ số là?', ['10', '90', '99', '100'], 2, 'Số lớn nhất có hai chữ số là 99.'), ('Cây hấp thụ nước chủ yếu bằng bộ phận nào?', ['Lá', 'Hoa', 'Thân', 'Rễ'], 3, 'Rễ hút nước và dinh dưỡng.')], 3: [('Số gồm 3 nghìn, 5 trăm và 2 đơn vị là:', ['352', '3520', '3502', '3052'], 2, 'Viết là 3502.'), ("Bộ phận trả lời 'Để làm gì?' trong câu: Em chăm học để bố mẹ vui lòng.", ['Em chăm học', 'để bố mẹ vui lòng', 'bố mẹ vui lòng', 'học để bố mẹ vui lòng'], 1, 'Đó là bộ phận chỉ mục đích.'), ('HCN dài 8cm, rộng 5cm. Diện tích là:', ['40 cm²', '26cm', '13 cm²', '40cm'], 0, '8×5=40 cm².'), ('Trái Đất quay quanh Mặt Trời mất bao lâu?', ['1 ngày', '1 tháng', '1 năm', '1 tuần'], 2, 'Khoảng 1 năm.'), ('Từ nào chỉ người làm việc trí thức?', ['Bác sĩ', 'Công nhân', 'Thợ may', 'Nông dân'], 0, 'Bác sĩ là lao động trí thức.'), ('84 : 4 bằng bao nhiêu?', ['20', '21', '22', '12'], 1, '84:4=21.'), ('Xóa ký tự trước con trỏ dùng phím nào?', ['Enter', 'Caps Lock', 'Backspace', 'Delete'], 2, 'Backspace xóa bên trái con trỏ.'), ('How _____ is she?', ['many', 'old', 'much', 'long'], 1, 'Hỏi tuổi dùng How old.'), ('Số chia là 6, số dư lớn nhất là:', ['6', '7', '5', '1'], 2, 'Số dư nhỏ hơn số chia, lớn nhất là 5.'), ('Nhạc cụ phát âm thanh bằng cách gảy dây?', ['Đàn sáo', 'Đàn tranh', 'Kèn Trumpet', 'Trống'], 1, 'Đàn tranh dùng dây đàn.')], 4: [('Giá trị chữ số 7 trong 475.210 là:', ['700', '7.000', '70.000', '700.000'], 2, '7 ở hàng chục nghìn.'), ("Chủ ngữ trong câu 'Đoàn thuyền đánh cá buồm căng gió ra khơi.' là:", ['Đoàn thuyền', 'Đoàn thuyền đánh cá', 'Buồm căng gió', 'Đoàn thuyền đánh cá buồm căng gió'], 1, 'Chủ ngữ là Đoàn thuyền đánh cá.'), ('Phân số nào bằng 2/3?', ['4/9', '6/9', '6/8', '2/6'], 1, '6/9 rút gọn được 2/3.'), ('Nước đóng băng ở nhiệt độ nào?', ['100°C', '37°C', '10°C', '0°C'], 3, 'Nước đóng băng ở 0°C.'), ('Ai lấy thân mình lấp lỗ châu mai?', ['Phan Đình Giót', 'Bế Văn Đàn', 'Tô Vĩnh Diện', 'Kim Đồng'], 0, 'Đó là Phan Đình Giót.'), ('Đồng bằng lớn nhất nước ta là:', ['Đồng bằng Bắc Bộ', 'Đồng bằng Nam Bộ', 'Duyên hải miền Trung', 'Sông Hồng'], 1, 'Đồng bằng Nam Bộ lớn nhất.'), ('Lớp 35 HS, nữ bằng 3/5. Có bao nhiêu nam?', ['21', '14', '15', '20'], 1, 'Nữ 21, nam 14.'), ('Từ nào là từ láy?', ['Mặt mũi', 'Long lanh', 'Sách vở', 'Tươi tốt'], 1, 'Long lanh là từ láy.'), ('Thực vật tự tổng hợp dinh dưỡng nhờ quá trình nào?', ['Hô hấp', 'Thoát hơi nước', 'Quang hợp', 'Hút nước'], 2, 'Quang hợp giúp cây tạo dinh dưỡng.'), ('Yesterday, my family _____ to the zoo.', ['go', 'goes', 'went', 'going'], 2, 'Yesterday dùng quá khứ: went.')], 5: [("Số thập phân 'Không đơn vị, hai mươi lăm phần trăm' là:", ['0,25', '0,025', '25,0', '0,205'], 0, 'Viết là 0,25.'), ('Vì... nên... biểu thị quan hệ gì?', ['Giả thiết - Kết quả', 'Nguyên nhân - Kết quả', 'Tương phản', 'Tăng tiến'], 1, 'Đó là quan hệ nguyên nhân - kết quả.'), ('Diện tích hình tròn bán kính 2cm là:', ['6,28 cm²', '12,56 cm²', '12,56 cm', '3,14 cm²'], 1, 'S=2×2×3,14=12,56.'), ('Chất nào tồn tại ở cả 3 thể?', ['Sắt', 'Không khí', 'Nước', 'Thủy ngân'], 2, 'Nước có rắn, lỏng, khí.'), ('Ngày Quốc khánh Việt Nam là:', ['30/4', '19/8', '2/9', '22/12'], 2, 'Quốc khánh là 2/9.'), ('Đất liền Việt Nam nằm trên bán đảo nào?', ['Đông Dương', 'Triều Tiên', 'Mã Lai', 'Ả Rập'], 0, 'Việt Nam nằm trên bán đảo Đông Dương.'), ('Ô tô đi 50 km/giờ trong 2,5 giờ. Quãng đường là:', ['125 km', '20 km', '100 km', '12,5 km'], 0, '50×2,5=125 km.'), ('Thành ngữ nào nói về dũng cảm?', ['Kề vai sát cánh', 'Vào sinh ra tử', 'Uống nước nhớ nguồn', 'Nhường cơm sẻ áo'], 1, 'Vào sinh ra tử chỉ sự dũng cảm.'), ('Nguồn năng lượng sạch và vô tận là:', ['Than đá', 'Dầu mỏ', 'Năng lượng mặt trời', 'Khí đốt'], 2, 'Năng lượng mặt trời là sạch và vô tận.'), ('She is the _____ student in my class.', ['good', 'better', 'best', 'well'], 2, 'So sánh nhất của good là best.')]}
class Audio:
    def __init__(self):
        self.enabled=True; self.music_enabled=True; self.sound_enabled=True; self.current=None; self.sounds={}
        try: pygame.mixer.init()
        except Exception: self.enabled=False
    def load(self):
        if not self.enabled: return
        for k,rel in SOUND_FILES.items():
            fp=path(rel)
            if os.path.exists(fp):
                try: self.sounds[k]=pygame.mixer.Sound(fp)
                except Exception: pass
    def play_music(self,name):
        if not self.enabled: return
        rel=LEVEL_MUSIC.get(name) if isinstance(name,int) else MUSIC_FILES.get(name)
        if not rel: return
        fp=path(rel)
        if not os.path.exists(fp): return
        if self.current==rel and pygame.mixer.music.get_busy(): return
        self.current=rel
        if not self.music_enabled: return
        try: pygame.mixer.music.load(fp); pygame.mixer.music.play(-1)
        except Exception: pass
    def toggle_music(self):
        self.music_enabled=not self.music_enabled
        if not self.enabled: return
        if not self.music_enabled: pygame.mixer.music.stop()
        else: self.current=None
    def toggle_sound(self): self.sound_enabled=not self.sound_enabled
    def sound(self,k):
        if self.enabled and self.sound_enabled and k in self.sounds:
            try: self.sounds[k].play()
            except Exception: pass
class Player:
    def __init__(self,imgs,start):
        self.imgs=imgs; self.rect=pygame.Rect(start[0],start[1],46,55); self.x=float(self.rect.x); self.y=float(self.rect.y); self.vx=0; self.vy=0; self.facing=1; self.on_ground=False; self.jumps=2; self.health=MAX_HEALTH; self.attack=0; self.inv=0; self.dmg_cd=0; self.dead=False
    def hurt(self,n=1,force=False):
        if not force and (self.inv>0 or self.dead): return False
        self.health-=n
        if not force: self.inv=INVINCIBLE_TIME
        if self.health<=0: self.health=0; self.dead=True
        return True
    def jump(self):
        if self.jumps>0: self.vy=DOUBLE_JUMP_POWER if self.jumps==1 else JUMP_POWER; self.jumps-=1; self.on_ground=False
    def attack_now(self): self.attack=ATTACK_TIME
    def attack_rect(self):
        if self.attack<=0: return pygame.Rect(0,0,0,0)
        return pygame.Rect(self.rect.right-4,self.rect.y-16,64,88) if self.facing==1 else pygame.Rect(self.rect.left-60,self.rect.y-16,64,88)
    def update(self,plats,spawn,keys):
        self.vx=0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.vx=-PLAYER_SPEED; self.facing=-1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.vx=PLAYER_SPEED; self.facing=1
        self.x+=self.vx; self.rect.x=round(self.x); old_bottom=self.rect.bottom
        self.vy=min(self.vy+GRAVITY,MAX_FALL_SPEED); self.y+=self.vy; self.rect.y=round(self.y); self.on_ground=False
        if self.vy>=0:
            for p in plats+[spawn]:
                r=pygame.Rect(p)
                if self.rect.colliderect(r) and old_bottom<=r.top+10:
                    self.rect.bottom=r.top; self.y=self.rect.y; self.vy=0; self.jumps=2; self.on_ground=True; break
        if self.attack>0: self.attack-=1
        if self.inv>0: self.inv-=1
        if self.dmg_cd>0: self.dmg_cd-=1
        self.rect.x=clamp(self.rect.x,-20,WIDTH-25); self.x=self.rect.x
    def draw_sword_wave(self,screen):
        # Sóng kiếm đậm hơn và bên trái được mirror từ bên phải để không bị ngược vòng cung.
        progress=(ATTACK_TIME-self.attack)/max(1,ATTACK_TIME)
        alpha=max(185, int(255*(1-progress*0.25)))
        wave=pygame.Surface((78,124), pygame.SRCALPHA)
        cx,cy=22+int(progress*10),62
        pygame.draw.arc(wave,(255,255,235,alpha),(cx-10,cy-56,42,112),-1.35,1.35,11)
        pygame.draw.arc(wave,(255,190,45,alpha),(cx-2,cy-50,34,100),-1.25,1.25,7)
        pygame.draw.arc(wave,(255,115,25,alpha),(cx+7,cy-42,24,84),-1.10,1.10,4)
        pygame.draw.line(wave,(255,255,255,alpha),(cx+25,cy-42),(cx+30,cy+42),4)
        if self.facing==1:
            screen.blit(wave,(self.rect.right+5,self.rect.y-36))
        else:
            wave=pygame.transform.flip(wave,True,False)
            screen.blit(wave,(self.rect.left-83,self.rect.y-36))
    def draw(self,screen):
        key='ar' if self.facing==1 and self.attack>0 else 'al' if self.attack>0 else 'r' if self.facing==1 else 'l'
        if self.inv>0 and (self.inv//5)%2==0: return
        img=self.imgs[key]; screen.blit(img,img.get_rect(midbottom=self.rect.midbottom))
        if self.attack>0: self.draw_sword_wave(screen)
def draw_outline_text(surface,font,text,color,pos,outline=(0,0,0),width=1,center=False):
    img=font.render(text,True,color); rect=img.get_rect()
    if center: rect.center=pos
    else: rect.topleft=pos
    for ox in range(-width,width+1):
        for oy in range(-width,width+1):
            if (ox or oy) and ox*ox+oy*oy<=width*width: surface.blit(font.render(text,True,outline),rect.move(ox,oy))
    surface.blit(img,rect)

def make_attack_wave_surface():
    s=pygame.Surface((86,126),pygame.SRCALPHA)
    pygame.draw.arc(s,(255,255,235,255),(8,5,48,112),-1.35,1.35,11)
    pygame.draw.arc(s,(255,190,45,250),(16,11,42,100),-1.25,1.25,7)
    pygame.draw.arc(s,(255,110,25,240),(26,19,31,84),-1.10,1.10,4)
    pygame.draw.line(s,(255,255,255,255),(54,22),(62,104),4); return s

class SkillWave:
    def __init__(self,x,y,d): self.rect=pygame.Rect(x,y,74,100); self.x=float(x); self.d=d; self.travel=0; self.hit_ids=set(); self.alive=True
    def update(self):
        self.x+=11*self.d; self.travel+=11; self.rect.x=round(self.x)
        if self.travel>=SKILL_WAVE_RANGE or self.rect.right<0 or self.rect.left>WIDTH: self.alive=False
    def draw(self,screen):
        s=make_attack_wave_surface()
        if self.d<0: s=pygame.transform.flip(s,True,False)
        screen.blit(s,s.get_rect(center=self.rect.center))

class StarBladeBurst:
    def __init__(self,center,d): self.cx=float(center[0]); self.cy=float(center[1]); self.d=d; self.rotation=0; self.alive=True; self.hit_ids=set(); self.rect=pygame.Rect(0,0,220,220); self.rect.center=center
    def update(self):
        self.cx+=10*self.d; self.rotation=(self.rotation+14*self.d)%360; self.rect.center=(round(self.cx),round(self.cy))
        if self.rect.right<0 or self.rect.left>WIDTH: self.alive=False
    def draw(self,screen):
        s=pygame.Surface((230,230),pygame.SRCALPHA); base=pygame.transform.smoothscale(make_attack_wave_surface(),(76,112))
        for angle in (45,135,225,315):
            blade=pygame.transform.rotate(base,angle-90); r=math.radians(angle); x=115+int(math.cos(r)*35); y=115-int(math.sin(r)*35); s.blit(blade,blade.get_rect(center=(x,y)))
        pygame.draw.circle(s,(255,245,175,245),(115,115),16); pygame.draw.circle(s,(255,190,45,220),(115,115),27,4)
        spin=pygame.transform.rotate(s,self.rotation); screen.blit(spin,spin.get_rect(center=self.rect.center))

class Enemy:
    def __init__(self,d,img):
        self.img=img; self.rect=pygame.Rect(d['x'],d['y'],46,46); self.x=float(self.rect.x); self.left=d.get('patrol_left',self.rect.x-80); self.right=max(d.get('patrol_right',self.rect.x+80),self.left+80); self.speed=d.get('speed',1.2); self.dir=1; self.hp=d.get('hp',3); self.max_hp=self.hp; self.hit=0
    @property
    def alive(self): return self.hp>0
    def update(self):
        self.x+=self.speed*self.dir
        if self.x<self.left: self.x=self.left; self.dir=1
        if self.x>self.right: self.x=self.right; self.dir=-1
        self.rect.x=round(self.x); self.hit=max(0,self.hit-1)
    def damage(self,amount=1):
        if self.hit>0: return False
        self.hp-=amount; self.hit=12; return True
    def draw(self,screen):
        img=pygame.transform.flip(self.img,True,False) if self.dir<0 else self.img
        if self.hit>0: img=img.copy(); img.fill((255,80,80,80),special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(img,img.get_rect(midbottom=self.rect.midbottom))
        if self.hp<self.max_hp:
            pygame.draw.rect(screen,(60,0,0),(self.rect.x,self.rect.y-8,self.rect.w,5)); pygame.draw.rect(screen,(255,70,70),(self.rect.x,self.rect.y-8,int(self.rect.w*self.hp/self.max_hp),5))
class Boss(Enemy):
    def __init__(self,d,img): super().__init__(d,img); self.rect=pygame.Rect(d['x'],d['y'],210,150); self.x=float(self.rect.x); self.hp=d.get('hp',30); self.max_hp=self.hp; self.fire=0
    def update(self): super().update(); self.fire=(self.fire+1)%180
    def fire_rect(self):
        if not (45<self.fire<95): return pygame.Rect(0,0,0,0)
        # Ảnh gốc rồng quay/phun sang trái. Khi đi sang phải phải lật ảnh và đặt lửa bên phải, tránh phun từ đuôi.
        return pygame.Rect(self.rect.right-16,self.rect.y+54,150,46) if self.dir>0 else pygame.Rect(self.rect.left-136,self.rect.y+54,150,46)
    def draw(self,screen):
        # Fix: dir > 0 thì lật ảnh để đầu/miệng rồng quay sang phải; dir < 0 giữ ảnh gốc quay trái.
        img=pygame.transform.flip(self.img,True,False) if self.dir>0 else self.img
        screen.blit(img,img.get_rect(midbottom=self.rect.midbottom)); fr=self.fire_rect()
        if fr.w:
            pygame.draw.rect(screen,(255,90,0,180),fr,border_radius=18); pygame.draw.rect(screen,(255,220,80),fr.inflate(-25,-18),border_radius=12)
        pygame.draw.rect(screen,(35,0,0),(281,145,590,22),border_radius=6); pygame.draw.rect(screen,(255,55,35),(281,145,int(590*self.hp/self.max_hp),22),border_radius=6); pygame.draw.rect(screen,(255,220,120),(281,145,590,22),3,border_radius=6)
class Game:
    def __init__(self):
        pygame.init(); self.audio=Audio(); info=pygame.display.Info(); self.display=pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE); self.screen=pygame.Surface((WIDTH,HEIGHT)).convert_alpha(); pygame.display.set_caption(TITLE); self.clock=pygame.time.Clock(); self.f=get_font(28); self.big=get_font(58); self.small=get_font(18); self.state='opening'; self.idx=0; self.grade=None; self.full=False; self.question_attempts=0; self.question_feedback=None; self.question_locked=False; self.question_result_until=0; self.mana=MAX_MANA; self.mana_regen_tick=0; self.mana_flash=0; self.skill_msg=''; self.skill_msg_time=0; self.cooldowns={'Q':0,'E':0,'R':0,'T':0}; self.shield_time=0; self.dash_inv_time=0; self.skill_waves=[]; self.star_bursts=[]; self.dash_trails=[]; self.load_assets(); self.load_levels(); self.audio.load(); self.audio.play_music('opening')
    def load_assets(self):
        # Fallback ảnh cũ nếu chưa có MP4 hoặc chưa cài opencv-python.
        self.opening_img=load_image('assets/scenes/opening.png',(WIDTH,HEIGHT),True)
        self.tutorial_img=load_image('assets/scenes/tutorial.png',(WIDTH,HEIGHT),True)
        self.ending_img=load_image('assets/scenes/ending.png',(WIDTH,HEIGHT),True)
        # MP4 tự lặp lại cho tới khi người chơi bấm Enter/Tab.
        self.videos={
            'opening': VideoPlayer(['opening','Opening'], self.opening_img),
            'tutorial': VideoPlayer(['tutorial','Tutorial','Hướng dẫn chơi'], self.tutorial_img),
            'ending': VideoPlayer(['ending','Ending'], self.ending_img),
        }
        self.hfull=load_image('assets/ui/heart_full.png',(42,42)); self.hempty=load_image('assets/ui/heart_empty.png',(42,42)); self.coin_img=load_image('assets/items/coin.png',(34,34)); self.pimgs={'r':load_image('assets/player/right.png',(56,62),True),'l':load_image('assets/player/left.png',(56,62),True),'ar':load_image('assets/player/attack_right.png',(78,62),True),'al':load_image('assets/player/attack_left.png',(78,62),True)}; fs={'slime':'enemy_1_slime.png','hedgehog':'enemy_2_hedgehog.png','scorpion':'enemy_3_scorpion.png','frog':'enemy_4_frog.png','snowman':'enemy_5_snowman.png','fire_imp':'enemy_6_fire_imp.png','guard':'enemy_7_guard.png','robot_guard':'enemy_8_robot_guard.png','alien':'enemy_9_alien.png'}; self.eimgs={k:load_image('assets/enemies/'+v,(54,54)) for k,v in fs.items()}; self.boss_img=load_image('assets/boss/dragon.png',(240,190),True); self.shield_effect=load_image('assets/ui/skills/skill_shield.png',(70,70),True); self.skill_icons={'Q':load_image('assets/ui/skills/skill_wave.png',(48,48),True),'E':load_image('assets/ui/skills/skill_shield.png',(48,48),True),'R':load_image('assets/ui/skills/skill_dash.png',(48,48),True),'T':load_image('assets/ui/skills/skill_storm.png',(48,48),True)}
    def load_levels(self):
        self.levels=json.load(open(path('data/levels.json'),encoding='utf-8'))['levels']; self.bgs=[load_image(l['background'],(WIDTH,HEIGHT),True) for l in self.levels]; self.load_level(0)
    def load_level(self,i):
        self.idx=i; self.lvl=self.levels[i]; self.lvl['player_start']=[self.lvl['spawn'][0]+20,self.lvl['spawn'][1]-58]; self.player=Player(self.pimgs,self.lvl['player_start']); self.coins=[{'rect':pygame.Rect(c[0],c[1],34,34),'got':False} for c in self.lvl['coins']]; self.enemies=[Enemy(e,self.eimgs.get(e['type'],self.eimgs['slime'])) for e in self.lvl['enemies']]; self.boss=Boss(self.lvl['boss'],self.boss_img) if self.lvl.get('boss') else None; self.collected=0; self.start_ticks=pygame.time.get_ticks(); self.mana=MAX_MANA; self.mana_regen_tick=0; self.cooldowns={'Q':0,'E':0,'R':0,'T':0}; self.shield_time=0; self.dash_inv_time=0; self.skill_waves=[]; self.star_bursts=[]; self.dash_trails=[]; self.audio.play_music(i+1)
    def present(self): self.display.blit(pygame.transform.smoothscale(self.screen,self.display.get_size()),(0,0)); pygame.display.flip()
    def start_question(self): self.state='question'; self.question_attempts=0; self.question_feedback=None; self.question_locked=False; self.question_result_until=0; self.audio.play_music('question')
    def current_question(self):
        q,o,a,e=QUESTION_BANK[self.grade][self.idx]; return {'q':q,'opts':o,'ans':a,'exp':e}
    def answer_question(self,key):
        if self.question_locked: return
        selected=None
        if pygame.K_1<=key<=pygame.K_4: selected=key-pygame.K_1
        elif pygame.K_a<=key<=pygame.K_d: selected=key-pygame.K_a
        if selected is None: return
        q=self.current_question(); ok=selected==q['ans']; self.question_feedback=(selected,ok)
        if ok: self.audio.sound('victory'); self.question_locked=True; self.question_result_until=pygame.time.get_ticks()+QUESTION_CORRECT_DELAY_MS
        else:
            self.question_attempts+=1
            if self.question_attempts>=2: self.state='game_over'; self.audio.play_music('game_over')
    def update_question_result(self):
        if self.state=='question' and self.question_locked and pygame.time.get_ticks()>=self.question_result_until: self.state='victory'; self.question_locked=False

    def add_mana(self,a): self.mana=min(MAX_MANA,self.mana+a)
    def spend_mana(self,cost,key):
        if self.cooldowns[key]>0:
            self.skill_msg=f"ĐANG HỒI CHIÊU: {self.cooldowns[key]/FPS:.1f} GIÂY"; self.skill_msg_time=75; self.audio.sound('skill_cooldown'); return False
        if self.mana<cost:
            self.mana_flash=35; self.skill_msg='KHÔNG ĐỦ MANA!'; self.skill_msg_time=75; self.audio.sound('no_mana'); return False
        self.mana-=cost; return True
    def hurt_player(self,n=1,force=False):
        if self.dash_inv_time>0 and not force: return False
        if self.shield_time>0 and not force:
            self.shield_time=0; self.player.inv=max(self.player.inv,45); self.player.vy=-5; self.skill_msg='KHIÊN ĐÃ VỠ - ĐÃ CHẶN SÁT THƯƠNG!'; self.skill_msg_time=65; self.audio.sound('shield_break'); return False
        return self.player.hurt(n,force)
    def use_skill(self,key):
        if key=='Q' and self.spend_mana(SKILL_WAVE_COST,key):
            x=self.player.rect.right if self.player.facing>0 else self.player.rect.left-74; self.skill_waves.append(SkillWave(x,self.player.rect.centery-50,self.player.facing)); self.cooldowns[key]=SKILL_WAVE_COOLDOWN; self.audio.sound('skill_wave')
        elif key=='E' and self.spend_mana(SKILL_SHIELD_COST,key): self.shield_time=SKILL_SHIELD_TIME; self.cooldowns[key]=SKILL_SHIELD_COOLDOWN; self.audio.sound('skill_shield')
        elif key=='R' and self.spend_mana(SKILL_DASH_COST,key):
            self.cooldowns[key]=SKILL_DASH_COOLDOWN; self.dash_inv_time=SKILL_DASH_INVINCIBLE; self.audio.sound('skill_dash'); d=self.player.facing; hit=set()
            for _ in range(0,SKILL_DASH_DISTANCE,6):
                trial=self.player.rect.move(d*6,0)
                if any(trial.colliderect(pygame.Rect(p)) for p in self.lvl['platforms']+[self.lvl['spawn']]) or any(trial.colliderect(pygame.Rect(z)) for z in self.lvl['death_zones']): break
                self.dash_trails.append([self.player.rect.copy(),24]); self.player.rect=trial; self.player.x=float(trial.x)
                for enemy in self.enemies:
                    if id(enemy) not in hit and trial.colliderect(enemy.rect): enemy.damage(SKILL_DASH_DAMAGE); hit.add(id(enemy))
                if self.boss and self.boss.alive and id(self.boss) not in hit and trial.colliderect(self.boss.rect): self.boss.damage(SKILL_DASH_DAMAGE); hit.add(id(self.boss))
        elif key=='T' and self.spend_mana(SKILL_STORM_COST,key):
            self.cooldowns[key]=SKILL_STORM_COOLDOWN; self.audio.sound('skill_storm'); start=(self.player.rect.centerx+self.player.facing*68,self.player.rect.centery); self.star_bursts.append(StarBladeBurst(start,self.player.facing))
    def update_skills(self):
        for k in self.cooldowns:
            if self.cooldowns[k]>0: self.cooldowns[k]-=1
        if self.shield_time>0: self.shield_time-=1
        if self.dash_inv_time>0: self.dash_inv_time-=1
        if self.mana_flash>0: self.mana_flash-=1
        if self.skill_msg_time>0: self.skill_msg_time-=1
        self.mana_regen_tick+=1
        if self.mana_regen_tick>=MANA_REGEN_FRAMES: self.mana_regen_tick=0; self.add_mana(MANA_REGEN_AMOUNT)
        for p in self.skill_waves:
            p.update()
            for enemy in self.enemies:
                if id(enemy) not in p.hit_ids and p.rect.colliderect(enemy.rect): enemy.damage(SKILL_WAVE_DAMAGE); p.hit_ids.add(id(enemy))
            if self.boss and self.boss.alive and id(self.boss) not in p.hit_ids and p.rect.colliderect(self.boss.rect): self.boss.damage(1); p.hit_ids.add(id(self.boss)); p.alive=False
        self.skill_waves=[p for p in self.skill_waves if p.alive]
        for p in self.star_bursts:
            p.update()
            for enemy in self.enemies:
                if id(enemy) not in p.hit_ids and p.rect.colliderect(enemy.rect): enemy.damage(SKILL_STORM_DAMAGE); p.hit_ids.add(id(enemy))
            if self.boss and self.boss.alive and id(self.boss) not in p.hit_ids and p.rect.colliderect(self.boss.rect): self.boss.damage(SKILL_STORM_BOSS_DAMAGE); p.hit_ids.add(id(self.boss))
        self.star_bursts=[p for p in self.star_bursts if p.alive]
        for t in self.dash_trails: t[1]-=1
        self.dash_trails=[t for t in self.dash_trails if t[1]>0]

    def music_for_state(self):
        if self.state=='paused': return 'pause'
        if self.state=='playing': return self.idx+1
        if self.state in ('question','class_select'): return 'question'
        if self.state=='game_over': return 'game_over'
        if self.state in ('ending','ending_wait'): return 'ending'
        if self.state=='tutorial': return 'tutorial'
        return 'opening'
    def events(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.VIDEORESIZE and not self.full: self.display=pygame.display.set_mode((max(640,e.w),max(420,e.h)),pygame.RESIZABLE)
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key==pygame.K_F11: self.full=not self.full; self.display=pygame.display.set_mode((0,0),pygame.FULLSCREEN) if self.full else pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
                if e.key==pygame.K_F12 and not self.full: pygame.display.iconify()
                if e.key==pygame.K_8: self.audio.toggle_music(); self.audio.play_music(self.music_for_state())
                if e.key==pygame.K_9: self.audio.toggle_sound()
                if e.key==pygame.K_F9 and self.state=='playing': self.state='paused'; self.audio.play_music('pause')
                elif e.key==pygame.K_F10 and self.state=='paused': self.state='playing'; self.audio.play_music(self.idx+1)
                elif self.state=='opening' and e.key in (pygame.K_RETURN,pygame.K_TAB): self.state='tutorial'; self.audio.play_music('tutorial')
                elif self.state=='tutorial' and e.key in (pygame.K_RETURN,pygame.K_TAB): self.state='class_select'; self.audio.play_music('question')
                elif self.state=='class_select' and pygame.K_1<=e.key<=pygame.K_5: self.grade=e.key-pygame.K_0; self.state='playing'; self.load_level(0)
                elif self.state=='question': self.answer_question(e.key)
                elif self.state=='ending' and e.key==pygame.K_RETURN: self.state='ending_wait'
                elif self.state=='ending_wait' and e.key==pygame.K_RETURN: self.state='opening'; self.audio.play_music('opening')
                elif self.state=='game_over' and e.key in (pygame.K_LCTRL,pygame.K_RCTRL): self.state='playing'; self.load_level(self.idx)
                elif self.state=='victory' and e.key==pygame.K_RETURN:
                    if self.idx>=9: self.state='ending'; self.audio.play_music('ending')
                    else: self.state='playing'; self.load_level(self.idx+1)
                elif self.state=='playing':
                    if e.key in (pygame.K_SPACE,pygame.K_UP,pygame.K_w): self.player.jump()
                    if e.key in (pygame.K_TAB,pygame.K_f): self.player.attack_now(); self.audio.sound('hit')
                    if e.key==pygame.K_q: self.use_skill('Q')
                    if e.key==pygame.K_e: self.use_skill('E')
                    if e.key==pygame.K_r: self.use_skill('R')
                    if e.key==pygame.K_t: self.use_skill('T')
    def update(self):
        self.update_skills()
        self.player.update(self.lvl['platforms'],self.lvl['spawn'],pygame.key.get_pressed())
        for e in self.enemies: e.update()
        if self.boss: self.boss.update()
        for c in self.coins:
            if not c['got'] and self.player.rect.colliderect(c['rect']):
                c['got']=True; self.collected+=1; mana_before=self.mana; self.add_mana(MANA_PER_COIN); self.audio.sound('coin')
                if self.mana>mana_before: self.audio.sound('mana_restore')
        ar=self.player.attack_rect()
        if ar.w:
            for e in self.enemies:
                if e.alive and ar.colliderect(e.rect): e.damage()
            if self.boss and self.boss.alive and ar.colliderect(self.boss.rect): self.boss.damage()
        self.enemies=[e for e in self.enemies if e.alive]
        for e in self.enemies:
            if self.player.rect.colliderect(e.rect) and self.hurt_player(): self.audio.sound('hurt')
        if self.boss and self.boss.alive and (self.player.rect.colliderect(self.boss.rect) or self.player.rect.colliderect(self.boss.fire_rect())):
            if self.hurt_player(): self.audio.sound('hurt')
        if any(self.player.rect.colliderect(pygame.Rect(z)) for z in self.lvl.get('damage_zones',[])) and self.player.dmg_cd<=0: self.hurt_player(1,False); self.player.dmg_cd=DAMAGE_ZONE_COOLDOWN; self.audio.sound('hurt')
        if any(self.player.rect.colliderect(pygame.Rect(z)) for z in self.lvl['death_zones']) or self.player.rect.top>HEIGHT+80: self.audio.sound('spike'); self.player.health=0; self.player.dead=True; self.state='game_over'; self.audio.play_music('game_over'); return
        if self.player.dead: self.state='game_over'; self.audio.play_music('game_over')
        boss_ok=not self.boss or not self.boss.alive
        if self.player.rect.colliderect(pygame.Rect(self.lvl['portal'])) and self.collected>=self.lvl['required_coins'] and boss_ok: self.audio.sound('portal'); self.start_question()
    def ui(self):
        # HUD không khung lớn, toàn bộ cụm được căn giữa ngang màn hình.
        # Xu được căn giữa theo dãy tim; thanh mana được căn giữa theo dòng Mana.
        top_y=12
        hearts_x=230
        heart_size=42
        heart_step=46
        hearts_width=(MAX_HEALTH-1)*heart_step+heart_size
        hearts_center=hearts_x+hearts_width//2

        mana_center=576
        mana_bar_w=170
        skills_x=696

        # 5 tim kích thước cũ.
        for i in range(MAX_HEALTH):
            self.screen.blit(self.hfull if i<self.player.health else self.hempty,(hearts_x+i*heart_step,top_y))

        # Xu nằm giữa dãy tim.
        draw_outline_text(self.screen,self.f,f"Xu: {self.collected}/{self.lvl['required_coins']}",(255,255,255),(hearts_center,top_y+55),width=2,center=True)

        # Mana thẳng hàng dọc với tim; chữ và thanh dùng cùng một tâm ngang.
        draw_outline_text(self.screen,self.f,f"Mana: {int(self.mana)}/{MAX_MANA}",(255,255,255),(mana_center,top_y+21),width=2,center=True)
        bar=pygame.Rect(mana_center-mana_bar_w//2,top_y+53,mana_bar_w,21)
        pygame.draw.rect(self.screen,(5,10,20),bar,border_radius=9)
        inner=bar.inflate(-6,-6); inner.w=int(inner.w*max(0,min(1,self.mana/MAX_MANA)))
        color=(255,70,70) if self.mana_flash>0 and (self.mana_flash//4)%2==0 else (165,45,145) if self.mana<20 else (35,190,224) if self.mana<=50 else (25,115,238)
        if inner.w>0:
            pygame.draw.rect(self.screen,color,inner,border_radius=6)
            shine=pygame.Rect(inner.x+2,inner.y+1,max(0,inner.w-4),max(2,inner.h//3)); pygame.draw.rect(self.screen,(165,240,255),shine,border_radius=4)
        pygame.draw.rect(self.screen,(0,0,0),bar,3,border_radius=9)
        pygame.draw.rect(self.screen,(245,185,65),bar,2,border_radius=9)

        # Bốn ô skill ở bên phải, nền đen xanh rất nhẹ và trong suốt.
        skill_data=[('Q',SKILL_WAVE_COST,SKILL_WAVE_COOLDOWN),('E',SKILL_SHIELD_COST,SKILL_SHIELD_COOLDOWN),('R',SKILL_DASH_COST,SKILL_DASH_COOLDOWN),('T',SKILL_STORM_COST,SKILL_STORM_COOLDOWN)]
        box_w=49; box_h=54; gap=10; icon_y=top_y+29
        for i,(key,cost,max_cd) in enumerate(skill_data):
            x=skills_x+i*(box_w+gap)
            draw_outline_text(self.screen,get_font(16),key,(255,235,120),(x+box_w//2,top_y+7),width=1,center=True)
            tile=pygame.Surface((box_w,box_h),pygame.SRCALPHA)
            pygame.draw.rect(tile,(8,14,28,82),tile.get_rect(),border_radius=8)
            pygame.draw.rect(tile,(245,190,75,150),tile.get_rect(),1,border_radius=8)
            self.screen.blit(tile,(x,icon_y))
            icon=pygame.transform.smoothscale(self.skill_icons[key],(42,42)); self.screen.blit(icon,(x+3,icon_y+2))
            cd=self.cooldowns[key]
            if cd>0:
                ratio=max(0,min(1,cd/max_cd)); dark_h=max(1,int(42*ratio))
                shade=pygame.Surface((42,dark_h),pygame.SRCALPHA); shade.fill((0,0,0,130))
                self.screen.blit(shade,(x+3,icon_y+2+42-dark_h))
                draw_outline_text(self.screen,get_font(17),f"{cd/FPS:.1f}",(255,255,255),(x+box_w//2,icon_y+23),width=2,center=True)
            cost_img=get_font(13).render(str(cost),True,(145,225,255)); self.screen.blit(cost_img,cost_img.get_rect(center=(x+box_w//2,icon_y+48)))

        if self.skill_msg_time>0:
            draw_outline_text(self.screen,get_font(34),self.skill_msg,(255,255,255),(WIDTH//2,676),outline=(0,0,0),width=2,center=True)
        if self.idx==9 and self.boss and self.boss.alive:
            draw_outline_text(self.screen,get_font(23),f"BOSS RỒNG LỬA: {self.boss.hp}/30",(255,230,170),(WIDTH//2,126),width=2,center=True)

    def draw_playing(self):
        self.screen.blit(self.bgs[self.idx],(0,0))
        for c in self.coins:
            if not c['got']: self.screen.blit(self.coin_img,c['rect'])
        for e in self.enemies: e.draw(self.screen)
        if self.boss and self.boss.alive: self.boss.draw(self.screen)
        for r,life in self.dash_trails:
            img=self.pimgs['r' if self.player.facing>0 else 'l'].copy(); img.set_alpha(int(145*life/24)); self.screen.blit(img,img.get_rect(midbottom=r.midbottom))
        for p in self.skill_waves: p.draw(self.screen)
        for p in self.star_bursts: p.draw(self.screen)
        self.player.draw(self.screen)
        if self.shield_time>0:
            shield=pygame.transform.smoothscale(self.shield_effect,(54,54)); shield.set_alpha(210+int(45*abs(math.sin(pygame.time.get_ticks()/120)))); self.screen.blit(shield,shield.get_rect(center=(self.player.rect.centerx,self.player.rect.centery+13)))
        self.ui()
        if pygame.time.get_ticks()-self.start_ticks<2000:
            txt=f"Màn {self.idx+1}: {self.lvl['title']}"; draw_outline_text(self.screen,self.big,txt,(255,255,255),(WIDTH//2,HEIGHT//2),outline=(0,0,0),width=2,center=True)
        pr=pygame.Rect(self.lvl['portal'])
        if self.player.rect.colliderect(pr):
            if self.idx==9 and (self.collected<self.lvl['required_coins'] or (self.boss and self.boss.alive)): msg='Bạn cần thu thập đủ xu và đánh bại boss để qua màn.'
            elif self.collected<self.lvl['required_coins']: msg='Chưa đủ xu để qua màn!'
            else: msg=''
            if msg: draw_outline_text(self.screen,get_font(36),msg,(255,255,255),(WIDTH//2,610),outline=(0,0,0),width=1,center=True)
    def overlay_text(self,title,msg,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,90)); self.screen.blit(ov,(0,0)); t=self.big.render(title,True,color); sh=self.big.render(title,True,(0,0,0)); self.screen.blit(sh,sh.get_rect(center=(WIDTH//2+4,285+4))); self.screen.blit(t,t.get_rect(center=(WIDTH//2,285))); m=self.f.render(msg,True,(255,255,255)); self.screen.blit(m,m.get_rect(center=(WIDTH//2,360)))
    def draw_scene(self,name):
        vp=self.videos.get(name)
        if vp: vp.draw(self.screen)
        else: self.screen.fill((0,0,0))

    def draw_class_select(self):
        self.draw_scene('tutorial'); ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,170)); self.screen.blit(ov,(0,0)); title=self.big.render('CHỌN LỚP',True,(255,235,120)); self.screen.blit(title,title.get_rect(center=(WIDTH//2,190)))
        lines=['Nhấn phím số để chọn gói câu hỏi:','1 - Lớp 1','2 - Lớp 2','3 - Lớp 3','4 - Lớp 4','5 - Lớp 5','8 - Bật/tắt nhạc nền','9 - Bật/tắt âm thanh']
        for i,l in enumerate(lines): s=self.f.render(l,True,(255,255,255)); self.screen.blit(s,s.get_rect(center=(WIDTH//2,270+i*43)))
    def draw_question(self):
        self.draw_playing(); ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,180)); self.screen.blit(ov,(0,0)); q=self.current_question()
        title=get_font(46).render('TRẢ LỜI CÂU HỎI ĐỂ QUA MÀN',True,(255,220,70)); self.screen.blit(title,title.get_rect(center=(WIDTH//2,105)))
        y=190; y=draw_wrapped_text(self.screen,f"Câu {self.idx+1} - Lớp {self.grade}: {q['q']}",self.f,(255,255,255),110,y,WIDTH-220,9,center=True)+28
        labels=['1/A','2/B','3/C','4/D']; fb_i,fb_ok=self.question_feedback if self.question_feedback else (None,None)
        for i,opt in enumerate(q['opts']):
            c=(70,255,90) if fb_i==i and fb_ok else (255,75,75) if fb_i==i else (255,255,255); y=draw_wrapped_text(self.screen,f"{labels[i]}. {opt}",self.f,c,195,y,WIDTH-390,6)+9
        if self.question_feedback: _,ok=self.question_feedback; status=('Đúng! '+q['exp']) if ok else 'SAI RỒI! HÃY CHỌN LẠI.'; c=(75,255,100) if ok else (255,95,85)
        else: status=f"BẠN CÒN {2-self.question_attempts} LƯỢT TRẢ LỜI - NHẤN 1-4 HOẶC A-D"; c=(255,230,130)
        draw_wrapped_text(self.screen,status,self.f,c,125,max(y+20,555),WIDTH-250,7,center=True)

    def draw_pause(self):
        self.draw_playing(); ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,165)); self.screen.blit(ov,(0,0)); lines=['TẠM DỪNG','Bấm F10 để tiếp tục',f"Bấm phím 8 để {'tắt' if self.audio.music_enabled else 'mở'} nhạc nền",f"Bấm phím 9 để {'tắt' if self.audio.sound_enabled else 'mở'} âm thanh"]
        for i,l in enumerate(lines): fnt=self.big if i==0 else self.f; color=(255,230,90) if i==0 else (255,255,255); s=fnt.render(l,True,color); self.screen.blit(s,s.get_rect(center=(WIDTH//2,230+i*70)))
    def draw_ending_wait(self):
        self.draw_scene('ending'); ov=pygame.Surface((WIDTH,120),pygame.SRCALPHA); ov.fill((0,0,0,150)); self.screen.blit(ov,(0,648)); msg=self.f.render('Bấm Phím Enter để chơi lại',True,(255,245,120)); self.screen.blit(msg,msg.get_rect(center=(WIDTH//2,705)))
    def run(self):
        while True:
            self.events()
            self.update_question_result()
            if self.state=='playing': self.update()
            if self.state=='opening': self.draw_scene('opening')
            elif self.state=='tutorial': self.draw_scene('tutorial')
            elif self.state=='class_select': self.draw_class_select()
            elif self.state=='playing': self.draw_playing()
            elif self.state=='question': self.draw_question()
            elif self.state=='paused': self.draw_pause()
            elif self.state=='victory': self.draw_playing(); self.overlay_text('CHIẾN THẮNG!','Nhấn ENTER để tiếp tục',(255,225,80))
            elif self.state=='game_over': self.draw_playing(); self.overlay_text('GAME OVER','Nhấn CTRL để chơi lại màn này',(255,45,45))
            elif self.state=='ending': self.draw_scene('ending')
            elif self.state=='ending_wait': self.draw_ending_wait()
            self.present(); self.clock.tick(FPS)
if __name__=='__main__': Game().run()
