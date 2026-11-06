# Hành Trình Huy Hiệu Cổ Đại - README mới

## 1. Giới thiệu

**Hành Trình Huy Hiệu Cổ Đại** là game platformer 2D làm bằng **Python/Pygame**. Người chơi điều khiển nhân vật vượt qua 10 màn chơi, thu thập đủ xu, tránh bẫy, đánh quái, đánh boss rồng ở màn 10 và trả lời câu hỏi học tập để qua màn.

Game hiện có các chức năng chính:

- 10 màn chơi tương ứng với 10 background.
- Opening, hướng dẫn chơi, chọn lớp, gameplay, câu hỏi qua màn, victory, game over và ending.
- Hệ thống chọn lớp từ lớp 1 đến lớp 5.
- Mỗi màn sau khi qua portal sẽ hiện câu hỏi tương ứng với lớp đã chọn.
- Hệ thống trả lời câu hỏi bằng phím số hoặc chữ.
- Nhạc nền và âm thanh MP3.
- Pause game bằng F9, tiếp tục bằng F10.
- Bật/tắt nhạc nền bằng phím 8.
- Bật/tắt âm thanh hiệu ứng bằng phím 9.
- Chế độ chỉnh map/collider bằng F1, F2 và các phím chức năng.

---

## 2. Cách chạy game

### Bước 1: Cài Python

Cài Python 3.10 trở lên.

### Bước 2: Cài Pygame

Mở terminal/cmd tại thư mục game và chạy:

```bash
pip install pygame
```

### Bước 3: Chạy game

```bash
python main.py
```

---

## 3. Cấu trúc file quan trọng

```text
main.py
settings.py
data/levels.json
assets/
  backgrounds/
  scenes/
  player/
  enemies/
  boss/
  items/
  ui/
music/
```

Trong các lần cập nhật nhỏ, chỉ cần thay 3 file:

```text
main.py
settings.py
levels.json
```

Nếu file `levels.json` đang nằm trong thư mục `data/`, hãy chép file cập nhật vào:

```text
data/levels.json
```

---

## 4. Luồng chơi

```text
Opening
→ Hướng dẫn chơi
→ Chọn lớp 1/2/3/4/5
→ Màn 1
→ Thu đủ xu
→ Qua portal
→ Trả lời câu hỏi
→ Trả lời đúng thì chiến thắng
→ Enter để qua màn tiếp theo
→ Màn 10 đánh boss rồng + đủ xu + qua portal + trả lời câu hỏi
→ Ending
→ Enter để hiện dòng chơi lại
→ Enter lần nữa để quay về Opening
```

---

## 5. Chọn lớp và câu hỏi

Sau màn hướng dẫn, game sẽ hiện màn **CHỌN LỚP**.

Người chơi chọn lớp bằng phím:

```text
1: Lớp 1
2: Lớp 2
3: Lớp 3
4: Lớp 4
5: Lớp 5
```

Sau khi chọn lớp, game sẽ dùng bộ câu hỏi tương ứng với lớp đó.

Ví dụ:

```text
Chọn lớp 3
Màn 1 → Câu 1 lớp 3
Màn 2 → Câu 2 lớp 3
Màn 3 → Câu 3 lớp 3
...
Màn 10 → Câu 10 lớp 3
```

---

## 6. Quy tắc trả lời câu hỏi

Khi người chơi qua portal, game sẽ dừng gameplay trên background hiện tại, làm tối màn hình nhẹ và hiện câu hỏi.

Người chơi có thể trả lời bằng:

```text
1 / 2 / 3 / 4
```

hoặc:

```text
A / B / C / D
```

Quy tắc:

```text
Trả lời đúng:
- Đáp án đúng hiện màu xanh.
- Hiện giải thích.
- Chuyển sang màn chiến thắng.

Trả lời sai lần 1:
- Đáp án sai hiện màu đỏ.
- Người chơi còn 1 lượt trả lời.

Trả lời sai lần 2:
- Game Over.
- Bấm Ctrl để chơi lại màn hiện tại.
```

---

## 7. Điều khiển nhân vật

```text
A / D hoặc ← / →: Di chuyển
W / ↑ / Space: Nhảy
Space hoặc ↑ lần 2: Nhảy cao/double jump
Tab hoặc F: Chém/đánh
```

---

## 8. Điều khiển giao diện và game

```text
Enter hoặc Tab: Bỏ qua Opening/Hướng dẫn
Enter: Qua màn khi chiến thắng
Ctrl: Chơi lại khi Game Over
Esc: Thoát game
F11: Bật/tắt fullscreen
```

---

## 9. Pause, nhạc nền và âm thanh

```text
F9: Tạm dừng game
F10: Tiếp tục game
8: Bật/tắt nhạc nền
9: Bật/tắt âm thanh hiệu ứng
```

Lưu ý: Phím `1` đến `5` dùng để chọn lớp, nên chức năng bật/tắt âm thanh đã được chuyển sang phím `8` và `9` để tránh trùng phím.

Trong màn tạm dừng sẽ hiện:

```text
TẠM DỪNG
Bấm F10 để tiếp tục
Bấm phím 8 để tắt/mở nhạc nền
Bấm phím 9 để tắt/mở âm thanh
```

---

## 10. Âm thanh MP3

Tất cả file âm thanh đặt trong thư mục:

```text
music/
```

### Nhạc nền lặp liên tục

```text
openingsong.mp3              Nhạc Opening
tutorial.mp3                 Nhạc Hướng dẫn chơi
traloicauhoi.mp3             Nhạc chọn lớp và trả lời câu hỏi
endingsong.mp3               Nhạc Ending
gameover.mp3                 Nhạc Game Over
resumegame.mp3               Nhạc Pause
man1dongco.mp3               Nhạc màn 1
man2samac.mp3                Nhạc màn 2
man3baibien.mp3              Nhạc màn 3
man4rungsau.mp3              Nhạc màn 4
man5vungtuyet.mp3            Nhạc màn 5
man6nuilua.mp3               Nhạc màn 6
man7thanhphotrenmay.mp3      Nhạc màn 7
man8nhamaycokhi.mp3          Nhạc màn 8
man9khonggian.mp3            Nhạc màn 9
man10dencocuoicung.mp3       Nhạc màn 10
```

### Âm thanh hiệu ứng

```text
hit.mp3             Âm thanh khi nhân vật chém
portal.mp3          Âm thanh khi đi qua portal
spiketrap.mp3       Âm thanh khi chạm vùng đỏ
 tiengmatmau.mp3    Âm thanh khi mất máu
tiengxu.mp3         Âm thanh khi nhặt xu
victory.mp3         Âm thanh khi chiến thắng
```

Lưu ý: Tên file nên viết đúng như trong danh sách trên để game đọc được.

---

## 11. Quy tắc gameplay

### Xu

```text
Màn 1 đến màn 5: cần 10 xu
Màn 6 đến màn 10: cần 15 xu
```

Nếu chưa đủ xu mà chạm portal, game sẽ báo chưa đủ xu.

### Quái

```text
Quái thường có 3 máu.
Nhân vật chém trúng quái thì quái mất 1 máu.
Quái di chuyển qua lại để canh xu và portal.
Chạm quái thì nhân vật mất máu.
```

### Boss rồng màn 10

```text
Boss rồng có 30 máu.
Phải thu đủ xu và đánh bại boss mới qua được portal.
Boss rồng phun lửa đúng hướng theo hướng rồng đang quay.
```

Thông báo màn 10:

```text
Bạn cần thu thập đủ xu và đánh bại boss để qua màn.
```

### Tim máu

```text
Nhân vật có 5 tim.
Mất máu thì tim chuyển thành tim trống.
Hết tim thì Game Over.
```

### Vùng đỏ

```text
Chạm vùng đỏ là Game Over ngay.
```

### Vùng vàng

```text
Chạm hoặc đứng trong vùng vàng sẽ mất 1 máu theo thời gian.
Đứng lâu trong vùng vàng sẽ chết dần.
```

---

## 12. Chỉnh map/collider

Bật chế độ chỉnh map:

```text
F1: Hiện/ẩn collider
F2: Bật/tắt chế độ chỉnh map
```

Các phím chỉnh map:

```text
F3: Thêm platform xanh one-way
F4: Thêm vùng đỏ chết ngay
F5: Đặt portal tàng hình
F6: Thêm vùng vàng mất máu từ từ
F7: Đặt spawn tím
F8: Lưu map vào levels.json
Backspace: Xóa vật thể đang chọn
```

Điều khiển bằng chuột:

```text
Click/kéo vật thể: Di chuyển vật thể
Kéo góc phải dưới: Chỉnh kích thước vật thể
```

Màu collider:

```text
Xanh lá: Platform one-way
Tím: Spawn
Đỏ: Vùng chết ngay
Vàng: Vùng mất máu theo thời gian
Xanh cyan: Portal tàng hình
Vàng viền nhỏ: Coin
Tím hồng: Enemy/Boss collider
```

---

## 13. Lưu ý khi cập nhật file

Khi chỉ sửa lỗi chức năng, bạn có thể chỉ thay:

```text
main.py
settings.py
data/levels.json
```

Nếu đã chỉnh map hoàn chỉnh trong game, nên giữ `levels.json` của bạn và chỉ sửa `main.py` hoặc `settings.py` khi không cần thay đổi dữ liệu map.

---

## 14. Các lỗi đã sửa gần đây

```text
- Đổi phím bật/tắt nhạc nền từ 1 sang 8.
- Đổi phím bật/tắt âm thanh từ 2 sang 9.
- Sửa sóng kiếm khi chém bên trái bị ngược vòng cung.
- Làm sóng kiếm đậm hơn, rõ hơn.
- Sửa boss rồng khi quay sang phải không còn phun lửa từ đuôi.
- Giữ nguyên levels.json đã chỉnh platform/collider.
```
